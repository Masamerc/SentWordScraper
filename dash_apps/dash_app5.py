#! env/bin/python3.7.1

"""
Dash Part 5: Live-graph with Dash, Deque and Plotly Grapgh Objects + External Javascript & CSS

Ref: https://pythonprogramming.net/vehicle-data-visualization-application-dash-python-tutorial/

"""
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import random
import time
from collections import deque
import pandas as pd
import pandas_datareader.data 

# external_stylesheets = ["https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"]
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]


external_scripts = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js']


dash_app = dash.Dash("vehicle-data", external_scripts=external_scripts, external_stylesheets=external_stylesheets)

max_len = 20
times = deque(maxlen=max_len)
oil_temps = deque(maxlen=max_len)
intake_temps = deque(maxlen=max_len)
coolant_temps = deque(maxlen=max_len)
rpms = deque(maxlen=max_len)
speeds = deque(maxlen=max_len)
throttle_pos = deque(maxlen=max_len)

data_dict = {
    "Oil Temprature": oil_temps,
    "Intake Temprature": intake_temps,
    "Coolant Temprature": coolant_temps,
    "RMP": rpms,
    "Speed": speeds,
    "Throttle Position": throttle_pos 
}

def update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos):

    times.append(time.time())
    if len(times) == 1:
        #starting relevant values
        oil_temps.append(random.randrange(180,230))
        intake_temps.append(random.randrange(95,115))
        coolant_temps.append(random.randrange(170,220))
        rpms.append(random.randrange(1000,9500))
        speeds.append(random.randrange(30,140))
        throttle_pos.append(random.randrange(10,90))
    else:
        for data_of_interest in [oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))

    return times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos

times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos = update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)


dash_app.layout = html.Div([
    html.Div([
        html.H2('Vehicle Data', style={'fload': 'left'})
    ]),
    dcc.Dropdown(
        id='vehicle-name-dropdown',
        options=[{'label': s, 'value': s} for s in data_dict.keys()],
        value=['Coolant Temprature', 'Oil Temprature', 'Intake Temprature'],
        multi=True),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id='graph-update',
        interval=5000
    )
]
, className="container", style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000})


@dash_app.callback(
    Output('graphs', 'children'),
    [Input('vehicle-name-dropdown', 'value'), Input('graph-update', 'n_intervals')]
)
def update_graph(data_names, n):
    graphs = []
    update_obd_values(times, oil_temps, intake_temps, coolant_temps, rpms, speeds, throttle_pos)
    # global times
    # global oil_temps
    # global intake_temps
    # global coolant_temps
    # global rpms
    # global speeds
    # global throttle_pos

    # materialzed css's grid system
    if len(data_names) > 2:
        class_choice = 'col s12 m6 14'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 16'
    else:
        class_choice = 'col s12'

    for data_name in data_names:

        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill='tozeroy',
            fillcolor='lightcyan'
        )
        
        graphs.append(html.Div(
            dcc.Graph(
                id=data_name,
                animate=True,
                figure={
                    'data': [data],
                    'layout': go.Layout(
                        xaxis=dict(range=[min(times), max(times)]),
                        yaxis=dict(range=[min(data_dict[data_name]), max(data_dict[data_name])]),
                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                        title='{}'.format(data_name)

                        )
                    }
                ),  className=class_choice))

    return graphs

if __name__ == "__main__":
    dash_app.run_server()