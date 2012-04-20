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

inner_radius = 64
outer_radius = 250
n = 49
for i in range(n):
    angle = (i/(float)(n)) * 2 * math.pi
    x1 = 256 + math.cos(angle)*inner_radius;
    y1 = 256 + math.sin(angle)*inner_radius;
    x2 = 256 + math.cos(angle)*outer_radius;
    y2 = 256 + math.sin(angle)*outer_radius;
    thickness = (i+1)/10.0;
    verts = [(x1, y1), (x2, y2)]
    codes = [Path.MOVETO, Path.LINETO ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=thickness)
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-lines-2.png', dpi=dpi)
plt.show()
