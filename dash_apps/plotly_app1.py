'''
Generate HTML and DIV
'''

import plotly.graph_objects as go
from plotly.offline import plot
from plotly.plotly import plot as online_plot
fig = go.Figure(data=go.Bar(y=[2, 3, 1]))

plot(fig, filename="test.html", auto_open=False)

url = online_plot(fig, filename="Test", auto_open=True)
print(url)