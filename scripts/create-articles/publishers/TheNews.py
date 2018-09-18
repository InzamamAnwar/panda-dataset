# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 12:34:33 2018    
"""

import common
from bs4 import BeautifulSoup as soup
import pdb
import re

class TheNews(common.Publisher):
    
    def __init__(self):
        super().__init__()
    
    def getPublisher(self, articleUrl, pageSoup):
        return "Dawn News"
    
    def getArticleLocalID(self, articleUrl, pageSoup):
        return None
        
    def getArticleText(self, articleUrl, pageSoup):
        text = pageSoup.find("div", {"id" : "storydetailarea"}).getText().strip("\r\n\t ")
        return text
        
    def getArticleLanguage(self, articleUrl, pageSoup):
        return "en"
    
    def getArticleDate(self, articleUrl, pageSoup):
        dateString = pageSoup.find("div", {"class" : "category-date"}).text.strip("\r\n\t ")
        # TODO: convert dateString to Date object, use date-time feature
        return dateString
        
    def getArticleAuthors(self, articleUrl, pageSoup):
        authors = set()
        authorObject = pageSoup.find("span", {"class" : "authorFullName"})
        if authorObject is not None:
            author = authorObject.text.strip("\r\n\t ")
            authors.add(author)
        else:
            authorObject = pageSoup.find("div", {"class" : "category-source"})
            if authorObject is not None:
                author = authorObject.text.strip("\r\n\t ")
                authors.add(author)
            
        return list(authors)
        
    def getArticleTags(self, articleUrl, pageSoup):
        tags = []
        category = pageSoup.find("div", {"class" : "category-name"}).h2.text.strip("\r\n\t ")
        tags.append(category)
        
        text = self.getArticleText(articleUrl, pageSoup)
        firstColon = text.find(":")
        if firstColon >= 0 and firstColon < 20:
            tags.append(text[:firstColon])
        
        return tags
    
    def getArticleHeading(self, articleUrl, pageSoup):
        return pageSoup.find("div", {"class" : "detail-heading"}).h1.text.strip("\r\n\t ")
    
    def getArticleSummary(self, articleUrl, pageSoup):
        return None
