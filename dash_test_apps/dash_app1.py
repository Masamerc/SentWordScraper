import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
# Adds html elements
import dash_html_components as html

external_stylesheets = ["/static/style.css"]
dash_app = dash.Dash(external_stylesheets=external_stylesheets)


# actual graph itself
dash_app.layout = html.Div(children=[
    html.H1("Dash Right Here"),
    dcc.Graph(id='example',
    figure = {
        'data': [
            {'x': [1, 2, 3, 4, 5], 'y': [11, 12, 13 ,21, 11], 'type': 'line', 'name': 'boats'},
            {'x': [1, 2, 3, 4, 5], 'y': [11, 12, 13 ,21, 11], 'type': 'bar', 'name': 'cars'}
            ],
        'layout': {
            'title': 'Basic Dash Example'
        }
    }, style={
        "backgroundColor":"black"
    })
]) 


if __name__ == "__main__":
    dash_app.run_server(debug=True)
