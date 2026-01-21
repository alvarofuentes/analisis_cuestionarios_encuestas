#Data-viz-ingresos-por-fuente

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import textwrap

# -----------------------------
# Data
# -----------------------------
# Load data from CSV
df_raw = pd.read_csv('datos/Totales-por-componente.csv')

# Clean category names (remove trailing spaces and special characters)
df_raw['Fuente de ingreso'] = df_raw['Fuente de ingreso'].str.strip()

# Categories we want to include in the plot
target_categories = [
    "Empleo asalariado",
    "Trabajo independiente",
    "Rentas de la propiedad",
    "Transferencias corrientes recibidas",
    "Transferencias sociales en especie (TRSE) recibidas"
]

# Filter to include only target categories and maintain order
df = df_raw[df_raw['Fuente de ingreso'].isin(target_categories)].copy()
df['Fuente de ingreso'] = pd.Categorical(df['Fuente de ingreso'], categories=target_categories, ordered=True)
df = df.sort_values('Fuente de ingreso').reset_index(drop=True)

# Select only ISO country columns (exclude 'Fuente de ingreso' and 'Total')
iso_cols = [col for col in df.columns if col not in ['Fuente de ingreso', 'Total']]

# -----------------------------
# Helpers
# -----------------------------
def wrap_label(label, width=26):
    """Wrap long x-axis labels to avoid overlap."""
    return "\n".join(textwrap.wrap(label, width=width, break_long_words=False))

wrapped_labels = [wrap_label(x) for x in df["Fuente de ingreso"]]
values_per_source = [df.loc[i, iso_cols].values for i in range(len(df))]

# Naciones Unidas–style blue for medians
un_blue = "#4BA3D3"

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(11.5, 4.8), facecolor="white")
ax = plt.gca()
ax.set_facecolor("white")

ax.boxplot(
    values_per_source,
    labels=wrapped_labels,
    patch_artist=False,
    showfliers=False,                 # outliers added manually
    medianprops=dict(color=un_blue, linewidth=2),
)

# Axis styling
ax.set_ylabel("Nº de preguntas / variables", fontsize=10)
ax.set_xlabel("")
ax.set_ylim(0, 75)                   # clave para mostrar PER=70 y CHL=51
ax.tick_params(axis="x", labelsize=9)
ax.tick_params(axis="y", labelsize=9)

for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)

# -----------------------------
# Outliers: Tukey 1.5 * IQR
# -----------------------------
rng = np.random.default_rng(42)

for i in range(len(df)):
    vals = df.loc[i, iso_cols].astype(float)
    q1, q3 = np.quantile(vals, [0.25, 0.75])
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = vals[(vals < lower) | (vals > upper)].sort_values()

    for j, (iso, y) in enumerate(outliers.items()):
        ax.text(
            i + 1 + rng.uniform(-0.12, 0.12),  # pequeño jitter horizontal
            y + (j % 2) * 0.6,                 # leve ajuste vertical
            iso,
            ha="center",
            va="bottom",
            fontsize=9,
            clip_on=True,
        )

plt.tight_layout()

# Save the plot
plt.savefig("Salidas/plot 1.png", dpi=300, bbox_inches="tight")
print("Gráfico guardado en Salidas/plot 1.png")

plt.show()
