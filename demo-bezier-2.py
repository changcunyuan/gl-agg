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

verts = np.array( [(90, 192), (524, 261), (536, 112), (66, 383)] )
codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4 ]

size = 512,512
dpi = 72.0
figsize= size[0]/float(dpi),size[1]/float(dpi)
fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
fig.canvas.set_window_title('AGG bezier') 


axes = fig.add_axes([0.0, 0.0, 1.0, 1.0])
axes.set_xlim(0,size[0])
axes.set_ylim(0,size[1])

path = Path(verts, codes)
patch = patches.PathPatch(path, facecolor='none', lw=100, alpha=0.5)
patch.set_path_effects([PathEffects.Stroke(capstyle='round')])
axes.add_patch(patch)

plt.xticks([]),plt.yticks([])
plt.show()
#fig.savefig('agg-bezier-2.png', dpi=dpi)
