# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 20:28:27 2018
"""

import sys
sys.path.append("..")
import common

import math
from bs4 import BeautifulSoup as soup
import pdb

class CountWords(common.Feature):
    
    def __init__(self):
        super().__init__()
    
    def extract(self, article):
        
        
        wordList = article.text.split()
        
        dictionary = self.__wordListToFreqDict(wordList)
        sortedDict = self.__sortFreqDict(dictionary)
        totalTopWords = min(10, len(sortedDict))
        shortListed = []
        for freq, word in sortedDict[:totalTopWords]:
            shortListed.append([word, freq])
        
        return {"totalWords" : len(wordList), \
                "mostCommonWords" : shortListed}
    
    # Given a list of words, return a dictionary of
    # word-frequency pairs.
    def __wordListToFreqDict(self, wordlist):
        wordfreq = [wordlist.count(p) for p in wordlist]
        return dict(zip(wordfreq, wordlist))
    
    # Sort a dictionary of word-frequency pairs in
    # order of descending frequency.
    def __sortFreqDict(self, freqdict):
        aux = [(key, freqdict[key]) for key in freqdict]
        aux.sort()
        aux.reverse()
        return aux
    