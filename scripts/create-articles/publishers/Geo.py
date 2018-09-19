"""
    This script is written to scrap data from Geo news
    Following are the assumptions

"""


import common
from datetime import datetime


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
        return None

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
        author = pageSoup.findAll('span', {'class': 'by_author'})[0].text.strip()
        if author == 'By':
            authors.append('')
            return authors
        else:
            authors.append(author)
            return authors

    def getArticleText(self, filename, pageSoup):
        return pageSoup.find(class_='content-area').getText().strip()

    def getArticleLanguage(self, filename, pageSoup):
        return 'en'

    def getArticleLocalID(self, filename, pageSoup):
        return filename.split('/')[-1]

    def getArticleSummary(self, filename, pageSoup):
        return None
