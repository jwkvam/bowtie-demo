#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bowtie.control import DropDown, Slider
from bowtie.visual import Plotly, SmartGrid

import numpy as np
import pandas as pd
import plotlywrapper as pw

from sklearn.kernel_ridge import KernelRidge

iris = pd.read_csv('./iris.csv')
iris = iris.drop(iris.columns[0], axis=1)

attrs = iris.columns[:-1]

xdown = DropDown(caption='X variable', labels=attrs, values=attrs)
ydown = DropDown(caption='Y variable', labels=attrs, values=attrs)
zdown = DropDown(caption='Z variable', labels=attrs, values=attrs)
alphaslider = Slider(caption='alpha parameter', start=10, minimum=1, maximum=50)

mainplot = Plotly()
mplot3 = Plotly()
linear = Plotly()
table1 = SmartGrid()


def pairplot(x, y):
    print('hellox')
    if x is None or y is None:
        return
    x = x['value']
    y = y['value']
    plot = pw.Chart()
    for i, df in iris.groupby('Species'):
        plot += pw.scatter(df[x], df[y], label=i)
    plot.xlabel(x)
    plot.ylabel(y)
    mainplot.do_all(plot.to_json())


def threeplot(x, y, z):
    if x is None or y is None or z is None:
        return
    x = x['value']
    y = y['value']
    z = z['value']
    plot = pw.Chart()
    for i, df in iris.groupby('Species'):
        plot += pw.scatter3d(df[x], df[y], df[z], label=i)
    plot.xlabel(x)
    plot.ylabel(y)
    plot.zlabel(z)
    mplot3.do_all(plot.to_json())


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
            'species': species[p['curveNumber']]
        })


    X = np.c_[mldatax, np.array(mldatax) ** 2]
    ridge = KernelRidge(alpha=alpha).fit(X, mldatay)

    xspace = np.linspace(min(mldatax)-1, max(mldatax)+1, 100)

    plot = pw.scatter(mldatax, mldatay, label='train', markersize=15)
    for i, df in iris.groupby('Species'):
        plot += pw.scatter(df[x], df[y], label=i)
    plot += pw.line(xspace, ridge.predict(np.c_[xspace, xspace**2]), label='model', mode='lines')
    plot.xlabel(x)
    plot.ylabel(y)
    linear.do_all(plot.to_json())
    table1.do_update(tabdata)


from bowtie import command

@command
def construct(path):
    from bowtie import Layout
    description = """
Bowtie Demo
===========

Demonstrates interactive elements with the iris dataset.
Select some attributes to plot and select some data on the 2d plot.
Change the alpha parameter to see how that affects the model.
"""
    layout = Layout(description=description, background_color='PaleTurquoise', debug=False)
    layout.add_controller(xdown)
    layout.add_controller(ydown)
    layout.add_controller(zdown)
    layout.add_controller(alphaslider)
    layout.add_visual(mainplot)
    layout.add_visual(mplot3)
    layout.add_visual(linear, next_row=True)
    layout.add_visual(table1)

    layout.subscribe(pairplot, xdown.on_change, ydown.on_change)
    layout.subscribe(threeplot, xdown.on_change, ydown.on_change, zdown.on_change)
    layout.subscribe(mainregress, mainplot.on_select, alphaslider.on_change)

    layout.build()
