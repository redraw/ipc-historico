#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#   "pandas",
#   "plotly",
# ]
# ///
"""
Script para comparar el IPC entre diferentes regiones
Genera gráficos comparativos usando pandas y plotly
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

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

# Filtrar solo NIVEL GENERAL
df_nivel_general = df[df['Descripcion'] == 'NIVEL GENERAL'].copy()

print('=' * 80)
print('COMPARACIÓN DEL IPC ENTRE REGIONES')
print('=' * 80)
print(f'\nRegiones disponibles: {", ".join(sorted(df_nivel_general["Region"].unique()))}')
print(f'Períodos analizados: {df_nivel_general["Periodo"].min().strftime("%Y-%m")} - {df_nivel_general["Periodo"].max().strftime("%Y-%m")}')

# Gráfico 1: Evolución del Índice - Comparación entre Regiones
print('\nGenerando gráfico 1: Evolución del Índice por Región...')
fig1 = go.Figure()

regiones = sorted(df_nivel_general['Region'].unique())
colores = px.colors.qualitative.Set2

for idx, region in enumerate(regiones):
    datos_region = df_nivel_general[df_nivel_general['Region'] == region].sort_values('Periodo')

    fig1.add_trace(go.Scatter(
        x=datos_region['Periodo'],
        y=datos_region['Indice_IPC'],
        mode='lines',
        name=region,
        line=dict(width=3 if region == 'Nacional' else 2),
        visible=True if region in ['Nacional', 'GBA'] else 'legendonly'
    ))

fig1.update_layout(
    title='IPC - Comparación del Índice entre Regiones',
    xaxis_title='Período',
    yaxis_title='Índice (Base Dic 2016 = 100)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_indice.html'
fig1.write_html(output_file)
print(f'✓ Gráfico 1 generado: {output_file}')

# Gráfico 2: Variación Mensual - Comparación entre Regiones
print('Generando gráfico 2: Variación Mensual por Región...')
fig2 = go.Figure()

for idx, region in enumerate(regiones):
    datos_region = df_nivel_general[df_nivel_general['Region'] == region].sort_values('Periodo')

    fig2.add_trace(go.Scatter(
        x=datos_region['Periodo'],
        y=datos_region['v_m_IPC'],
        mode='lines',
        name=region,
        line=dict(width=3 if region == 'Nacional' else 2),
        visible=True if region in ['Nacional', 'GBA'] else 'legendonly'
    ))

fig2.update_layout(
    title='IPC - Comparación de Variación Mensual entre Regiones',
    xaxis_title='Período',
    yaxis_title='Variación Mensual (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_variacion_mensual.html'
fig2.write_html(output_file)
print(f'✓ Gráfico 2 generado: {output_file}')

# Gráfico 3: Variación Interanual - Comparación entre Regiones
print('Generando gráfico 3: Variación Interanual por Región...')
fig3 = go.Figure()

for idx, region in enumerate(regiones):
    datos_region = df_nivel_general[df_nivel_general['Region'] == region].sort_values('Periodo')

    fig3.add_trace(go.Scatter(
        x=datos_region['Periodo'],
        y=datos_region['v_i_a_IPC'],
        mode='lines',
        name=region,
        line=dict(width=3 if region == 'Nacional' else 2),
        visible=True if region in ['Nacional', 'GBA'] else 'legendonly'
    ))

fig3.update_layout(
    title='IPC - Comparación de Variación Interanual entre Regiones',
    xaxis_title='Período',
    yaxis_title='Variación Interanual (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_variacion_interanual.html'
fig3.write_html(output_file)
print(f'✓ Gráfico 3 generado: {output_file}')

# Gráfico 4: Inflación Acumulada - Comparación entre Regiones
print('Generando gráfico 4: Inflación Acumulada por Región...')
fig4 = go.Figure()

for idx, region in enumerate(regiones):
    datos_region = df_nivel_general[df_nivel_general['Region'] == region].sort_values('Periodo')

    # Calcular inflación acumulada desde la base
    datos_region = datos_region.copy()
    datos_region['inflacion_acumulada'] = ((datos_region['Indice_IPC'] - 100) / 100) * 100

    fig4.add_trace(go.Scatter(
        x=datos_region['Periodo'],
        y=datos_region['inflacion_acumulada'],
        mode='lines',
        name=region,
        line=dict(width=3 if region == 'Nacional' else 2),
        visible=True if region in ['Nacional', 'GBA'] else 'legendonly'
    ))

fig4.update_layout(
    title='IPC - Comparación de Inflación Acumulada entre Regiones',
    xaxis_title='Período',
    yaxis_title='Inflación Acumulada desde Dic 2016 (%)',
    hovermode='x unified',
    legend=dict(yanchor='top', y=0.99, xanchor='left', x=0.01),
    height=600,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_acumulado.html'
fig4.write_html(output_file)
print(f'✓ Gráfico 4 generado: {output_file}')

# Gráfico 5: Ranking de Inflación por Región (últimos 12 meses)
print('Generando gráfico 5: Ranking de Inflación por Región...')

# Obtener últimos 12 meses
fecha_max = df_nivel_general['Periodo'].max()
fecha_inicio = fecha_max - pd.DateOffset(months=11)
df_ultimos_12 = df_nivel_general[df_nivel_general['Periodo'] >= fecha_inicio].copy()

# Calcular inflación acumulada en los últimos 12 meses
inflacion_por_region = []
for region in regiones:
    datos = df_ultimos_12[df_ultimos_12['Region'] == region].sort_values('Periodo')
    if len(datos) >= 2:
        indice_inicial = datos.iloc[0]['Indice_IPC']
        indice_final = datos.iloc[-1]['Indice_IPC']
        inflacion = ((indice_final / indice_inicial) - 1) * 100
        inflacion_por_region.append({'Region': region, 'Inflacion_12m': inflacion})

df_ranking = pd.DataFrame(inflacion_por_region).sort_values('Inflacion_12m', ascending=True)

fig5 = go.Figure(go.Bar(
    x=df_ranking['Inflacion_12m'],
    y=df_ranking['Region'],
    orientation='h',
    text=[f'{val:.1f}%' for val in df_ranking['Inflacion_12m']],
    textposition='outside',
    marker_color='steelblue'
))

fig5.update_layout(
    title='IPC - Ranking de Inflación por Región (Últimos 12 meses)',
    xaxis_title='Inflación Acumulada 12 meses (%)',
    yaxis_title='Región',
    height=500,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_ranking.html'
fig5.write_html(output_file)
print(f'✓ Gráfico 5 generado: {output_file}')

# Gráfico 6: Heatmap de Variación Mensual por Región (últimos 24 meses)
print('Generando gráfico 6: Heatmap de Variación Mensual por Región...')

# Obtener últimos 24 meses
fecha_inicio_24 = fecha_max - pd.DateOffset(months=23)
df_ultimos_24 = df_nivel_general[df_nivel_general['Periodo'] >= fecha_inicio_24].copy()

# Crear pivot table
pivot_heatmap = df_ultimos_24.pivot_table(
    values='v_m_IPC',
    index='Region',
    columns='year_month',
    aggfunc='first'
)

fig6 = go.Figure(data=go.Heatmap(
    z=pivot_heatmap.values,
    x=pivot_heatmap.columns,
    y=pivot_heatmap.index,
    colorscale='RdYlGn_r',
    text=pivot_heatmap.values,
    texttemplate='%{text:.1f}%',
    textfont={'size': 9},
    colorbar=dict(title='Var. Mensual (%)')
))

fig6.update_layout(
    title='IPC - Mapa de Calor Variación Mensual por Región (Últimos 24 meses)',
    xaxis_title='Período',
    yaxis_title='Región',
    height=500,
    template='plotly_white'
)

output_file = f'{graficos_dir}/ipc_comparacion_heatmap.html'
fig6.write_html(output_file)
print(f'✓ Gráfico 6 generado: {output_file}')

# Mostrar estadísticas comparativas
print('\n' + '=' * 80)
print('ESTADÍSTICAS COMPARATIVAS (Octubre 2025)')
print('=' * 80)

datos_actuales = df_nivel_general[df_nivel_general['Periodo'] == fecha_max].sort_values('Indice_IPC', ascending=False)

print('\nÍndice Actual por Región:')
for _, row in datos_actuales.iterrows():
    print(f"  {row['Region']:12s}: Índice {row['Indice_IPC']:8.2f} | Var.Mensual {row['v_m_IPC']:5.2f}% | Var.Interanual {row['v_i_a_IPC']:5.2f}%")

print('\n' + '=' * 80)
print('✓ Análisis comparativo completado exitosamente!')
print(f'Se generaron 6 archivos HTML con gráficos comparativos en {graficos_dir}/')
print('=' * 80)
