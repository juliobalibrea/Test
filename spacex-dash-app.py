# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Componente visual del gráfico de pastel
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Componente visual del gráfico de dispersión
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ----------------------------------------------------------------------------------
# CALLBACKS (Siempre van FUERA del app.layout)
# ----------------------------------------------------------------------------------

# TASK 2 Callback: Dropdown -> Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, 
                     values='class', 
                     names='Launch Site', 
                     title='Total Success Launches By Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        df_site = filtered_df.groupby('class').size().reset_index(name='counts')
        fig = px.pie(df_site, 
                     values='counts', 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
        return fig

# TASK 4 Callback: Dropdown + RangeSlider -> Scatter Chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, payload_range):
    # Desempaquetar los valores minimo y maximo del slider
    low, high = payload_range
    
    # Filtrar el dataframe completo según el rango del payload
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    filtered_df = spacex_df[mask]
    
    if entered_site == 'ALL':
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', 
            color='Booster Version Category',
            title='Correlation between Payload and Success for all Sites'
        )
        return fig
    else:
        # Filtrar aún más para obtener solo el sitio seleccionado
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(
            filtered_df, x='Payload Mass (kg)', y='class', 
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {entered_site}'
        )
        return fig

# Run the app
if __name__ == '__main__':
    app.run(port = 8051)