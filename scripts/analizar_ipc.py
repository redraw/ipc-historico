#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pandas",
#   "plotly",
#   "jinja2",
# ]
# ///
"""
Script para analizar la evolución del IPC por divisiones
Genera gráficos interactivos usando pandas y plotly
"""

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import argparse
import os
import glob
from jinja2 import Template

# Configurar argumentos de línea de comandos
parser = argparse.ArgumentParser(
    description='Analiza la evolución del IPC por divisiones y regiones'
)
parser.add_argument(
    '--region',
    type=str,
    default='Nacional',
    help='Región a analizar (Nacional, GBA, Pampeana, Noreste, Noroeste, Cuyo, Patagonia)'
)
parser.add_argument(
    '--periodo-inicial',
    type=str,
    default=None,
    help='Período inicial en formato YYYYMM (ej: 201612). Si no se especifica, usa todos los datos'
)

args = parser.parse_args()

# Crear carpeta para gráficos si no existe
graficos_dir = 'graficos'
os.makedirs(graficos_dir, exist_ok=True)

# Cargar los datos del CSV
print('Cargando datos del IPC desde INDEC...')
df = pd.read_csv('data/serie_ipc_divisiones.csv', encoding='latin1', sep=';', decimal=',', na_values=['NA'])

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Convertir período a datetime
df['Periodo'] = pd.to_datetime(df['Periodo'].astype(str), format='%Y%m')
df['year_month'] = df['Periodo'].dt.strftime('%Y-%m')

# Filtrar por región
df_region = df[df['Region'] == args.region].copy()

if len(df_region) == 0:
    print(f"Error: No se encontraron datos para la región '{args.region}'")
    print(f"Regiones disponibles: {', '.join(sorted(df['Region'].unique()))}")
    exit(1)

# Filtrar por período inicial si se especificó
if args.periodo_inicial:
    periodo_inicial = pd.to_datetime(args.periodo_inicial, format='%Y%m')
    df_region = df_region[df_region['Periodo'] >= periodo_inicial]

# Ordenar por período
df_region = df_region.sort_values('Periodo')

print('=' * 80)
print('ANÁLISIS DE EVOLUCIÓN DEL IPC')
print('=' * 80)
print(f'\nRegión: {args.region}')
print(f'Divisiones disponibles: {len(df_region["Descripcion"].unique())}')
print(f'Períodos analizados: {df_region["Periodo"].min().strftime("%Y-%m")} - {df_region["Periodo"].max().strftime("%Y-%m")}')
print(f'Total de registros: {len(df_region)}')

# Obtener todas las divisiones únicas (filtrar NaN)
divisiones = df_region['Descripcion'].dropna().unique()

# Gráfico 1: Evolución del Índice por División
print('\nGenerando gráfico 1: Evolución del Índice por División...')
fig1 = go.Figure()

# Colores para las divisiones más importantes
colores = px.colors.qualitative.Set3

for idx, division in enumerate(sorted([d for d in divisiones if isinstance(d, str)])):
    datos_div = df_region[df_region['Descripcion'] == division].sort_values('Periodo')

    # Solo agregar si hay datos válidos
    if datos_div['Indice_IPC'].notna().any():
        fig1.add_trace(go.Scatter(
            x=datos_div['Periodo'],
            y=datos_div['Indice_IPC'],
            mode='lines',
            name=division,
            line=dict(width=2 if division == 'NIVEL GENERAL' else 1),
            visible=True if division == 'NIVEL GENERAL' else 'legendonly'
        ))

