# Copyright (c) 2015 Christian Alis
#
# See the file LICENSE for copying permission.

import pandas as pd

def to_pandas_tseries(tseries):
    """
    Convert dict time series to a pandas TimeSeries
    
    tree.mu sends and receives time series values as a dict (json-encoded) of 
    timestamp (in seconds) and value pairs. This function will convert it to a
    pandas TimeSeries.
    
    
    Parameters
    ----------
    tseries : dict 
        dict of timestamp (in seconds) as key
    
    
    Returns
    -------
    pd_timeseries : pandas.TimeSeries
        Converted time series with timestamp as index   
    """
    tseries = pd.TimeSeries(tseries)
    tseries.index = pd.to_datetime(tseries.index.astype(int), unit='s')
    return tseries

def results_to_dframe(results):
    """
    Convert results to a data frame
    
    Flattens correlation results into a data frame. Time series values are
    excluded.
    
    
    Parameters
    ----------
    results : list of dict
        This is the output of TreeClient.get_most_correlated()
        
    Returns
    -------
    df : pandas.DataFrame
        Data frame of results
    """
    data = []
    for r in results:
        d = {
                'r': r['r'],
                'title': r['title'],
                'p_double': r['p']['double'],
                'p_left': r['p']['left'],
                'p_right': r['p']['right'],
                'p_bh_double': r['p_bh']['double'],
                'p_bh_left': r['p_bh']['left'],
                'p_bh_right': r['p_bh']['right']
            }
        data.append(d)
    return pd.DataFrame(data)