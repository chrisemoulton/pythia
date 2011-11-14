'''
Created on 13 Nov 2011

@author: george

This module performs text analysis of the feeds
'''

import nltk #!@UnresolvedImport
import re

class TextAnalyser(object):
    '''
    This class contains and implements all the methods responsible for 
    text analysis.
    '''
    
    def __init__(self, tweet_list=None):
        self.tweets = tweet_list
        words = self._preprocess_text()
        self.words = words
        
    def _preprocess_text(self):    
        '''
        Preprocess plain text. It is supposed to be a private method. Should not
        be called fro, outside.
        '''
        words = []
        for t in self.tweets:
            words += [ w for w in t.split() ]
        return words    
        
    def frequency_distribution(self):    
        '''
        Performs simple frequency distribution on the given text.
        '''
        frequencies = nltk.FreqDist(self.words)
        return frequencies   
    
    def retweets_patterns(self):
        '''
        A regular expression is used to identify retweets. Note that 
        Twitter identifies retweets either with "RT" followed by username
        or "via" followed by username. 
        It returns a list of dictionaries containing the origin and the user 
        who retweeted.
        
        #TODO: Refactor regex generation to the tools package
        '''
        rt_patterns = re.compile(r"(RT|via)((?:\b\W*@\w+)+)", re.IGNORECASE)
        rt_origins = []
        for t in self.tweets:
            rt_origins += rt_patterns.findall(t)
              
        return rt_origins
    
    