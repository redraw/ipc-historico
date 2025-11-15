#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "jinja2",
# ]
# ///
"""
Script para generar el index.html con todos los gráficos organizados
"""

import glob
import os
from datetime import datetime
from jinja2 import Template

# Obtener fecha de última actualización de los datos
try:
    datos_timestamp = os.path.getmtime('data/serie_ipc_divisiones.csv')
    fecha_datos = datetime.fromtimestamp(datos_timestamp).strftime('%d/%m/%Y %H:%M:%S')
except:
    fecha_datos = 'No disponible'

# Obtener todos los archivos HTML
graficos_dir = 'graficos'
html_files = sorted(glob.glob(f'{graficos_dir}/ipc_*.html'))

# Definir regiones y sus etiquetas
regiones_info = {
    'nacional': 'Nacional',
    'gba': 'GBA (Gran Buenos Aires)',
    'pampeana': 'Pampeana',
    'noreste': 'Noreste (NEA)',
    'noroeste': 'Noroeste (NOA)',
    'cuyo': 'Cuyo',
    'patagonia': 'Patagonia',
    'comparacion': 'Comparación entre Regiones'
}

# Definir tipos de gráficos y sus descripciones
graficos_info = {
    'indice': {
        'titulo': 'Evolución del Índice',
        'descripcion': 'Evolución del índice de precios por división'
    },
    'variacion_mensual': {
        'titulo': 'Variación Mensual',
        'descripcion': 'Variación porcentual mensual del IPC'
    },
    'variacion_interanual': {
        'titulo': 'Variación Interanual',
        'descripcion': 'Variación porcentual interanual del IPC'
    },
    'ultimos_12_meses': {
        'titulo': 'Últimos 12 Meses',
        'descripcion': 'Comparación de variación mensual en los últimos 12 meses'
    },
    'heatmap': {
        'titulo': 'Mapa de Calor',
        'descripcion': 'Mapa de calor de variación mensual por división'
    },
    'acumulado': {
        'titulo': 'Inflación Acumulada',
        'descripcion': 'Inflación acumulada desde diciembre 2016'
    },
    'ranking': {
        'titulo': 'Ranking Regional',
        'descripcion': 'Ranking de inflación acumulada en últimos 12 meses'
    }
}

# Organizar gráficos por región
graficos_por_region = {region: [] for region in regiones_info.keys()}

for html_file in html_files:
    basename = os.path.basename(html_file)

    # Determinar región
    region = None
    for key in regiones_info.keys():
        if f'ipc_{key}_' in basename:
            region = key
            break

    if not region:
        continue

    # Determinar tipo de gráfico
    tipo = None
    titulo = None
    descripcion = 'Gráfico del IPC'

    for key, info in graficos_info.items():
        if key in basename:
            tipo = key
            titulo = info['titulo']
            descripcion = info['descripcion']
            break

    if not titulo:
        continue

    graficos_por_region[region].append({
        'filename': f'{graficos_dir}/{basename}',
        'title': titulo,
        'description': descripcion,
        'tipo': tipo
    })

# Ordenar gráficos dentro de cada región
orden_tipos = ['indice', 'variacion_mensual', 'variacion_interanual',
               'ultimos_12_meses', 'heatmap', 'acumulado', 'ranking']

for region in graficos_por_region:
    graficos_por_region[region].sort(
        key=lambda x: orden_tipos.index(x['tipo']) if x['tipo'] in orden_tipos else 999
    )

# Preparar estructura para el template
graficos_agrupados = []

# Primero la sección de comparación
if graficos_por_region['comparacion']:
    graficos_agrupados.append({
        'label': regiones_info['comparacion'],
        'graficos': graficos_por_region['comparacion'],
        'region_key': 'comparacion'
    })

# Luego todas las demás regiones
for region_key, region_label in regiones_info.items():
    if region_key != 'comparacion' and graficos_por_region[region_key]:
        graficos_agrupados.append({
            'label': region_label,
            'graficos': graficos_por_region[region_key],
            'region_key': region_key
        })

# Cargar template y renderizar
with open('index.jinja', 'r', encoding='utf-8') as f:
    template_content = f.read()

