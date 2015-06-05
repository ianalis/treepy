# Copyright (c) 2015 Christian Alis
#
# See the file LICENSE for copying permission.

from __future__ import absolute_import

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from urllib import unquote
from scipy.stats import zscore

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

def plot_max(tseries, results, legend_label='', axis_label='', n=0):
    topp_tseries = results[n]['tseries']
    topp_tseries = topp_tseries[topp_tseries.notnull()]
    
    limits = (max(tseries.index[0], topp_tseries.index[0]),
              min(tseries.index[-1], topp_tseries.index[-1]))
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    tseries.plot(ax=ax1, label=legend_label, color='b')
    ax1.set_ylabel(axis_label)
    lines, labels = ax1.get_legend_handles_labels()
        
    ax1b = topp_tseries.plot(ax=ax1, color='g', secondary_y=True,
                           label=unquote(results[n]['title']).replace('_', ' '))
    
    ax1b.set_ylabel('Normalized page views')
    lines.extend(ax1b.get_legend_handles_labels()[0])
    labels.extend(ax1b.get_legend_handles_labels()[1])
    ax1b.legend(lines, labels)
    
    ((tseries - tseries.mean()) / tseries.std()).plot(ax=ax2, color='b', 
                                                      label=legend_label)
    ((topp_tseries - topp_tseries.mean()) / topp_tseries.std()).plot(ax=ax2,
                                                                     color='g',
                        label=unquote(results[n]['title']).replace('_', ' '))
    
    ax2.set_xlim(*limits)
    ax2.set_ylabel('z-score')
    ax2.legend()
    
    fig.tight_layout()
