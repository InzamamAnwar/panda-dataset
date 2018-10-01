import common
import re
from datetime import datetime
from bs4 import Comment


def dateconvert(date_string):
    """
        Expected format of date is "Month Day, Year"
        E.g. September 20, 2018
    """
    date = date_string.replace(',', '')
    date_obj = datetime.strptime(date, '%B %d %Y')
    return date_obj


class FrontierPost(common.Publisher):
    def __init__(self):
        super().__init__()

    def getArticleText(self, articleSourceFilename, pageSoup):
        text = ''
        text_handle = pageSoup.findAll('div', {'class': 'entry-content'})
        tags = text_handle[0].findAll()

        for tag in tags:
            if tag.name in ['p', 'li', 'h2', 'h3', 'h4', 'h5', 'br']:
                text += re.sub(r'[^\x00-\x7F]+', ' ', tag.text)
                text += ' '
        return text

    def getArticleTags(self, articleSourceFilename, pageSoup):
        tag_handle = pageSoup.findAll('div', {'class': 'cat-links'})[0].findAll()
        tags = []
        for tag in tag_handle:
            tags.append(tag.text)
        tags = tags[1:]
        return tags

    def getArticleSummary(self, articleSourceFilename, pageSoup):
        return None

    def getArticleLanguage(self, articleSourceFilename, pageSoup):
        return 'en'

    def getArticleHeading(self, articleSourceFilename, pageSoup):
        return pageSoup.findAll('header', {'class': 'entry-header'})[0].h1.text.strip()

    def getArticleDate(self, articleSourceFilename, pageSoup):
        """
            Date format Month Day, Year
            E.g. April 13, 2018
        """
        date = pageSoup.findAll('header', {'class': 'entry-header'})[0].span.time.text.strip()
        return dateconvert(date)

    def getArticleAuthors(self, articleSourceFilename, pageSoup):
        author_name = []
        author_name.append(pageSoup.findAll('div', {'class': 'author'})[0].a.text.strip())
        return author_name

    def getPublisher(self, articleSourceFilename, pageSoup):
        return 'Frontier Post'

    def getArticleLocalID(self, articleSourceFilename, pageSoup):
        return None

    def getArticleUrl(self, articleSourceFilename, pageSoup):
        comment = pageSoup.find(string=lambda comment_text: isinstance(comment_text, Comment))
        url = 'https://' + comment.split(' ')[3]
        return url
