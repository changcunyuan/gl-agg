#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects

size = 512,512
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

radius = 255.0
theta = 0
dtheta = 5.5/180.0*math.pi
for i in range(500):
    theta += dtheta
    x = 256+radius*math.cos(theta);
    y = 256+radius*math.sin(theta);
    r = 10.1-i*0.02;
    radius -= 0.45
    patch = patches.Circle((x,y), r, lw=1.0, color='None', ec='k', fc='None')
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-circles-2.png', dpi=dpi)
plt.show()