fig1.update_layout(
    title=f'IPC - Evolución del Índice por División - {args.region}',
    xaxis_title='Período',
    yaxis_title='Índice (Base Dic 2016 = 100)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_indice.html'
fig1.write_html(output_file)
print(f'✓ Gráfico 1 generado: {output_file}')

# Gráfico 2: Variación Mensual (v_m_IPC)
print('Generando gráfico 2: Variación Mensual...')
fig2 = go.Figure()

for division in sorted([d for d in divisiones if isinstance(d, str)]):
    datos_div = df_region[df_region['Descripcion'] == division].sort_values('Periodo')

    if datos_div['v_m_IPC'].notna().any():
        fig2.add_trace(go.Scatter(
            x=datos_div['Periodo'],
            y=datos_div['v_m_IPC'],
            mode='lines',
            name=division,
            line=dict(width=2 if division == 'NIVEL GENERAL' else 1),
            visible=True if division == 'NIVEL GENERAL' else 'legendonly'
        ))

fig2.update_layout(
    title=f'IPC - Variación Mensual por División - {args.region}',
    xaxis_title='Período',
    yaxis_title='Variación Mensual (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_variacion_mensual.html'
fig2.write_html(output_file)
print(f'✓ Gráfico 2 generado: {output_file}')

# Gráfico 3: Variación Interanual (v_i_a_IPC)
print('Generando gráfico 3: Variación Interanual...')
fig3 = go.Figure()

for division in sorted([d for d in divisiones if isinstance(d, str)]):
    datos_div = df_region[df_region['Descripcion'] == division].sort_values('Periodo')

    if datos_div['v_i_a_IPC'].notna().any():
        fig3.add_trace(go.Scatter(
            x=datos_div['Periodo'],
            y=datos_div['v_i_a_IPC'],
            mode='lines',
            name=division,
            line=dict(width=2 if division == 'NIVEL GENERAL' else 1),
            visible=True if division == 'NIVEL GENERAL' else 'legendonly'
        ))

fig3.update_layout(
    title=f'IPC - Variación Interanual por División - {args.region}',
    xaxis_title='Período',
    yaxis_title='Variación Interanual (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_variacion_interanual.html'
fig3.write_html(output_file)
print(f'✓ Gráfico 3 generado: {output_file}')

# Gráfico 4: Comparación de Variación Mensual (últimos 12 meses)
print('Generando gráfico 4: Comparación últimos 12 meses...')

# Obtener últimos 12 meses
fecha_max = df_region['Periodo'].max()
fecha_inicio = fecha_max - pd.DateOffset(months=11)
df_ultimos_12 = df_region[df_region['Periodo'] >= fecha_inicio].copy()

# Filtrar solo nivel general y principales divisiones (excluyendo subcategorías)
# Solo códigos numéricos de máximo 2 dígitos
df_principales = df_ultimos_12[
    (df_ultimos_12['Codigo'].str.len() <= 2) &
    (df_ultimos_12['Codigo'].str.match(r'^\d+$', na=False))
]
divisiones_principales = df_principales['Descripcion'].unique()

fig4 = go.Figure()

for division in sorted([d for d in divisiones_principales if isinstance(d, str)]):
    datos_div = df_ultimos_12[df_ultimos_12['Descripcion'] == division].sort_values('Periodo')

    if datos_div['v_m_IPC'].notna().any():
        fig4.add_trace(go.Bar(
            x=datos_div['Periodo'].dt.strftime('%Y-%m'),
            y=datos_div['v_m_IPC'],
            name=division,
            visible=True if division == 'NIVEL GENERAL' else 'legendonly'
        ))

fig4.update_layout(
    title=f'IPC - Variación Mensual Últimos 12 Meses - {args.region}',
    xaxis_title='Período',
    yaxis_title='Variación Mensual (%)',
    barmode='group',
    hovermode='x unified',
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_ultimos_12_meses.html'
fig4.write_html(output_file)
print(f'✓ Gráfico 4 generado: {output_file}')

# Gráfico 5: Heatmap de Variación Mensual por División
print('Generando gráfico 5: Heatmap de Variación Mensual...')

# Filtrar solo divisiones principales para el heatmap (códigos numéricos de máximo 2 dígitos)
df_heatmap = df_region[
    (df_region['Codigo'].str.len() <= 2) &
    (df_region['Codigo'].str.match(r'^\d+$', na=False))
].copy()
pivot_heatmap = df_heatmap.pivot_table(
    values='v_m_IPC',
    index='Descripcion',
    columns='year_month',
    aggfunc='first'
)

# Limitar a últimos 24 meses para mejor visualización
pivot_heatmap = pivot_heatmap.iloc[:, -24:]

fig5 = go.Figure(data=go.Heatmap(
    z=pivot_heatmap.values,
    x=pivot_heatmap.columns,
    y=pivot_heatmap.index,
    colorscale='RdYlGn_r',
    text=pivot_heatmap.values,
    texttemplate='%{text:.1f}%',
    textfont={'size': 8},
    colorbar=dict(title='Var. Mensual (%)')
))

fig5.update_layout(
    title=f'IPC - Mapa de Calor Variación Mensual - {args.region} (Últimos 24 meses)',
    xaxis_title='Período',
    yaxis_title='División',
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_heatmap.html'
fig5.write_html(output_file)
print(f'✓ Gráfico 5 generado: {output_file}')

# Gráfico 6: Acumulación inflacionaria (crecimiento desde base)
print('Generando gráfico 6: Acumulación inflacionaria...')
fig6 = go.Figure()

# Calcular crecimiento porcentual desde la base (dic 2016 = 100)
for division in sorted([d for d in divisiones_principales if isinstance(d, str)]):
    datos_div = df_region[df_region['Descripcion'] == division].sort_values('Periodo')

    if datos_div['Indice_IPC'].notna().any():
        # Crecimiento = ((índice_actual - 100) / 100) * 100
        datos_div = datos_div.copy()
        datos_div['crecimiento_acumulado'] = ((datos_div['Indice_IPC'] - 100) / 100) * 100

        fig6.add_trace(go.Scatter(
            x=datos_div['Periodo'],
            y=datos_div['crecimiento_acumulado'],
            mode='lines',
            name=division,
            line=dict(width=2 if division == 'NIVEL GENERAL' else 1),
            visible=True if division == 'NIVEL GENERAL' else 'legendonly'
        ))

fig6.update_layout(
    title=f'IPC - Inflación Acumulada desde Dic 2016 - {args.region}',
    xaxis_title='Período',
    yaxis_title='Inflación Acumulada (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_{args.region.lower()}_acumulado.html'
fig6.write_html(output_file)
print(f'✓ Gráfico 6 generado: {output_file}')

# Mostrar estadísticas
print('\n' + '=' * 80)
print('ESTADÍSTICAS GENERALES')
print('=' * 80)

nivel_general = df_region[df_region['Descripcion'] == 'NIVEL GENERAL'].sort_values('Periodo')

if len(nivel_general) > 0:
    print(f'\nÍndice actual (NIVEL GENERAL): {nivel_general.iloc[-1]["Indice_IPC"]:.2f}')
    print(f'Variación mensual más reciente: {nivel_general.iloc[-1]["v_m_IPC"]:.2f}%')
    print(f'Variación interanual más reciente: {nivel_general.iloc[-1]["v_i_a_IPC"]:.2f}%')

    # Inflación acumulada
    indice_inicial = nivel_general.iloc[0]['Indice_IPC']
    indice_final = nivel_general.iloc[-1]['Indice_IPC']
    inflacion_acumulada = ((indice_final / indice_inicial) - 1) * 100
    print(f'Inflación acumulada desde {nivel_general.iloc[0]["Periodo"].strftime("%Y-%m")}: {inflacion_acumulada:.2f}%')

print('\n' + '=' * 80)
print('✓ Análisis completado exitosamente!')
print(f'Se generaron 6 archivos HTML con gráficos interactivos en {graficos_dir}/')
print('=' * 80)

# Generar index.html usando Jinja2
print('\nGenerando index.html...')

# Obtener fecha de última actualización de los datos
try:
    datos_timestamp = os.path.getmtime('data/serie_ipc_divisiones.csv')
    fecha_datos = datetime.fromtimestamp(datos_timestamp).strftime('%d/%m/%Y %H:%M:%S')
except:
    fecha_datos = 'No disponible'

# Obtener archivos HTML y preparar datos
html_files = sorted(glob.glob(f'{graficos_dir}/ipc_*.html'))

# Definir descripciones para cada tipo de gráfico
file_descriptions = {
    'indice': 'Evolución del índice de precios por división',
    'variacion_mensual': 'Variación porcentual mensual del IPC',
    'variacion_interanual': 'Variación porcentual interanual del IPC',
    'ultimos_12_meses': 'Comparación de variación mensual en los últimos 12 meses',
    'heatmap': 'Mapa de calor de variación mensual por división',
    'acumulado': 'Inflación acumulada desde diciembre 2016'
}

# Preparar estructura de gráficos
graficos = []
for html_file in html_files:
    basename = os.path.basename(html_file)

    # Extraer tipo de gráfico del nombre del archivo
    titulo = basename.replace('ipc_', '').replace('.html', '').replace('_', ' ').title()

    # Determinar descripción
    desc = 'Gráfico del IPC'
    for key, value in file_descriptions.items():
        if key in basename:
            desc = value
            titulo_map = {
                'indice': 'Evolución del Índice',
                'variacion_mensual': 'Variación Mensual',
                'variacion_interanual': 'Variación Interanual',
                'ultimos_12_meses': 'Últimos 12 Meses',
                'heatmap': 'Mapa de Calor',
                'acumulado': 'Inflación Acumulada'
            }
            titulo = titulo_map.get(key, titulo)
            break

    graficos.append({
        'filename': f'{graficos_dir}/{basename}',
        'title': titulo,
        'description': desc
    })

# Agrupar gráficos (solo un grupo para IPC)
graficos_agrupados = [
    {
        'label': 'Análisis del IPC',
        'graficos': graficos
    }
]

# Cargar template y renderizar
with open('index.jinja', 'r', encoding='utf-8') as f:
    template = Template(f.read())

html_output = template.render(
    fecha_datos=fecha_datos,
    graficos_agrupados=graficos_agrupados,
    region=args.region
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_output)

print('✓ Generado index.html con todos los gráficos disponibles')
