from __future__ import absolute_import

import json
import pandas as pd
from urllib import urlopen, urlencode, quote
from operator import itemgetter
from .utils import to_pandas_tseries

class TreeClient(object):
    def __init__(self, platform_url='http://api.tree.mu'):
        self.platform_url = platform_url
        
    def get_most_correlated(self, tseries, results_count=100, method='pearson', 
                            freq='D'):
        """Return most correlated articles"""
        params = [('values', tseries.to_json()),
                  ('results_count', results_count),
                  ('method', method),
                  ('freq', freq)]
        print freq
        
        results = json.load(urlopen(self.platform_url + '/corr/', 
                                    data=urlencode(params)))
        results = sorted(results, key=itemgetter('r'), reverse=True)
        for r in results:
            r['tseries'] = to_pandas_tseries(r['tseries'])            
        
        return results
    
    def get_page(self, title, freq='D'):
        """Get page views time series"""
        params = {'freq': freq}
        tseries = json.load(urlopen('%s/page/%s?%s' % (self.platform_url,
                                                     quote(title),
                                                     urlencode(params))))
        return to_pandas_tseries(tseries)
    
    def get_total(self, freq='D'):
        """Get total page views time series"""
        params = {'freq': freq}
        tseries = json.load(urlopen('%s/page/?%s' % (self.platform_url,
                                                   urlencode(params))))
        return to_pandas_tseries(tseries)