# Actualizar template con nueva estructura
template_actualizado = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Análisis del IPC - Índice de Precios al Consumidor</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #007bff;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 0;
            margin-bottom: 15px;
        }
        h3 {
            color: #666;
            margin-top: 25px;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e0e0e0;
        }
        .card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .file-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        .file-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #007bff;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .file-item:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .file-item a {
            color: #007bff;
            text-decoration: none;
            font-weight: 600;
            font-size: 16px;
            display: block;
            margin-bottom: 8px;
        }
        .file-item a:hover {
            text-decoration: underline;
            color: #0056b3;
        }
        .file-item .description {
            color: #666;
            font-size: 13px;
            line-height: 1.4;
        }
        .info {
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .timestamp {
            color: #999;
            font-size: 12px;
            margin-top: 20px;
        }
        .highlight {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }
        .nav-section {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .nav-section p {
            margin: 0 0 12px 0;
            color: #666;
            font-size: 14px;
        }
        .nav-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .nav-button {
            display: inline-block;
            padding: 8px 16px;
            background: white;
            color: #333;
            text-decoration: none;
            border: 1px solid #ddd;
            font-size: 14px;
            transition: border-color 0.2s;
        }
        .nav-button:hover {
            border-color: #007bff;
            color: #007bff;
        }
    </style>
</head>
<body>
    <h1>📊 Análisis del IPC Argentino por Divisiones</h1>

    <div class="card">
        <div class="info">
            <strong>Datos actualizados:</strong> {{ fecha_datos }}
        </div>
    </div>

    <div class="nav-section">
        <p>Ir a:</p>
        <div class="nav-grid">
        {% for grupo in graficos_agrupados %}
            <a href="#{{ grupo.region_key }}" class="nav-button">{{ grupo.label }}</a>
        {% endfor %}
        </div>
    </div>

    {% for grupo in graficos_agrupados %}
    <div class="card" id="{{ grupo.region_key }}">
        <h2>{{ grupo.label }}</h2>
        {% if grupo.region_key == 'comparacion' %}
        <p>Gráficos comparativos entre todas las regiones argentinas. Útil para analizar diferencias regionales en la evolución del IPC.</p>
        {% else %}
        <p>Análisis detallado del IPC para la región {{ grupo.label }}. Haz clic en cualquier gráfico para verlo en detalle.</p>
        {% endif %}

        <div class="file-list">
        {% for item in grupo.graficos %}
            <div class="file-item">
                <a href="{{ item.filename }}" target="_blank">{{ item.title }}</a>
                <div class="description">{{ item.description }}</div>
            </div>
        {% endfor %}
        </div>
    </div>
    {% endfor %}

    <div class="card">
        <h2>Acerca del Análisis</h2>
        <p>Estos gráficos muestran la evolución del Índice de Precios al Consumidor (IPC) argentino por divisiones y regiones desde diciembre de 2016.</p>
        <ul>
            <li><strong>Índice:</strong> Valor del índice con base diciembre 2016 = 100</li>
            <li><strong>Variación Mensual:</strong> Cambio porcentual respecto al mes anterior</li>
            <li><strong>Variación Interanual:</strong> Cambio porcentual respecto al mismo mes del año anterior</li>
            <li><strong>Inflación Acumulada:</strong> Crecimiento porcentual total desde la base (diciembre 2016)</li>
            <li><strong>Divisiones:</strong> NIVEL GENERAL y categorías de gasto según clasificación COICOP</li>
            <li><strong>Regiones:</strong> Nacional, GBA, Pampeana, Noreste (NEA), Noroeste (NOA), Cuyo, Patagonia</li>
        </ul>
        <p><strong>Fuente:</strong> Instituto Nacional de Estadística y Censos (INDEC)</p>
        <p><strong>Total de gráficos:</strong> {{ total_graficos }}</p>
    </div>

    <div class="timestamp">
        Generado automáticamente con scripts de análisis IPC
    </div>
</body>
</html>
"""

# Contar total de gráficos
total_graficos = sum(len(grupo['graficos']) for grupo in graficos_agrupados)

template = Template(template_actualizado)
html_output = template.render(
    fecha_datos=fecha_datos,
    graficos_agrupados=graficos_agrupados,
    total_graficos=total_graficos
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print('=' * 80)
print('INDEX.HTML GENERADO EXITOSAMENTE')
print('=' * 80)
print(f'Fecha de datos: {fecha_datos}')
print(f'Total de regiones: {len(graficos_agrupados)}')
print(f'Total de gráficos: {total_graficos}')
print('\nGráficos por región:')
for grupo in graficos_agrupados:
    print(f'  {grupo["label"]:30s}: {len(grupo["graficos"])} gráficos')
print('=' * 80)
print('✓ Archivo index.html actualizado')
