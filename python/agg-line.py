#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects
import matplotlib.image as mpimg

size = 512,512+32
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

radius = 255.0
theta, dtheta = 0, 5.5/180.0*np.pi
for i in range(500):
    xc, yc = 256, 256+32
    r = 10.1-i*0.02

    x0 = xc + np.cos(theta)*radius*.925
    y0 = yc + np.sin(theta)*radius*.925
    x1 = xc + np.cos(theta)*radius*1.00
    y1 = yc + np.sin(theta)*radius*1.00
    verts = np.array( [(x0, y0), (x1, y1)] )
    codes = [Path.MOVETO, Path.LINETO ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=1.0)
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

    radius -= 0.45
    theta += dtheta

for i in range(0,49):
    thickness = (i+1)/10.0
    x0 = 20+i*10
    y0 = 10
    x1 = x0
    y1 = y0+12

    verts = np.array( [(x0, y0), (x1, y1)] )
    codes = [Path.MOVETO, Path.LINETO ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=thickness)
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-line.png', dpi=dpi)
plt.show()
