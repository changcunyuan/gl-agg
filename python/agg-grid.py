#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

size = 512,512
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=True)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

major_grid = np.array([64.,64.])
minor_grid = np.array([64.,64.])/5.0

axes.xaxis.set_major_locator(MultipleLocator(major_grid[0]))
axes.xaxis.set_minor_locator(MultipleLocator(minor_grid[0]))
axes.yaxis.set_major_locator(MultipleLocator(major_grid[1]))
axes.yaxis.set_minor_locator(MultipleLocator(minor_grid[1]))
axes.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
axes.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
axes.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
axes.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')

fig.savefig('agg-grid.png', dpi=dpi)
plt.show()
