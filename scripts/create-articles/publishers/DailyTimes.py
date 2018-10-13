import common
import re
from datetime import datetime
from bs4 import Comment


def dateconvert(date_string):
    """
        Expected fromat of date is "Month Day, Year"
        E.g. September 18 2018
    """
    date = date_string.replace(',', '')
    date_obj = datetime.strptime(date, '%B %d %Y')
    return date_obj


class DailyTimes(common.Publisher):
    def __init__(self):
        super().__init__()

    def getArticleTags(self, articleSourceFilename, pageSoup):
        tag = []
        tag_handle = pageSoup.find(class_="entry-terms").text
        tag.append(tag_handle)
        return tag

    def getArticleSummary(self, articleSourceFilename, pageSoup):
        return ''

    def getArticleText(self, articleSourceFilename, pageSoup):
        text = ''
        text_handle = pageSoup.findAll('div', {'class': 'entry-content'})
        tags = text_handle[0].findAll()
        for tag in tags:
            # Up to h5 is not necessary, however for safe side it is being used
            if tag.name in ['p', 'li', 'h2', 'h3', 'h4', 'h5', 'br', 'div']:
                # Here we remove all the non-ASCII characters from the string
                text += re.sub(r'[^\x00-\x7F]+', ' ', tag.text)
                text += ' '
        return text

    def getArticleLanguage(self, articleSourceFilename, pageSoup):
        return 'en'

    def getArticleAuthors(self, articleSourceFilename, pageSoup):
        """
            Assumption for extracting Author name
            < a href="SOME LINK" title="More Articles by staff Report" class="author-name">AUTHOR NAME </a>

            In some cases the author name is present in the first found class of "author-name" so we extract class
            with same name "author-name" using previous handle with "findNext" method. This is implemented in else
            statement. If statement checks whether the author name is present in the first class or not
        """
        author_name = []
        author_name_handle = pageSoup.find(class_='author-name')
        if author_name_handle.text != '':
            author_name.append(author_name_handle.text)
            return author_name
        else:
            author_name_handle = author_name_handle.findNext(class_='author-name')
            author_name.append(author_name_handle.text)
            return author_name

    def getArticleHeading(self, articleSourceFilename, pageSoup):
        """
            Assumption for extracting the title
            ['<meta content=', '"TITLE" - Daily Times', ' property=', 'og:title', '/>']
        """
        heading_handle = pageSoup.findAll('meta', {'property': 'og:title'})[0]
        return str(heading_handle).split('"')[1].split('- Daily Times')[0]

    def getArticleDate(self, articleSourceFilename, pageSoup):
        """
            Data format is "Month Day, Year"
            E.g. September 19, 2018
        """
        date = pageSoup.find(class_='entry-time').text
        return dateconvert(date)

    def getPublisher(self, articleSourceFilename, pageSoup):
        return "Daily Times"

    def getArticleLocalID(self, articleSourceFilename, pageSoup):
        return None

    def getArticleUrl(self, articleSourceFilename, pageSoup):
        """
            Article URL is assumed to be the first comment in the file
        """
        comment = pageSoup.find(string=lambda comment_text: isinstance(comment_text, Comment))
        url = 'https://' + comment.split(' ')[3]
        return url
