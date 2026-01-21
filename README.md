# Análisis de Cuestionarios y Encuestas de Hogares (BADEHOG)

## Descripción
Este proyecto realiza un análisis comparativo del número de ítems (variables o preguntas) utilizados en los cuestionarios de encuestas de hogares de América Latina y el Caribe (LAC) para estimar las variables de ingresos, siguiendo el marco del manual de Canberra.

## Estructura del Proyecto
- `datos/`: Carpeta con las bases de datos en formato CSV.
  - `Totales-por-componente.csv`: Resumen de preguntas por fuente de ingreso y país.
  - `Variables-pais-componente.csv`: Desagregación por componente específico y concepto Canberra.
- `Salidas/`: Carpeta donde se guardan las visualizaciones exportadas (PNG).
- `Data-viz-ingresos-por-fuente.py`: Genera gráficos de caja (boxplots) comparativos por país.
- `Data-viz-desagregada.py`: Herramienta interactiva para visualizar la desagregación de componentes con paletas oficiales (UN Blue).
- `.conda_env/`: Entorno virtual de Python con las dependencias necesarias.
- `.gitignore`: Configuración para excluir archivos temporales y el entorno virtual de Git.

## Configuración del Entorno
El proyecto utiliza un entorno de Conda local para asegurar la reproducibilidad. Las librerías instaladas incluyen:
- `pandas`: Procesamiento de datos.
- `matplotlib`: Generación de gráficos.
- `numpy`: Cálculos numéricos.
- `openpyxl`: Soporte para archivos Excel.

## Uso de las Herramientas
Para ejecutar los scripts de visualización, utiliza el intérprete de Python del entorno local desde la terminal:

### 1. Visualización de Totales
Genera un gráfico de cajas que muestra la distribución de preguntas por país para cada fuente de ingreso.
```powershell
.\.conda_env\python.exe Data-viz-ingresos-por-fuente.py
```

### 2. Visualización Desagregada (Interactiva)
Permite explorar los componentes específicos de cada fuente. Incluye un menú de selección y un botón para exportar imágenes limpias.
```powershell
.\.conda_env\python.exe Data-viz-desagregada.py
```
*Nota: Los países con cero preguntas para una fuente seleccionada se ocultan automáticamente para mejorar la claridad visual.*

## Exportación de Resultados
Los gráficos se guardan automáticamente en la carpeta `Salidas/` con alta resolución (300 DPI), listos para ser incluidos en documentos e informes técnicos.
