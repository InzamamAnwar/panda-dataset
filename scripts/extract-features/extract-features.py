# -*- coding: utf-8 -*-
"""
Created on Sat Aug 18 17:53:07 2018

- Take in list of directories and recursively go into sub-directories
- Create a list of yaml/json files
- for each file, load data, run feature functions and save results
    in an output directory with appending x-with-features.y as filename

"""
import sys
sys.path.append('features/')
sys.path.append('../common/')
import common

import glob
import pdb
import yaml
import json

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\extract-features.yaml"

outputFolder = None
inputFolders = []
features = None
outputTypeString = None

print ("Loading config file: " + configFilePath)
# Extract config data from config file
if os.path.exists(configFilePath):
    config = yaml.load(open(configFilePath))

    params = ["outputFolder", "inputFolders", "features", "outputType"]
    # Check for elements in the config file
    for param in params:
        if param not in config:
            print("Error: " + param + " missing in config file")
            exit

    outputFolder = config["outputFolder"]
    inputFolders = config["inputFolders"]
    features = config["features"]
    outputTypeString = config["outputType"]

else:
    print ("config file does not exist")
    exit

# Create folder if not exists
if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

# Set output type
outputType = None
if outputTypeString.lower() == "yaml":
    outputType = common.OutputType.YAML
elif outputTypeString.lower() == "json":
    outputType = common.OutputType.JSON
else:
    print ("Error: Invalid outputType")

# Get a list of article files
articleFiles = []
for inputFolder in inputFolders:
    for filename in glob.iglob(inputFolder + '/**/*.yaml', recursive=True):
        articleFiles.append(filename)
    for filename in glob.iglob(inputFolder + '/**/*.json', recursive=True):
        articleFiles.append(filename)

for articleFile in articleFiles:

    if os.path.exists(articleFile):
        articleDict = None
        if articleFile.endswith(".yaml"):
            articleDict = yaml.load(open(articleFile))
        if articleFile.endswith(".json"):
            with open(articleFile) as jsonFile:
                articleDict = json.load(jsonFile)

        # Check if all Article elements are present
        if articleDict is not None:

            tempArticle = common.Article()
            for element in vars(tempArticle):
                if element not in articleDict:
                    print ("Error: Missing Element " + element + " while processing " + article)

            # Load article elements
            articleName = articleDict["name"]
            publisher = articleDict["publisher"]
            url = articleDict["url"]
            localID = articleDict["localID"]
            date = articleDict["date"]
            text = articleDict["text"]
            language = articleDict["language"]
            heading = articleDict["heading"]
            summary = articleDict["summary"]
            tags = articleDict["tags"]
            authors = articleDict["authors"]

            article = common.Article(name = articleName, publisher = publisher, url = url, \
                                     localID = localID, date = date, text = text, \
                                     language = language, heading = heading, \
                                     summary = summary, tags = tags, authors = authors)

            featuresObject = {}
            for featureName in features:
                # Dynamically load the right feature class
                fetureModule = dynamicImport(featureName)
                featureClass = getattr(fetureModule, featureName)()
                # Extract feature
                try:
                    featureDict = featureClass.extract(article)
                    featuresObject[featureName] = featureDict
                except:
                    print ("Error: while extracting feature " + featureName + " for article " + articleFile)

            output = {}
            output["article"] = article.__dict__
            output["features"] = featuresObject

            # Output To File
            # TODO: The following logic is common here and in common.py->Article.save(..)
            # TODO: Refactor this and put in a common location
            fileContents = None
            extension = None
            if outputType == common.OutputType.YAML:
                fileContents = yaml.dump(output, default_flow_style = False)
                extension = ".yaml"
            elif outputType == common.OutputType.JSON:
                fileContents = json.dumps(output)
                extension = ".json"

            # Generate filename
            filename = articleName + ".features"

            fullPath = os.path.join(outputFolder, filename + extension)
            outputFile = open(fullPath, 'w+')
            outputFile.write(fileContents)
            outputFile.close()

    else:
        print ("Error: Following article does not exist -> " + article)

print ("Done")
