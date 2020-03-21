import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
# Adds html elements
import dash_html_components as html

dash_app = dash.Dash()

# actual graph itself
dash_app.layout = html.Div(children=[
    # input field in html field
    dcc.Input(id='input', value='Enter Value', type='text'),
    # oupput field in html field
    html.Div(id='output'),
    html.Div(children=[
        html.H1("hey"),
        html.P("This is a paragraph")
        ]),
    html.H1("Hey Outer")
])

# action triggered by input 
@dash_app.callback(
    Output(component_id='output', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    return "Input: {}".format(input_data)

if __name__ == "__main__":
    dash_app.run_server(debug=True)
