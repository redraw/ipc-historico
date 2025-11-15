# Análisis del IPC Argentino por Divisiones

Este proyecto analiza la evolución del Índice de Precios al Consumidor (IPC) argentino por divisiones y regiones, utilizando datos oficiales del INDEC.

## Características

- **Datos actualizados automáticamente**: GitHub Actions descarga los datos más recientes del INDEC mensualmente
- **48 gráficos interactivos**: Visualizaciones con Plotly que permiten zoom, filtrado y exploración de datos
- **Análisis por regiones**: Análisis completo para todas las regiones argentinas (Nacional, GBA, Pampeana, Noreste, Noroeste, Cuyo, Patagonia)
- **Comparación entre regiones**: Gráficos específicos para comparar la evolución del IPC entre diferentes regiones
- **Múltiples visualizaciones por región**:
  - Evolución del índice por división
  - Variación mensual e interanual
  - Mapas de calor
  - Inflación acumulada desde diciembre 2016
  - Últimos 12 meses
- **Análisis comparativo entre regiones**:
  - Evolución comparada del índice
  - Variaciones mensuales e interanuales
  - Ranking de inflación regional
  - Heatmaps comparativos

## Uso

### Requisitos

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (gestor de paquetes Python)

### Instalación de uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Generar análisis completo

```bash
# 1. Generar gráficos para todas las regiones (42 gráficos)
for region in Nacional GBA Pampeana Noreste Noroeste Cuyo Patagonia; do
  uv run scripts/analizar_ipc.py --region $region
done

# 2. Generar comparaciones entre regiones (6 gráficos)
uv run scripts/comparar_regiones.py

# 3. Generar index.html con todos los gráficos organizados
uv run scripts/generar_index.py
```

### Análisis individual por región

```bash
# Análisis nacional (por defecto)
uv run scripts/analizar_ipc.py

# Análisis para una región específica
uv run scripts/analizar_ipc.py --region GBA

# Análisis desde un período específico
uv run scripts/analizar_ipc.py --region Nacional --periodo-inicial 202001
```

### Opciones disponibles

**analizar_ipc.py**:
- `--region`: Región a analizar (Nacional, GBA, Pampeana, Noreste, Noroeste, Cuyo, Patagonia)
- `--periodo-inicial`: Período inicial en formato YYYYMM (ej: 202001)

**comparar_regiones.py**:
- Sin opciones, genera automáticamente comparaciones entre todas las regiones

**generar_index.py**:
- Sin opciones, escanea todos los gráficos y genera el index.html organizado

### Ver los resultados

Abre el archivo `index.html` en tu navegador para ver todos los 48 gráficos organizados por región.

## Actualización automática

El proyecto incluye un GitHub Action (`.github/workflows/update-ipc.yml`) que:

1. Se ejecuta automáticamente el día 15 de cada mes
2. Descarga los datos más recientes del INDEC
3. Genera todos los gráficos para todas las regiones
4. Hace commit y push de los cambios si hay datos nuevos

También puedes ejecutar la actualización manualmente desde la pestaña "Actions" en GitHub.

## Fuente de datos

Los datos provienen del [Instituto Nacional de Estadística y Censos (INDEC)](https://www.indec.gob.ar/):
- **URL**: https://www.indec.gob.ar/ftp/cuadros/economia/serie_ipc_divisiones.csv
- **Base**: Diciembre 2016 = 100
- **Clasificación**: Divisiones COICOP (Classification of Individual Consumption According to Purpose)

## Divisiones COICOP

El IPC se divide en las siguientes categorías de gasto:

- **00**: Nivel general
- **01**: Alimentos y bebidas no alcohólicas
- **02**: Bebidas alcohólicas y tabaco
- **03**: Prendas de vestir y calzado
- **04**: Vivienda, agua, electricidad y otros combustibles
- **05**: Equipamiento y mantenimiento del hogar
- **06**: Salud
- **07**: Transporte
- **08**: Comunicación
- **09**: Recreación y cultura
- **10**: Educación
- **11**: Restaurantes y hoteles
- **12**: Bienes y servicios varios

## Tecnologías utilizadas

- **Python**: Lenguaje principal
- **pandas**: Procesamiento y análisis de datos
- **Plotly**: Visualizaciones interactivas
- **Jinja2**: Generación de la página web
- **uv**: Gestión de dependencias y ejecución
- **GitHub Actions**: Automatización y CI/CD

## Inspiración

Este proyecto está basado en el proyecto [monotributo](../monotributo), adaptando la misma estructura y metodología para el análisis del IPC.

## Licencia

Los datos del IPC son de dominio público y pertenecen al INDEC. Este proyecto es de código abierto.
