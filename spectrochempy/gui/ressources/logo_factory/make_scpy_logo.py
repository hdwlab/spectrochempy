# -*- coding: utf-8 -*-
#
# =============================================================================
# Copyright (©) 2015-2018 LCS
# Laboratoire Catalyse et Spectrochimie, Caen, France.
# CeCILL-B FREE SOFTWARE LICENSE AGREEMENT
# See full LICENSE agreement in the root directory
# =============================================================================

"""
Logo SCPy (based on the LCS logo)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from spectrochempy.utils import NRed, NBlue

def draw_circle(ax) :
    circle = plt.Circle((-0.5 + decal, 0.5), .48,
                        edgecolor=contour,
                        fill=True,
                        clip_on=False,
                        facecolor=background,
                        linewidth=3)
    ax.add_artist(circle)


def plot_fid(ax, start, lim) :
    x = np.linspace(start, lim, 550)
    y = -np.exp(-x / .2) * np.sin(8. * x * np.pi) / 3. + 0.6
    s = 0
    ax.plot(x[s :] - 1. + decal, y[s :],
            transform=ax.transAxes,
            clip_on=False,
            c=contour, lw=3)
    return x, y


def write_scpy(ax, decal) :
    ax.text(0.47, 0.25, 'SCP', color=NBlue, fontsize=62, ha='center',
            va='baseline', alpha=1.0, family=['Calibri', 'sans-serif'],
            weight=999, transform=ax.transAxes)
    ax.text(0.77, 0.185, 'y', color=NRed, fontsize=50, ha='center',
            va='baseline', alpha=1.0, family=['Calibri', 'sans-serif'],
            weight=999, transform=ax.transAxes)


decal = 1

figcolor = 'white'
dpi = 300
fig = plt.figure(figsize=(2.5, 2.5), dpi=dpi)

ax = fig.add_axes([0, 0, 1, 1], frameon=True, clip_on=False, aspect=1)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_axis_off()

contour = '#505080'
background = (0.98,0.82,0.42)
draw_circle(ax)
plot_fid(ax, 0.05, 0.96)
write_scpy(ax, decal)

plt.savefig('../scpy.png', dpi=60, transparent=True)

plt.savefig('../scpy_splash.png', dpi=150, transparent=True)