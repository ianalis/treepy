import pandas as pd

def to_pandas_tseries(tseries):
    """Convert tseries dict to pandas TimeSeries"""
    tseries = pd.TimeSeries(tseries)
    tseries.index = pd.to_datetime(tseries.index.astype(int), unit='s')
    return tseries

def results_to_dframe(results):
    """Convert results to a data frame"""
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