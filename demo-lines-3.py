#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
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


verts = [ [(50,  50), (200,  50+20)],
          [(50, 122), (200, 122+20)],
          [(50, 194), (200, 194+20)] ]
effects = [ PathEffects.Stroke(capstyle='round'),
            PathEffects.Stroke(capstyle='projecting'),
            PathEffects.Stroke(capstyle='butt') ]


for vert,effect in zip(verts,effects):
    code = [Path.MOVETO, Path.LINETO ]
    path = Path(vert, code)
    patch = patches.PathPatch(path, facecolor='none', lw=32)
    patch.set_path_effects([effect])
    axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
fig.savefig('agg-lines-3.png', dpi=dpi)
plt.show()
