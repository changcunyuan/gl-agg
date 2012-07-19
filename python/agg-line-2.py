#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
#matplotlib.use('Agg')
matplotlib.rcParams['toolbar'] = 'None'
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.patheffects as PathEffects
import matplotlib.image as mpimg

size = 512,256
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")

axes = fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

for i in range(45):
    x1 = 20+i*10
    x2 = x1+15
    y1 = 25
    y2 = 225
    thickness = (i+1)/10.0
    verts = np.array( [(x1, y1), (x2, y2)] )
    codes = [Path.MOVETO, Path.LINETO ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='none', lw=thickness)
    patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-line.png', dpi=dpi)
plt.show()
