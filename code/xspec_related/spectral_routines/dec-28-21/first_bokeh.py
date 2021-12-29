import pandas as pd
import numpy as np
from random import random
from numpy.random import randn

from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, CustomJS, Range1d, Button
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
import os

import numpy as np
from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, CustomJS
from bokeh.layouts import column

slider_slope = Slider(title = 'Slope', start = 0, end = 1, value = 0.5, step = 0.1)
slider_intercept = Slider(title = 'Intercept', start = 0, end = 20, value = 10, step = 1)

s = slider_slope.value  # slope.
i = slider_intercept.value  # intercept.

x = np.linspace(-40, 20, 200)
y = [(s * xx + i) for xx in x]

p = figure(title = "simple line example", plot_height = 500, plot_width = 600, y_range = Range1d(start = -80, end = 40), background_fill_color = '#efefef')
r = p.line(x, y, color = "red", line_width = 1.5, alpha = 0.8)  # 1st line. This line can be controlled by sliders.
q = p.line(x, 2 * x + 1.2, color = "blue", line_width = 1.9, alpha = 0.2)  # 2nd line.

def update(attr, old, new):
    s = slider_slope.value  # slope.
    i = slider_intercept.value  # intercept
    x = r.data_source.data['x'];
    y = []

    for value in x:
        y.append((s * value) + i)

    r.data_source.data['y'] = y

slider_slope.on_change('value', update)
slider_intercept.on_change('value', update)

layout = column(p, slider_slope, slider_intercept)
curdoc().add_root(layout)

show(layout, notebook_handle = True) # Launch the chart in the web browser.
