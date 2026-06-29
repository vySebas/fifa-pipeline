import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import duckdb

app = dash.Dash(__name__)

# DISEÑO MAXIMIZADO: Fuentes grandes y contenedor expandido al 95% de la pantalla
ESTILO_PANEL = {
    'fontFamily': 'Segoe UI, Helvetica, Arial, sans-serif',
    'backgroundColor': '#f3f4f6',
    'color': '#111111',
    'padding': '40px',
    'width': '95%',
    'margin': '0 auto'
}

ESTILO_TARJETA = {
    'backgroundColor': '#ffffff',
    'padding': '40px',
    'borderRadius': '16px',
    'boxShadow': '0 4px 20px rgba(0,0,0,0.06)',
    'marginBottom': '35px'
}

app.layout = html.Div(style=ESTILO_PANEL, children=[
    
    # Encabezado Gigante
    html.Div(style={'textAlign': 'center', 'marginBottom': '60px'}, children=[
        html.H1("Rendimiento de Jugadores - FIFA World Cup 2026", style={'fontWeight': '700', 'fontSize': '42px', 'margin': '0 0 15px 0', 'color': '#111111'}),
        html.P("Análisis Multidimensional Interactivo • Operaciones de Roll-up (Global) y Drill-down (Detalle)", style={'color': '#4b5563', 'fontSize': '22px', 'fontWeight': '400'})
    ]),
    
    # Selector de País Enorme
    html.Div(style=ESTILO_TARJETA, children=[
        html.Label("Seleccionar País para aplicar Drill-down (Aumentar Detalle):", style={'fontWeight': '700', 'fontSize': '22px', 'display': 'block', 'marginBottom': '20px', 'color': '#2563eb'}),
        dcc.Dropdown(
            id='filtro-pais',
            placeholder="Escriba o seleccione un país para desglosar estadísticas...",
            style={'width': '100%', 'fontSize': '20px', 'color': '#111111'}
        )
    ]),
    
    # Gráficos en Paralelo Grandes
    html.Div(style={'display': 'flex', 'gap': '30px', 'flexWrap': 'wrap'}, children=[
        html.Div(style={'flex': '1', 'minWidth': '600px'}, children=[
            html.Div(style=ESTILO_TARJETA, children=[
                dcc.Graph(id='grafico-goles', style={'height': '550px'})
            ])
        ]),
        html.Div(style={'flex': '1', 'minWidth': '600px'}, children=[
            html.Div(style=ESTILO_TARJETA, children=[
                dcc.Graph(id='grafico-posiciones', style={'height': '550px'})
            ])
        ])
    ]),
    
    # Gráfico de Eficiencia Inferior
    html.Div(style=ESTILO_TARJETA, children=[
        dcc.Graph(id='grafico-dispersion', style={'height': '600px'})
    ])
])

@app.callback(
    [Output('filtro-pais', 'options'),
     Output('grafico-goles', 'figure'),
     Output('grafico-posiciones', 'figure'),
     Output('grafico-dispersion', 'figure')],
    [Input('filtro-pais', 'value')]
)
def actualizar_dashboard(pais_seleccionado):
    conn = duckdb.connect('data/transformed/fifa.duckdb')
    
    # LEER APUNTANDO DIRECTAMENTE AL ESQUEMA INTERNO DE DBT (main)
    paises = [row[0] for row in conn.execute("SELECT DISTINCT nationality FROM main.stg_players WHERE nationality IS NOT NULL ORDER BY nationality").fetchall()]
    opciones_dropdown = [{'label': p, 'value': p} for p in paises]
    
    if not pais_seleccionado:
        # ==========================================
        # MODO ROLL-UP (Vista de Mayor Jerarquía)
        # ==========================================
        df_goles = conn.execute("SELECT nationality, SUM(goals) as goles FROM main.stg_players GROUP BY nationality ORDER BY goles DESC LIMIT 10").df()
        df_pos = conn.execute("SELECT position, COUNT(player_id) as total FROM main.stg_players GROUP BY position").df()
        df_disp = conn.execute("SELECT nationality, SUM(expected_goals_xg) as xg, SUM(goals) as goles FROM main.stg_players GROUP BY nationality").df()
        
        fig_goles = px.bar(df_goles, x='nationality', y='goles', title='Top 10 Países con Mayor Goleo (Roll-up Global)', template='plotly_white', color_discrete_sequence=['#2563eb'])
        fig_posiciones = px.pie(df_pos, values='total', names='position', title='Distribución Global de Jugadores por Posición', template='plotly_white', color_discrete_sequence=px.colors.qualitative.Set3)
        fig_dispersion = px.scatter(df_disp, x='xg', y='goles', hover_name='nationality', title='Eficiencia Global: Goles Esperados (xG) vs Goles Reales', template='plotly_white', color_discrete_sequence=['#10b981'])
    else:
        # ==========================================
        # MODO DRILL-DOWN (Desglose de Menor Jerarquía)
        # ==========================================
        df_goles = conn.execute("SELECT player_name, goals FROM main.stg_players WHERE nationality = ? ORDER BY goals DESC LIMIT 10", [pais_seleccionado]).df()
        df_pos = conn.execute("SELECT position, COUNT(player_id) as total FROM main.stg_players WHERE nationality = ? GROUP BY position", [pais_seleccionado]).df()
        df_disp = conn.execute("SELECT player_name, expected_goals_xg as xg, goals, position FROM main.stg_players WHERE nationality = ?", [pais_seleccionado]).df()
        
        fig_goles = px.bar(df_goles, x='player_name', y='goals', title=f'Máximos Anotadores: {pais_seleccionado} (Drill-down Individual)', template='plotly_white', color_discrete_sequence=['#f59e0b'])
        fig_posiciones = px.pie(df_pos, values='total', names='position', title=f'Composición Táctica: {pais_seleccionado}', template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_dispersion = px.scatter(df_disp, x='xg', y='goals', color='position', hover_name='player_name', title=f'Rendimiento de Jugadores de {pais_seleccionado} (xG vs Goles)', template='plotly_white')

    conn.close()
    
    # AUMENTO ESCALADO DE FUENTES EN LOS TRES GRÁFICOS
    for fig in [fig_goles, fig_posiciones, fig_dispersion]:
        fig.update_layout(
            font_family="Segoe UI, Helvetica, Arial, sans-serif",
            font_size=16,            # Letras de los ejes más grandes
            title_font_size=22,      # Títulos de gráficos imponentes
            title_font_color="#111111",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=60, b=40)
        )
    return opciones_dropdown, fig_goles, fig_posiciones, fig_dispersion

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=False)
