"""
    Script written for scrapping news article from Dawn.com
    Following are the assumptions of collecting data
"""

import common
from datetime import datetime


def dateconvert(date_string):
    date_split = date_string.split(' ')
    if len(date_split) == 5:
        date = date_split[2].split(',')[0]
        month = date_split[1]
        year = date_split[3]
    elif len(date_split) == 4:
        date = date_split[2].split(',')[0]
        month = date_split[1]
        year = date_split[3]
    else:
        date = date_split[1].split(',')[0]
        month = date_split[0]
        year = date_split[2]
    if len(month) <= 3:
        date_obj = datetime.strptime(date + month + year, '%d%b%Y')
    else:
        date_obj = datetime.strptime(date + month + year, '%d%B%Y')
    return date_obj


class Dawn(common.Publisher):
    def __init__(self):
        super().__init__()

    def getPublisher(self, filename, pageSoup):
        return "Dawn News"

    def getArticleUrl(self, filename, pageSoup):
        """
            ** this was the old approach **
            Filename is expected to be in the format "pagexxxxx.html"
            id = filename.split('.html')[0].split('page')[1]
            url = 'https://www.dawn.com/news/' + id

            ** New approach **
            Article URL is given in the and extracted with the following assumption
            Assuming that with 'link' tag name there is two attributes with name "rel"
            and "href" in <head>
            <link rel="canonical" href="url of the article">
        """
        url_handle = pageSoup.findAll('link', {'rel': 'canonical'})
        url_handle = url_handle[0]
        url = url_handle['href']
        return url

    def getArticleLocalID(self, filename, pageSoup):
        return filename.split('/')[-1]

    def getArticleHeading(self, filename, pageSoup):
        return pageSoup.h2.text.strip()

    def getArticleAuthors(self, filename, pageSoup):
        authors = pageSoup.findAll("span", {"class": "story__byline"})[0].text.strip()
        return authors.split('|')

    def getArticleDate(self, filename, pageSoup):
        date_string = pageSoup.findAll("span", {"class": "story__time"})[0].text.strip()
        return dateconvert(date_string)

    def getArticleLanguage(self, filename, pageSoup):
        return 'en'

    def getArticleText(self, filename, pageSoup):
        text = pageSoup.find(class_='story__content').getText().strip('\r\n').replace('\n', '')
        return text

    def getArticleSummary(self, filename, pageSoup):
        return None

    def getArticleTags(self, filename, pageSoup):
        return pageSoup.head.title.text.split('-')
