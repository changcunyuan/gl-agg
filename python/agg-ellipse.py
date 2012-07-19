#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Ellipse

size = 512,512+32
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
    x = 256+radius*math.cos(theta);
    y = 256+32+radius*math.sin(theta);
    rx = 10.1-i*0.02
    ry = 1.5*rx
    patch = Ellipse( xy=(x,y), width=2*rx, height=2*ry, angle=90+180*theta/math.pi,
                     lw=1.0, color='None', ec='k', fc='None' )
    axes.add_patch(patch)
    radius -= 0.45
    theta += dtheta

for i in range(0,39):
    thickness = (i+1)/10.0
    rx, ry = 4, 8
    x = 20 - rx +i*12.5
    y = 16 
    patch = Ellipse( xy=(x,y), width=2*rx, height=2*ry, angle=0,
                     lw=thickness, color='None', ec='k', fc='None' )
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-ellipse.png', dpi=dpi)
plt.show()
