#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects


size = 512,512+32
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])


radius = 255.0
theta, dtheta = 0, 5.5/180.0*math.pi
thickness = 1.0

for i in range(500):
    xc, yc = 256, 256+32
    r = 10.1-i*0.02
    thickness = 1.0
    x0 = xc + np.cos(theta)*radius*0.925
    y0 = yc + np.sin(theta)*radius*0.925
    x1 = xc + np.cos(theta+dtheta/2)*radius*0.950
    y1 = yc + np.sin(theta+dtheta/2)*radius*0.950
    x2 = xc + np.cos(theta-dtheta/2)*radius*0.975
    y2 = yc + np.sin(theta-dtheta/2)*radius*0.975
    x3 = xc + np.cos(theta)*radius*1.000
    y3 = yc + np.sin(theta)*radius*1.000
    verts = [ (x0,y0), (x1,y1), (x2,y2), (x3,y3) ] 
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4 ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, lw=thickness, color='None', ec='k', fc='None')
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

    radius -= 0.45
    theta += dtheta

for i in range(0,49):
    thickness = (i+1)/10.0
    x0 = 20+i*10
    y0 = 10
    x1 = 15+i*10
    y1 = 14
    x2 = 25+i*10
    y2 = 18
    x3 = 20+i*10
    y3 = 22

    verts = [ (x0,y0), (x1,y1), (x2,y2), (x3,y3) ] 
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4 ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, lw=thickness, color='None', ec='k', fc='None')
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)



plt.xticks([]),plt.yticks([])
fig.savefig('agg-curve.png', dpi=dpi)
plt.show()
