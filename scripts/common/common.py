# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 08:21:55 2018
"""

from abc import ABC, abstractmethod
from enum import Enum
from bs4 import BeautifulSoup as soup
import yaml
import json
import os
import glob
import pdb
from datetime import datetime

# TODO: Is common really common? Keep the truly common parts and move everything else to stage level

# TODO: check types when running init functions
# This ensures that everyone ends up with the same common objects

def dynamicImport(name):
    try:
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod
    except:
        return None

class Article:
    def __init__(self, articleDict = None, globalID = None, publisher = None, url = None, date = None, text = None, language = None, heading = None, summary = None, tags = None, authors = None):

        if articleDict is not None:
            # Load article elements
            self.globalID = articleDict["globalID"]
            self.publisher = articleDict["publisher"]
            self.url = articleDict["url"]
            self.date = articleDict["date"]
            self.text = articleDict["text"]
            self.language = articleDict["language"]
            self.heading = articleDict["heading"]
            self.summary = articleDict["summary"]
            self.tags = articleDict["tags"]
            self.authors = articleDict["authors"]
        else:
            self.globalID = globalID
            self.publisher = publisher
            self.url = url
            self.date = date
            self.text = text
            self.language = language
            self.heading = heading
            self.summary = summary
            self.tags = tags
            self.authors = authors

    def __str__(self):
        response = "globalID: " + str(self.globalID) + "\n" + \
        "publisher: " + str(self.publisher) + "\n" + \
        "url: " + str(self.url) + "\n" + \
        "date: " + str(self.date) + "\n" + \
        "text: " + str(self.text) + "\n" + \
        "language: " + str(self.language) + "\n" + \
        "heading: " + str(self.heading) + "\n" + \
        "summary: " + str(self.summary) + "\n"

        response += "tags: "
        if self.tags == None:
            response += str(self.tags)
        else:
            response += "[" + ", ".join(self.tags) + "]"
        response += "\n"

        response += "authors: "
        if self.authors == None:
            response += str(self.authors)
        else:
            response += "[" + ", ".join(self.authors) + "]"
        response += "\n"

        return response

    def save(self, folderPath, filename, outputType):

        # TODO: check output type before accessing dot value
        fileContents = None
        extension = ""
        if outputType.value is OutputType.YAML.value:
            fileContents = yaml.dump(self.__dict__, default_flow_style = False)
            extension = ".yaml"
        elif outputType.value is OutputType.JSON.value:
            fileContents = json.dumps(self.__dict__)
            extension = ".json"
        else:
            print ("Error: Invalid output type")

        fullPath = os.path.join(folderPath, filename + extension)
        outputFile = open(fullPath, 'w+')
        outputFile.write(fileContents)
        outputFile.close()

class OutputType(Enum):
    YAML = 1
    JSON = 2

# Need to implement 3 methods for dates
# 1 - compareWith(anotherDate)
# 2 - isValidDate()
# 3 - getNextDate()
# 4 - getWeekDay() - optional
# Either use the datetime object or create a wrapper class that uses the datetime object internally

class Date:
    def __init__(self, day = None, month = None, year = None):

        self.valid = False
        if self.isValid(day, month, year):
            self.day = day
            self.month = month
            self.year = year
            self.valid = True

    def __init__(self, dateString = None):
        # String Date Pattern expected: DD-MM-YYYY
        # TODO: Date from String
        self.valid = False
        if dateString is None:
            return

        dateParts = dateString.split("-")
        if len(dateParts) is not 3:
            return

        day, month, year = dateParts
        if not day.isdigit() or not month.isdigit() or not year.isdigit():
            return

        if self.isValid(day, month, year):
            self.day = day
            self.month = month
            self.year = year
            self.valid = True

    def compareWith(self, date):
        # TODO: logic should be similar to compareTo(...)
        pass

    def isValid(self, day, month, year):
        # TODO: check if the date is valid
        return True # TODO: remove this line

    def getNextDate(self):
        # TODO: get the next date: will be useful to find dates in ranges
        pass

    def getWeekDay(self):
        # TODO: find weekday based on date
        pass

    def __str__(self):
        return "date: " + "[" + "day: " + str(self.day) + ", " + "month: " +  str(self.month) + ", " + "year: " + str(self.year) + "]"

class Feature(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def extract(self, article):
        pass

class Publisher(ABC):

    def __init__(self):
        super().__init__()

    def createArticleObject(self, globalID, articleSourceFilename, articleSourceCode):

        # Create page soup
        pageSoup = soup(articleSourceCode, 'html.parser')

        status = ""
        publisher, status = self.__parseElement("getPublisher", articleSourceFilename, pageSoup, status)
        url, status = self.__parseElement("getArticleUrl", articleSourceFilename, pageSoup, status)
        date, status = self.__parseElement("getArticleDate", articleSourceFilename, pageSoup, status)
        text, status = self.__parseElement("getArticleText", articleSourceFilename, pageSoup, status)
        language, status = self.__parseElement("getArticleLanguage", articleSourceFilename, pageSoup, status)
        heading, status = self.__parseElement("getArticleHeading", articleSourceFilename, pageSoup, status)
        summary, status = self.__parseElement("getArticleSummary", articleSourceFilename, pageSoup, status)
        tags, status = self.__parseElement("getArticleTags", articleSourceFilename, pageSoup, status)
        authors, status = self.__parseElement("getArticleAuthors", articleSourceFilename, pageSoup, status)

        article = Article(globalID = globalID, publisher = publisher, url = url, date = date, text = text, \
                          language = language, heading = heading, summary = summary, \
                          tags = tags, authors = authors)
        return article, status

    def __parseElement(self, elementName, articleSourceFilename, pageSoup, status):
        # Call the derived methods to extract elements from the pageSoup
        # Enclose the logic in a try catch block and complain if the method fails
        response = None
        try:
            response = getattr(self, elementName)(articleSourceFilename, pageSoup)

            # set date format
            if elementName is "getArticleDate":
                if isinstance(response, datetime):
                    date = str('%02d' % response.day) + "-" + str('%02d' % response.month) + "-" + str(response.year)
                    return date, status

            # Specific assertions
            if elementName is "getArticleUrl":
                if response is None or not response.strip().startswith("http"):
                    status += "Error: Url is not valid: " + str(response) + "\n"

            if elementName is "getArticleHeading":
                if response is None or len(response.strip()) < 3:
                    status += "Error: Article heading not captured properly: " + str(response) + "\n"

            if elementName is "getArticleText":
                if response is None or len(response.strip()) < 10:
                    status += "Error: Article text not captured properly: " + str(response) + "\n"

            if elementName is "getArticleDate":
                if not isinstance(response, datetime):
                    status += "Error: Invalid time type: " + str(response) + "\n"


        except:
            # print ("Error parsing " + elementName + "(...) of " + articleSourceFilename)
            status += "Error parsing " + elementName + "\n"
        return response, status

    @abstractmethod
    def getPublisher(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleUrl(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleDate(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleText(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleLanguage(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleHeading(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleSummary(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleTags(self, articleSourceFilename, pageSoup):
        pass

    @abstractmethod
    def getArticleAuthors(self, articleSourceFilename, pageSoup):
        pass




def loadConfiguration(configFilePath, params):
    print ("Loading config file: " + configFilePath)
    # Extract config data from config file
    if os.path.exists(configFilePath):
        config = yaml.load(open(configFilePath))

        # Check for elements in the config file
        for param in params:
            if param not in config:
                print("Error: " + param + " missing in config file")
                exit

        configurations = []
        for param in params:
            configurations.append(config[param])
        return configurations
    else:
        print ("config file does not exist")
        exit

# TODO: Find a good home for this function
def loadDataset(inputFolders):
    articleFiles = []
    for inputFolder in inputFolders:
        for filename in glob.iglob(inputFolder + '/**/*.yaml', recursive=True):
            articleFiles.append(filename)
        for filename in glob.iglob(inputFolder + '/**/*.json', recursive=True):
            articleFiles.append(filename)

    # TODO: Treat ArticleWithFeatures as a first-class citizen

    dataset = []
    for articleFile in articleFiles:

        if os.path.exists(articleFile):
            fileDict = None
            if articleFile.endswith(".yaml"):
                fileDict = yaml.load(open(articleFile))
            if articleFile.endswith(".json"):
                with open(articleFile) as jsonFile:
                    fileDict = json.load(jsonFile)

            # Check if all Article and Feature elements are present
            if fileDict is not None:
                dataset.append(fileDict)

    return dataset
