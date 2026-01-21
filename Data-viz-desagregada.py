import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Button
import os

# -----------------------------
# Configuration & Labels
# -----------------------------
LABEL_MAPPING = {
    "Salarios y sueldos": "Salarios y sueldos",
    "Bonos, incentivos, gratificaciones, premios, aguinaldos": "Bonos y premios",
    "Comisiones y propinas": "Comisiones y propinas",
    "Bienes y servicios gratuitos o subsidiados por parte de un empleador": "Beneficios especie",
    "Acciones ofrecidas como parte de la remuneración": "Acciones",
    "Participación en beneficios": "Partic. beneficios",
    "Indemnización por despido y despido": "Indemnizaciones",
    "Independientes: Ingresos del trabajo por cuenta propia": "Trabajo cuenta propia",
    "Independientes: Ganancias netas de empresas no constituidas en sociedad": "Ganancias empresas",
    "Independientes: Bienes producidos para consumo propio": "Consumo propio",
    "Independientes: Bienes y servicios producidos para trueque": "Trueque",
    "Dividendos, utilidades e intereses de la propiedad de activos financieros": "Dividendos e intereses",
    "Alquiler de maquinaria, vehiculos y rendimiento de activos no financieros (ganado a capitalizacion, derechos de aguas)": "Alquileres y rendimientos",
    "Derechos de autor, regalías": "Regalías",
    "Jubilaciones y pensiones de la Seguridad Social": "Jubilaciones",
    "Montepios y pensiones de orfandad": "Montepíos y orfandad",
    "Transferencias de asistencia social (excluidas las transferencias sociales en especie)": "Asistencia social",
    "Transferencias corrientes recibidas de instituciones sin fines de lucro (iglesias, fundaciones)": "Inst sin fines lucro",
    "Transferencias corrientes recibidas de otros hogares": "Remesas y otros hogares",
    "Primas por seguros": "Seguros",
    "Transferencias sociales en especie (TRSE) recibidas": "TRSE recibidas",
    "NPC": "No clasificable",
    "No considerado": "No ingreso corriente"
}

# -----------------------------
# Data Loading & Cleaning
# -----------------------------
df_raw = pd.read_csv('datos/Variables-pais-componente.csv')

# Clean columns and strings
df_raw.columns = df_raw.columns.str.strip()

# Normalize whitespace in all string columns (replace \xa0 with space and strip)
for col in ['Fuente de ingreso', 'concepto_canberra_definitivo']:
    df_raw[col] = df_raw[col].str.replace('\xa0', ' ', regex=True).str.strip()
    # Collapse multiple spaces into one to be super robust
    df_raw[col] = df_raw[col].str.replace(r'\s+', ' ', regex=True)

# Apply label mapping
df_raw['label_short'] = df_raw['concepto_canberra_definitivo'].map(lambda x: LABEL_MAPPING.get(x, x))

# ISO columns list
iso_cols = [col for col in df_raw.columns if col not in ['Fuente de ingreso', 'concepto_canberra_definitivo', 'Total', 'label_short']]
fuentes = df_raw['Fuente de ingreso'].unique().tolist()
# Filter out non-income current sources if present
fuentes = [f for f in fuentes if "No forma parte" not in f and "No es posible" not in f]

# -----------------------------
# Visualization State
# -----------------------------
current_fuente = fuentes[0]

# UN Blues Palette Generator
un_blue = "#4BA3D3"
def get_blue_shades(n):
    """Generate n shades of blue based on UN Blue."""
    import matplotlib.colors as mcolors
    base_rgb = mcolors.to_rgb(un_blue)
    shades = []
    for i in range(n):
        # Vary luminance/saturation slightly
        factor = 0.4 + (i / max(1, n-1)) * 0.7  # Start darker, go lighter
        shade = [min(1, c * factor) for c in base_rgb]
        shades.append(shade)
    return shades

fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(left=0.25, bottom=0.15) 

def update_plot(fuente):
    ax.clear()
    data_sub = df_raw[df_raw['Fuente de ingreso'] == fuente]
    
    # Identify countries with at least one question
    total_per_country = data_sub[iso_cols].sum().astype(float)
    active_countries = total_per_country[total_per_country > 0].index.tolist()
    
    if not active_countries:
        ax.text(0.5, 0.5, "Sin datos para esta fuente en ningún país", 
                ha='center', va='center', transform=ax.transAxes)
        plt.draw()
        return

    # Bottom tracker for stacking
    bottom = pd.Series(0, index=active_countries)
    
    # Monochromatic Blue Palette
    n_components = len(data_sub)
    colors = get_blue_shades(n_components)
    
    for i, (_, row) in enumerate(data_sub.iterrows()):
        values = row[active_countries].astype(float)
        ax.bar(active_countries, values, bottom=bottom, label=row['label_short'], 
               color=colors[i], edgecolor='white', linewidth=0.5)
        bottom += values

    ax.set_title(f"Desagregación: {fuente}", fontsize=12, pad=15)
    ax.set_ylabel("Nº de preguntas / variables")
    ax.set_xlabel("País (ISO)")
    
    # Styling
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    
    # Legend
    ax.legend(title="Componentes", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.draw()

# -----------------------------
# Interactive Widgets
# -----------------------------
# Radio Buttons for selection
ax_radio = plt.axes([0.02, 0.4, 0.18, 0.3], facecolor='#f0f0f0')
radio = RadioButtons(ax_radio, fuentes)

def handle_radio(label):
    global current_fuente
    current_fuente = label
    update_plot(label)

radio.on_clicked(handle_radio)

# Save Button
ax_save = plt.axes([0.8, 0.02, 0.1, 0.05])
btn_save = Button(ax_save, 'Guardar PNG')

def save_plot(event):
    if not os.path.exists('Salidas'):
        os.makedirs('Salidas')
    
    filename = f"Salidas/desagregada_{current_fuente.replace(' ', '_')}.png"
    
    # Hide widgets for a clean export
    ax_radio.set_visible(False)
    ax_save.set_visible(False)
    
    # Save the figure
    fig.savefig(filename, dpi=300, bbox_inches='tight')
    
    # Restore widgets
    ax_radio.set_visible(True)
    ax_save.set_visible(True)
    plt.draw()
    
    print(f"Grafico guardado sin controles: {filename}")

btn_save.on_clicked(save_plot)

# Initial call
update_plot(current_fuente)
print("Iniciando visualización interactiva...")
print(f"Usa el panel de la izquierda para cambiar la fuente.")
print(f"Haz clic en 'Guardar PNG' para exportar el gráfico actual.")

plt.show()
