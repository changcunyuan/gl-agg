#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
#matplotlib.use('Agg')
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
    xc = 256
    yc = 32+256
    r = 10.1-i*0.02
    
    x0 = xc + np.cos(theta+dtheta/3)*radius*.925
    y0 = yc + np.sin(theta+dtheta/3)*radius*.925
    
    x1 = xc + np.cos(theta-dtheta/3)*radius*.925
    y1 = yc + np.sin(theta-dtheta/3)*radius*.925
    
    x2 = xc + np.cos(theta)*radius*1.00
    y2 = yc + np.sin(theta)*radius*1.00

    P = Polygon( ([x0,y0], [x1,y1], [x2,y2]), closed=True,
                 lw=1., color='None', ec='k', fc='None' )
    axes.add_patch( P )

    theta += dtheta
    radius -= 0.45

for i in range(0,39):
    thickness = (i+1)/20.0
    xc,yc = 20 + i*12.5, 16
    x0,y0 = xc-5, yc-5
    x1,y1 = xc+5, yc-5
    x2,y2 = xc,   yc+5
    P = Polygon( ([x0,y0], [x1,y1], [x2,y2]), closed=True,
                 lw=thickness, color='None', ec='k', fc='None' )
    axes.add_patch( P )



plt.xticks([]),plt.yticks([])
fig.savefig('agg-triangle.png', dpi=dpi)
plt.show()
