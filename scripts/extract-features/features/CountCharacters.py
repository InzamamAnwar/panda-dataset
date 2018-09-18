# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 22:43:38 2018
"""

import sys
sys.path.append("..")
import common

from bs4 import BeautifulSoup as soup
import pdb

class CountCharacters(common.Feature):
    
    def __init__(self):
        super().__init__()
    
    def extract(self, article):
        return {"count" : len(article.text)}
    