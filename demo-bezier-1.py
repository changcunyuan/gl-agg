#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects


size = 256,256
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

n = 20
x0,y0 =  25, 240
x1,y1 =  75, 290
x2,y2 = 175, 190
x3,y3 = 225, 240

for i in range(n):
    y0 -= 10
    y1 -= 10
    y2 -= 10
    y3 -= 10
    thickness = (i+1)/10.0
    verts = [(x0, y0), (x1, y1), (x2, y2), (x3, y3) ]
    codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4 ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=thickness)
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-bezier-1.png', dpi=dpi)
plt.show()

