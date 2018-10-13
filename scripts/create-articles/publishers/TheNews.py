# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 12:34:33 2018
"""

import common
from bs4 import Comment
from datetime import datetime
import pdb
import re


def dateconvert(date_string):
    date = date_string.replace(',', '')
    date_obj = datetime.strptime(date, '%B %d %Y')
    return date_obj

class TheNews(common.Publisher):

    def __init__(self):
        super().__init__()

    def getPublisher(self, filename, pageSoup):
        return "The News"

    def getArticleUrl(self, filename, pageSoup):
        comment = pageSoup.find(string=lambda comment_text: isinstance(comment_text, Comment))
        url = 'https://' + comment.split(' ')[3]
        return url

    def getArticleLocalID(self, filename, pageSoup):
        return None

    def getArticleText(self, filename, pageSoup):
        text = pageSoup.find("div", {"id" : "storydetailarea"}).getText().strip("\r\n\t ")
        return text

    def getArticleLanguage(self, filename, pageSoup):
        return "en"

    def getArticleDate(self, filename, pageSoup):
        dateString = pageSoup.find("div", {"class" : "category-date"}).text.strip("\r\n\t ")
        """
            Date string format for The News is Month Day, Year
            E.g. "February 10, 2016"
        """
        return dateconvert(dateString)

    def getArticleAuthors(self, filename, pageSoup):
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

    def getArticleTags(self, filename, pageSoup):
        tags = []
        category = pageSoup.find("div", {"class" : "category-name"}).h2.text.strip("\r\n\t ")
        tags.append(category)

        text = self.getArticleText(filename, pageSoup)
        firstColon = text.find(":")
        if firstColon >= 0 and firstColon < 20:
            tags.append(text[:firstColon])

        return tags

    def getArticleHeading(self, filename, pageSoup):
        return pageSoup.find("div", {"class" : "detail-heading"}).h1.text.strip("\r\n\t ")

    def getArticleSummary(self, filename, pageSoup):
        return None
