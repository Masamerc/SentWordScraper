#! env/bin/python3.7.1

"""
Dash Part 3: Live-graph with Dash, Deque and Plotly Grapgh Objects

Key Takeaways:
- Working with Input / Output
- Working with plotly grapgh objects 
"""
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import random
from collections import deque


X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)


dash_app = dash.Dash(__name__)

dash_app.layout = html.Div(children=[
    # Grapgh component
    dcc.Graph(
        id='live-graph',
        animate=True
    ),
    # Interval for live-update
    dcc.Interval(
        id='graph-update',
        # in mili-seconds
        interval=1000
    )
])

# 1st arg of Output: where do you want the output 2nd: what do you want as output
@dash_app.callback(
    Output('live-graph', 'figure'),
    [Input("graph-update", "n_intervals")]
    )
def update_graph(n):
    X.append(X[-1] + 1)
    Y.append(Y[-1] + (Y[-1]*random.uniform(-0.1, 0.1)))

    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name = 'Scatter',
        mode = 'lines+markers'
    )

    return {'data': [data], 'layout': go.Layout(
        xaxis=dict(range=[min(X), max(X)]),
        yaxis=dict(range=[min(Y), max(Y)])
    )}


if __name__ == "__main__":
    dash_app.run_server()
