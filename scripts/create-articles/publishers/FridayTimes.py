import common
import re
from datetime import datetime
from bs4 import Comment


def dateconvert(date_string):
    """
        Expeected date format "Day Month Year"
        E.g. 20 Sep 2019
    """
    date = date_string.strip()
    date_obj = datetime.strptime(date, '%d %b %Y')
    return date_obj


class FridayTimes(common.Publisher):
    def __init__(self):
        super().__init__()

    def getArticleUrl(self, articleSourceFilename, pageSoup):
        comment = pageSoup.find(string=lambda comment_text: isinstance(comment_text, Comment))
        url = 'https://' + comment.split(' ')[3]
        return url

    def getArticleLocalID(self, articleSourceFilename, pageSoup):
        return None

    def getPublisher(self, articleSourceFilename, pageSoup):
        return 'Friday Times'

    def getArticleAuthors(self, articleSourceFilename, pageSoup):
        """
            Authors of the article are extracted with the following assumption
            '
            Author Name
            TFT Issue: 13 Sep 2018
            '
        """
        return pageSoup.findAll('div', {'class': 'post_detail2'})[0].text.split('\n')[1]

    def getArticleDate(self, articleSourceFilename, pageSoup):
        """
            Article publishing date is mentioned in the following way
            '
            Author Name
            TFT Issue: 13 Sep 2018
            '
        """
        # Uncomment the following if pageSoup is obtained from URL directly
        # date = pageSoup.findAll('div', {'class': 'post_detail2'})[0].text.split('\n')[2].split(':')[1]
        date = pageSoup.findAll('div', {'class': 'post_detail2'})[0].text.split('\n')[3].split(':')[1]
        return dateconvert(date)

    def getArticleHeading(self, articleSourceFilename, pageSoup):
        return pageSoup.findAll('div', {'class': 'post_header'})[0].h1.text.strip()

    def getArticleLanguage(self, articleSourceFilename, pageSoup):
        return 'en'

    def getArticleSummary(self, articleSourceFilename, pageSoup):
        return None

    def getArticleTags(self, articleSourceFilename, pageSoup):
        tag_handle = pageSoup.findAll('div', {'class': 'post_wrapper'})
        for tag in tag_handle:
            text = tag.p.text.split(':')
            if len(text) != 0 and text[0] == 'Tags':
                category = text[1:]
                break
        return category

    def getArticleText(self, articleSourceFilename, pageSoup):
        text = ''
        text_handle = pageSoup.findAll('div', {'class': 'backgroundtext'})
        tags = text_handle[0].findAll()

        for tag in tags:
            if tag.name in ['p', 'li', 'h2', 'h3', 'h4', 'h5']:
                # Removing non-ASCII characters
                text += re.sub(r'[^\x00-\x7F]+', ' ', tag.text)
                text += ' '
        return text
