import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from bokeh.plotting import figure, show, curdoc
from bokeh.models import Slider, CustomJS, Range1d, Button
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
import os

df = pd.read_csv('/home/thaddaeus/GitHub/MAXI-J1535/code/xspec_related/spectral_routines/dec-28-21/results.csv')

red_pgs = np.array(df['red_pgs'])

slider_cutoff = Slider(title = 'Max. Redudced pg-stat', start = 2, end = 15, value = 2, step = 0.25)

s = slider_cutoff.value  # max cutoff

p = figure(title = "simple test example", plot_height = 500, plot_width = 600, background_fill_color = '#efefef')

hist, edges = np.histogram(red_pgs, density=True, bins=15)

p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], line_color="white")

def update(attr, old, new):
    cutoff_value = slider_cutoff.value  # slope.
    x = hist.data_source.data['x'];
    y = []

    for value in x:
        if value < cutoff_value: 
            y.append(value)

    hist.data_source.data['x'] = y

slider_cutoff.on_change('value', update)

layout = column(p, slider_cutoff)
curdoc().add_root(layout)

show(layout, notebook_handle = True) # Launch the chart in the web browser.