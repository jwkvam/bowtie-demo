#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie import App, command
from bowtie.control import Dropdown, Slider
from bowtie.visual import Plotly, Table
from bowtie.html import Markdown, Header

import numpy as np
import pandas as pd
import plotlywrapper as pw

from sklearn.kernel_ridge import KernelRidge

iris = pd.read_csv('./iris.csv')
iris = iris.drop(iris.columns[0], axis=1)

attrs = iris.columns[:-1]

app = App(rows=2, columns=3, sidebar=True, background_color='PaleTurquoise', debug=True)

description = Markdown("""Bowtie Demo
===========

Demonstrates interactive elements with the iris dataset.
Select some attributes to plot and select some data on the 2d plot.
Change the alpha parameter to see how that affects the model.
""")

xdown = Dropdown(labels=attrs, values=attrs)
ydown = Dropdown(labels=attrs, values=attrs)
zdown = Dropdown(labels=attrs, values=attrs)
alphaslider = Slider(start=10, minimum=1, maximum=50)

mainplot = Plotly()
mplot3 = Plotly()
linear = Plotly()
table1 = Table()

app.columns[0].fraction(2)
app.columns[1].fraction(1)
app.columns[2].fraction(1)

app.add_sidebar(description)
app.add_sidebar(Header('X Variable', size=3))
app.add_sidebar(xdown)
app.add_sidebar(Header('Y Variable', size=3))
app.add_sidebar(ydown)
app.add_sidebar(Header('Z Variable', size=3))
app.add_sidebar(zdown)
app.add_sidebar(Header('Alpha Parameter', size=3))
app.add_sidebar(alphaslider)

app[0, 0] = mainplot
app[0, 1:] = mplot3
app[1, :2] = linear
app[1, 2] = table1


@app.subscribe(xdown.on_change, ydown.on_change)
def pairplot(x, y):
    if x is None or y is None:
        return
    x = x['value']
    y = y['value']
    plot = pw.Chart()
    for i, df in iris.groupby('Species'):
        plot += pw.scatter(df[x], df[y], label=i)
    plot.xlabel = x
    plot.ylabel = y
    mainplot.do_all(plot.dict)


@app.subscribe(xdown.on_change, ydown.on_change, zdown.on_change)
def threeplot(x, y, z):
    if x is None or y is None or z is None:
        return
    x = x['value']
    y = y['value']
    z = z['value']
    plot = pw.Chart()
    for i, df in iris.groupby('Species'):
        plot += pw.scatter3d(df[x], df[y], df[z], label=i)
    plot.xlabel = x
    plot.ylabel = y
    mplot3.do_all(plot.dict)


@app.subscribe(mainplot.on_select, alphaslider.on_change)
def mainregress(selection, alpha):
    if len(selection) < 2:
        return

    x = xdown.get()['value']
    y = ydown.get()['value']

    tabdata = []
    mldatax = []
    mldatay = []
    species = iris.Species.unique()
    for i, p in enumerate(selection['points']):
        mldatax.append(p['x'])
        mldatay.append(p['y'])
        tabdata.append({
            x: p['x'],
            y: p['y'],
            'species': species[p['curve']]
        })


    X = np.c_[mldatax, np.array(mldatax) ** 2]
    ridge = KernelRidge(alpha=alpha).fit(X, mldatay)

    xspace = np.linspace(min(mldatax)-1, max(mldatax)+1, 100)

    plot = pw.scatter(mldatax, mldatay, label='train', markersize=15)
    for i, df in iris.groupby('Species'):
        plot += pw.scatter(df[x], df[y], label=i)
    plot += pw.line(xspace, ridge.predict(np.c_[xspace, xspace**2]), label='model', mode='lines')
    plot.xlabel = x
    plot.ylabel = y
    linear.do_all(plot.dict)
    table1.do_data(pd.DataFrame(tabdata))


@command
def main():
    return app
