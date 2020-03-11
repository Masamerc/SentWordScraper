import dash
import dash_core_components as dcc

# Adds html elements
import dash_html_components as html

dash_app = dash.Dash()

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
    })

    
    ]) 


if __name__ == "__main__":
    dash_app.run_server(debug=True)
