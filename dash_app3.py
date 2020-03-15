import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output
# Adds html elements
import dash_html_components as html

import pandas_datareader.data as web
from datetime import datetime, date
from dateutil.relativedelta import relativedelta 


# Initialize app
dash_app = dash.Dash()

# actual graph itself
dash_app.layout = html.Div(children=[
    html.H3("Type the name of company: "),
    # input field in html field
    dcc.Input(id='input', value='', type='text'),
    # oupput field in html field
    html.Div(id='output-graph')
    
])


# action triggered by input 
@dash_app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(input_data):
    # getting today's date and date five years ago
    end = date.today()
    start = end - relativedelta(years=3)

    # load stock data 
    tick_name = input_data
    df = web.DataReader(tick_name, 'yahoo', start, end)

    print(f"Pulled data for '{tick_name}. Graphing...'")

    return dcc.Graph(
        id="stock-close-price",
        figure={
            'data': [{
                'x': df.index, 'y':df['Close'], 'type': 'line', 'name': tick_name
            }],
            'layout': {
                'title': tick_name
            }
        }
    )


if __name__ == "__main__":
    dash_app.run_server(debug=True)
    # print(df.tail())
    # print(df.head())