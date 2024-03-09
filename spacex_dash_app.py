# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

spacex_df['class'] = pd.to_numeric(spacex_df['class'], errors='coerce')
spacex_df['Payload Mass (kg)'] = pd.to_numeric(spacex_df['Payload Mass (kg)'], errors='coerce')

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value='ALL',  # Default. # The default select value is for ALL sites
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),                                
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')), 
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=2500,
                                                marks={0: '0',
                                                       2500: '2500',
                                                       5000: '5000',
                                                       7500: '7500',
                                                       10000: '10000'},
                                                value=[min_payload, max_payload]),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                    Input(component_id='site-dropdown', component_property='value')
                    )
def get_pie_chart(entered_site):
                    filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
                    success_count = filtered_df[filtered_df['class'] == 1].shape[0]
                    failed_count = filtered_df[filtered_df['class'] == 0].shape[0]

                    if entered_site == 'ALL':
                        fig = px.pie(spacex_df, values='class', 
                                        names='Launch Site', 
                                        title='Lacun Sucess Rate')
                        return fig
                    else:

                        fig2 = px.pie(names=['Success', 'Failed'], 
                                        values=[success_count, failed_count], 
                                        title='Launch Success Rate - ' + entered_site)
                        return fig2


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
             )
def get_scatter_chart(entered_site, payload_range):
                    if entered_site == 'ALL':
                        filtered_df3 = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
                        fig3 = px.scatter(filtered_df3, 
                                        x='Payload Mass (kg)', 
                                        y='class', 
                                        color='Booster Version Category', 
                                        title='Scatter Plot - All Sites')
                        return fig3
                    else:
                        filtered_df4 = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
                        fig4 = px.scatter(filtered_df2,
                                         x='Payload Mass (kg)',
                                         y='class', 
                                         color='Booster Version Category', 
                                         title=f'Scatter Plot - {entered_site}')
                        return fig4



# Run the app
if __name__ == '__main__':
    app.run_server()
