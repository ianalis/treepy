# Copyright (c) 2015 Christian Alis
#
# See the file LICENSE for copying permission.

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from urllib import unquote

def plot_corr(results):
    """
    Plot title, correlation and corrected p-values as horizontal bars
    
    Rendering works best with 50 results.
    
    Parameters
    ----------
    results : list of dict
        Output of `get_most_correlated()`
    
    
    Returns
    -------
    ax : matplotlib.Axes
        Rendered
    """
    fig, ax = plt.subplots(figsize=(6,10)
                           #subplot_kw=dict(left=0.05, right=0.95,
                           #                bottom=0.03, top=0.97)
                           )
    ax.barh(np.arange(len(results))+0.5, [r['r'] for r in results[::-1]], 0.3, 
            label='r')
    ax.barh(range(len(results)), [r['p_bh']['double'] for r in results[::-1]], 
            0.3, color='r', label='FDR-corrected p')
    for i, result in enumerate(results[::-1]):
        title = unquote(result['title']).replace('_', ' ')
        if len(title) > 30:
            title = title[:27].strip()
            title = title + '...'
        if result['r'] > 0:
            ax.text(-0.01, i, title, horizontalalignment='right')
        else:
            ax.text(0.01, i, title, horizontalalignment='left')
    ax.set_xlim(-1,1)
    ax.set_xticks(np.linspace(1,-1,9))
    ax.set_yticks([])
    legend = ax.legend(loc='best', frameon=True, framealpha=0.4)
    legend.get_frame().set_facecolor('w')
    fig.tight_layout()
    return ax