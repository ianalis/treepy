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
    def __init__(self, platform_url='http://api.tree.mu', db=None):
        """
        Parameters
        ----------
        platform_url : str
            URL of server including protocol and port
        db : str
            database name; server default if `None`
        """
        self.platform_url = platform_url
        self.db = db
        
    def get_most_correlated(self, title_or_tseries, results_count=50, 
                            method='pearson', freq='D', db=None):
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
        db : str
            database name; db defined at `__init__` if `None`
            
        
        Returns
        -------
        results : list of dict
            List of most correlated articles ordered by decreasing correlation
            coefficient
        """
        params = {'results_count': results_count,
                  'method': method,
                  'freq': freq}
        if db is None:
            db = self.db
        if db:
            params['db'] = db            
        if isinstance(title_or_tseries, basestring):
            params['title'] = title_or_tseries
        else:
            params['values'] = title_or_tseries.to_json()
        
        results = json.load(urlopen(self.platform_url + '/corr/', 
                                    data=urlencode(params)))
        results = sorted(results, key=itemgetter('r'), reverse=True)
        for r in results:
            r['tseries'] = to_pandas_tseries(r['tseries'])            
        
        return results
    
    def get_page(self, title, freq='D', db=None):
        """
        Get page views time series of a particular article
        
        
        Parameters
        ----------
        title : str
            Article title which should match the Wikipedia title including
            case, underscores and escaped characters
        freq :  "D", "W-SUN", "MS"
            Frequency of time series
        db : str
            database name; db defined at `__init__` if `None`
            
            
        Returns
        -------
        tseries : pandas.TimeSeries
            Pageviews normalized with total pageviews
        """
        params = {'freq': freq}
        if db is None:
            db = self.db
        if db:
            params['db'] = db
            
        tseries = json.load(urlopen('%s/page/%s?%s' % (self.platform_url,
                                                       quote(title),
                                                       urlencode(params))))
        return to_pandas_tseries(tseries)
    
    def get_total(self, freq='D', db=None):
        """
        Get the time series of total pageviews
                
        Parameters
        ----------
        freq :  "D", "W-SUN", "MS"
            Frequency of time series
        db : str
            database name; db defined at `__init__` if `None`
            
        
        Returns
        -------
        tseries : pandas.TimeSeries
            Time series of total pageviews
        """
        params = {'freq': freq}
        if db is None:
            db = self.db
        if db:
            params['db'] = db
            
        tseries = json.load(urlopen('%s/page/?%s' % (self.platform_url,
                                                     urlencode(params))))
        return to_pandas_tseries(tseries)
    
    def lookup(self, key, limit=None, db=None):
        """
        Return nearest substring matches of key in titles
        
        The other Tree API endpoints require a precise title. This 
        endpoint/method allows a user to find the titles most similar to `key`. 
        The appropriate `raw_title` can then be selected from the results and 
        passed on as the `title` parameter in other endpoints.
        
        Parameters
        ----------
        key : str or unicode
            Substring to search for in titles
        limit : int
            Maximum number of results. Default server limit if `None`.
        db : str
            Database name; db defined at `__init__` if `None`
        
        
        Returns
        -------
        matches : list of dict
            Titles that contain `key` as a case-insensitive substring, sorted by
            increasing Damerau-Levenshtein distance
        """
        params = {'key': key}
        if limit:
            paras['limit'] = limit
        if db:
            params['db'] = db
            
        matches = json.load(urlopen('%s/lookup/%s?%s' % (self.platform_url,
                                                         quote(key),
                                                         urlencode(params))))
        return matches
    