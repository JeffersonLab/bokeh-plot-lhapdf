import lhapdf
lhapdf.version()

lhapdf.setPaths(["/home/wdconinc/.local/share/lhapdf"])

p = {}
menu = []
for n in lhapdf.availablePDFSets():
    p[n] = lhapdf.mkPDF(n)
    menu.append((n,n))

import numpy as np
from ipywidgets import interact, fixed

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Slider, Dropdown, MultiSelect
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import push_notebook, show, output_notebook
from bokeh.plotting import figure

x = np.logspace(-6, 0, 100)
y = [p["CT10"].xfxQ2(1, x, 0.1) for x in x]

plot = []
line = []
panels = []

for i,axis_type in enumerate(["linear", "log"]):
    plot.append(figure(title = "parton distribution function",
                 plot_height = 400, plot_width = 600,
                 tools = "crosshair,pan,reset,save,wheel_zoom",
                 x_axis_type = "log", y_axis_type = axis_type,
                 background_fill_color = '#efefef'))
    plot[i].xaxis.axis_label = "x"
    plot[i].yaxis.axis_label = "f(x)"
    line.append(plot[i].line(x, y, color = "#8888cc", line_width = 1.5, alpha = 0.8))
    panels.append(Panel(child = plot[i], title = axis_type))

pdfset_dropdown = Dropdown(
    label = "PDF set ",
    value = "CT10",
    menu = menu,
)
parton_dropdown = Dropdown(
    label = "Parton: ",
    value = "u",
    menu = [("g","g"), ("u","u"), ("d","d"), ("s","s")],
)
Q2_slider = Slider(
    title = "Q²",
    value = 0.1,
    start = 0.01, end = 10.0, step = 0.01,
)


def update(attrname, old, new):
    pdfset = pdfset_dropdown.value
    parton = parton_dropdown.value
    Q2 = Q2_slider.value

    if parton == "g": pid = 21
    if pdfset[0] == "J":
      if   parton == "u": pid = 901
      elif parton == "d": pid = 902
      elif parton == "s": pid = 903
    else:
      if   parton == "u": pid = 1
      elif parton == "d": pid = 2
      elif parton == "s": pid = 3

    for l in line:
        l.data_source.data['y'] = [p[pdfset].xfxQ2(pid, x, Q2) for x in x]


for w in [pdfset_dropdown, parton_dropdown, Q2_slider]:
    w.on_change('value', update)

inputs = column(pdfset_dropdown, parton_dropdown, Q2_slider)
tabs = Tabs(tabs = panels)

curdoc().add_root(column(tabs, inputs, width=800))
curdoc().title = "LHAPDF Bokeh"
