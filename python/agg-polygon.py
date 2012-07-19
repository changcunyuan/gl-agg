#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import Polygon


size = 512,512+32
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

radius = 255.0
theta = 0
dtheta = 5.5/180.0*np.pi

for i in range(500):
    xc =    256+radius*np.cos(theta);
    yc = 32+256+radius*np.sin(theta);
    r = 10.1-i*0.02
    points = [(xc+np.cos(t+theta)*r, yc+np.sin(t+theta)*r)
              for t in np.linspace(0,2*np.pi,6,endpoint=False)]
    P = Polygon( points, closed=True, lw=1., color='None', ec='k', fc='None' )
    axes.add_patch( P )

    radius -= 0.45
    theta += dtheta

for i in range(0,39):
    thickness = (i+1)/10.0
    r = 4
    xc = 20+i*12.5 - r
    yc = 16
    points = [(xc+np.cos(t)*r, yc+np.sin(t)*r)
              for t in np.linspace(0,2*np.pi,6,endpoint=False)]
    P = Polygon( points, closed=True, lw=thickness, color='None', ec='k', fc='None' )
    axes.add_patch( P )

plt.xticks([]),plt.yticks([])
fig.savefig('agg-polygon.png', dpi=dpi)
plt.show()
