from bokeh.plotting import figure, output_file, show

x = range(1, 6)
y = [4, 5, 6, 7, 8]

output_file("index.html")

p = figure(
    title="example plot",
    x_axis_label='X',
    y_axis_label='Y',
)

p.line(x, y, legend="test", line_width=2)

show(p)