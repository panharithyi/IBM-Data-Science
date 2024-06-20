# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
def build_options(data_frame_series, add_all=False):
    option_list = [{'label': i, 'value': i} for i in data_frame_series.unique()]
    if add_all:
        option_list.insert(0, {'label': 'All Sites', 'value': 'ALL'})
    return option_list

# Create a dash application
app = dash.Dash(__name__)


# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options=build_options(launch_sites_df['Launch Site'], add_all=True),
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        print('block pie with all sites executed')
        suc_launch = filtered_df[filtered_df['class'] == 1]
        exp_rec= suc_launch.groupby('Launch Site')['class'].count().reset_index()

        fig = px.pie(exp_rec, values='class', 
        names=exp_rec['Launch Site'].unique(), 
        title='Total Success launches by site')

        return fig  

    else:
        print('block pie with particular site executed')
        suc_fail_launch_by_site = filtered_df[filtered_df['Launch Site'] == entered_site]
        exp_rec_by_site = suc_fail_launch_by_site.groupby(['Launch Site','class'],as_index= False)['class'].count()
        
        fig = px.pie(exp_rec_by_site, values='class', 
        names=exp_rec_by_site.index, 
        title='Total Success launches by site ' + entered_site)

        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, payload_value):


    if entered_site == 'ALL':
        print('block scatter with all sites executed')
        suc_fail_launch_by_site = spacex_df[(spacex_df['Payload Mass (kg)'] > payload_value[0]) & (spacex_df['Payload Mass (kg)'] < payload_value[1])]
        fig = px.scatter(suc_fail_launch_by_site, x="Payload Mass (kg)", y="class",
                        color="Booster Version Category")
        return fig
    else:
        print('block scatter with particular site executed')
        suc_fail_launch_by_site = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'] > payload_value[0]) & (spacex_df['Payload Mass (kg)'] < payload_value[1])]
        fig = px.scatter(suc_fail_launch_by_site, x="Payload Mass (kg)", y="class",
                        color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
