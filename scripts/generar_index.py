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

# Contar total de gráficos
total_graficos = sum(len(grupo['graficos']) for grupo in graficos_agrupados)

template = Template(template_content)
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
