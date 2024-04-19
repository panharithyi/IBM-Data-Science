import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output


# read data airline carriers into the pandas dataframe

airline_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                            encoding = 'ISO-8859-1',
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# print(type(airline_data))
# print(airline_data.head())

# create dash application and get the layout
app = dash.Dash(__name__)

# skeleton layout
    # Get the layout of the application and adjust it.
    # Create an outer division using html.Div and add title to the dashboard using html.H1 component
    # Add a html.Div and core input text component
    # Finally, add graph component.


app.layout = html.Div([html.H1('Total number of flights to the destination state split by reporting airline',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 50}),
                    html.Div(["Input Year", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size':35}),], style={'font-size':40}),
                    html.Br(),
                    html.Br(),
                    html.Div(dcc.Graph(id='bar-plot')),
                    ])

# add callback decorator
@app.callback(Output(component_id='bar-plot', component_property='figure'),
                Input(component_id='input-year', component_property='value'))

# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    fig = px.bar(bar_data, x= "DestState", y= "Flights", title='Total number of flights to the destination state split by reporting airline') 
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()