from bokeh.plotting import figure, output_file, show, save, ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Greens8
from bokeh.models.tools import HoverTool
from bokeh.embed import components
import pandas as pd

output_file('index_test.html')


# Loading data
df = pd.read_csv('cars.csv')
source=ColumnDataSource(df)
car_list = source.data["Car"].tolist()


p = figure(
    title="Cars - Price",
    y_axis_label='Price',
    plot_width=1000,
    plot_height=600,
    tools="pan,zoom_in,zoom_out,reset,box_select",
    y_range=car_list)


p.hbar(
    y='Car',
    right='Horsepower',
    left=0,
    height=0.4,
    fill_color=factor_cmap(
        'Car',
        palette=Greens8,
        factors=car_list
    ),
    fill_alpha=0.7,
    source=source,
    legend_group='Car'
)


# add tooltip
hover = HoverTool()

hover.tooltips = """
<div>
    <h3>@Car</h3>
    <div><strong>Price: </strong>@Price</div>
    <br>
    <div><strong>Horsepower: </strong>@Horsepower</div>
</div
"""


p.add_tools(hover)

# show result
# show(p)

# save file
save(p)

# Print out div and script
script, div = components(p)
print(div)
print(script)