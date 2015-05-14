# Copyright (c) 2015 Christian Alis
#
# See the file LICENSE for copying permission.

from __future__ import absolute_import

import json
import pandas as pd
from urllib import urlopen, urlencode, quote
from operator import itemgetter
from .utils import to_pandas_tseries

class TreeClient(object):
    """Client for interacting with the tree.mu API"""
    def __init__(self, platform_url='http://api.tree.mu'):
        self.platform_url = platform_url
        
    def get_most_correlated(self, title_or_tseries, results_count=50, 
                            method='pearson', freq='D'):
        """
        Return most correlated articles
        
        
        Parameters
        ----------
        title_or_tseries : str or pandas TimeSeries
            Article title or time series to correlate with. The title must 
            exactly match the Wikipedia title including case, underscores and 
            escaped characters.
        results_count : integer
            Number of most correlated articles to return
        method : "pearson", "spearman", "kendall"
            Method of correlation
        freq : "D", "W-SUN", "MS"
            Frequency of time series
            
        
        Returns
        -------
        results : list of dict
            List of most correlated articles ordered by decreasing correlation
            coefficient
        """
        params = [('results_count', results_count),
                  ('method', method),
                  ('freq', freq)]
        if isinstance(title_or_tseries, basestring):
            params.append(('title', title_or_tseries))
        else:
            params.append(('values', title_or_tseries.to_json()))
        
        results = json.load(urlopen(self.platform_url + '/corr/', 
                                    data=urlencode(params)))
        results = sorted(results, key=itemgetter('r'), reverse=True)
        for r in results:
            r['tseries'] = to_pandas_tseries(r['tseries'])            
        
        return results
    
    def get_page(self, title, freq='D'):
        """
        Get page views time series of a particular article
        
        
        Parameters
        ----------
        title : str
            Article title which should match the Wikipedia title including
            case, underscores and escaped characters
        freq :  "D", "W-SUN", "MS"
            Frequency of time series
            
            
        Returns
        -------
        tseries : pandas.TimeSeries
            Pageviews normalized with total pageviews
        """
        params = {'freq': freq}
        tseries = json.load(urlopen('%s/page/%s?%s' % (self.platform_url,
                                                     quote(title),
                                                     urlencode(params))))
        return to_pandas_tseries(tseries)
    
    def get_total(self, freq='D'):
        """
        Get the time series of total pageviews
                
        Parameters
        ----------
        freq :  "D", "W-SUN", "MS"
            Frequency of time series
            
        
        Returns
        -------
        tseries : pandas.TimeSeries
            Time series of total pageviews
        """
        params = {'freq': freq}
        tseries = json.load(urlopen('%s/page/?%s' % (self.platform_url,
                                                   urlencode(params))))
        return to_pandas_tseries(tseries)
    