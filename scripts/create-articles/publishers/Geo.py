"""
    This script is written to scrap data from Geo news
    Following are the assumptions

"""


import common
from datetime import datetime
from bs4 import Comment
import re


def dateconvert(date_string):
    date_split = date_string.split(' ')
    date = date_split[2].split(',')[0]
    month = date_split[1]
    year = date_split[3]
    if len(month) <= 4:
        date_obj = datetime.strptime(date + month + year, '%d%b%Y')
    else:
        date_obj = datetime.strptime(date + month + year, '%d%B%Y')
    return date_obj


class Geo(common.Publisher):
    def __init__(self):
        super().__init__()

    def getPublisher(self, filename, pageSoup):
        return "Geo News"

    def getArticleUrl(self, filename, pageSoup):
        comment = pageSoup.find(string=lambda comment_text: isinstance(comment_text, Comment))
        url = 'https://' + comment.split(' ')[3]
        return url

    def getArticleTags(self, filename, pageSoup):
        tag = []
        tag.append(pageSoup.findAll("span", {"class": "category"})[0].text.strip())
        return tag

    def getArticleHeading(self, filename, pageSoup):
        return pageSoup.findAll("div", {"class": 'story-area'})[0].h1.text.strip()

    def getArticleDate(self, filename, pageSoup):
        article_date = pageSoup.findAll('div', {'class': 'post-time'})[0].text.strip()
        return dateconvert(article_date)

    def getArticleAuthors(self, filename, pageSoup):
        authors = []
        """
            Assuming that with 'meta' tag name there is two attributes with name "name"
            and "content" in <head>
            <meta name="twitter:creator" content="@Web Desk">
        """
        author_handle = pageSoup.findAll('meta', {'name': 'twitter:creator'})
        author_handle = author_handle[0]
        authors.append(author_handle['content'].replace('@', ''))
        return authors

    def getArticleText(self, filename, pageSoup):
        text = ''

        text_handle = pageSoup.findAll('div', {'class': 'content-area'})
        tags = text_handle[0].findAll()

        for tag in tags:
            if tag.name in ['p', 'li', 'h2', 'h3', 'h4', 'h5', 'br']:
                text += re.sub(r'[^\x00-\x7F]+', ' ', tag.text)
                text += ' '
        """
            if text is not enclosed in any tags than we collect it all from following function
        """
        if text.isspace():
            text = pageSoup.find(class_='content-area').getText().strip()
        return text

    def getArticleLanguage(self, filename, pageSoup):
        return 'en'

    def getArticleLocalID(self, filename, pageSoup):
        return filename.split('/')[-1]

    def getArticleSummary(self, filename, pageSoup):
        return None
