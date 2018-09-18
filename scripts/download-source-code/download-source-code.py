# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 01:45:32 2018
"""

import sys
sys.path.append('../common/')
import common

import glob
import os
from enum import Enum
import time
import pdb
import yaml
import json
import datetime

def getSourceCode(inputFilepath):
    sourceCode = None
    with open(inputFilepath, 'r', encoding="utf8") as inputFile:
        sourceCode = inputFile.read()
    return sourceCode

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\download-source-code.yaml"

outputFolderPath = None
outputTypeString = None
dataSources = []

print ("Loading config file: " + configFilePath)
# Extract config data from config file
if os.path.exists(configFilePath):
    config = yaml.load(open(configFilePath))

    params = ["outputFolderPath", "outputType", "dataSources"]
    # Check for elements in the config file
    for param in params:
        if param not in config:
            print("Error: " + param + " missing in config file")
            exit

    outputFolderPath = config["outputFolderPath"]
    outputTypeString = config["outputType"]
    dataSources = config["dataSources"]

else:
    print ("config file does not exist")
    exit

# Create folder if not exists
if not os.path.exists(outputFolderPath):
    os.makedirs(outputFolderPath)
    
# Set output type
outputType = None
if outputTypeString.lower() == "yaml":
    outputType = common.OutputType.YAML
elif outputTypeString.lower() == "json":
    outputType = common.OutputType.JSON
    
# TODO: Only supporting GET requests for now
# For POST requests, set config.yaml format to set get/post and post data for each url    
for dataSource in dataSources:
    
    publisher = dataSource['publisher']
    inputFolders = dataSource['inputFolders']
    
    # Get a list of article files
    articleSourceFiles = []
    for inputFolder in inputFolders:
        for filename in glob.iglob(inputFolder + '/**/*.html', recursive=True):
            articleSourceFiles.append(filename)

    # For each article    
    for articleSourceFile in articleSourceFiles:
        print ("working on: " + articleSourceFile)
        startTime = time.time()
        sourceCode = getSourceCode(articleSourceFile)
    
        # Generate filename
        sourceFilename = os.path.basename(articleSourceFile)
        # Remove extension
        sourceFilename = os.path.splitext(sourceFilename)[0]
        filename = publisher + "+" + sourceFilename + ".src"
        
        outputData = {}
        # TODO: Can we extract the url of the article given the source code?
        outputData['articleUrl'] = None
        outputData['articleName'] = publisher + "+" + sourceFilename
        outputData['publisher'] = publisher
        outputData['sourceCode'] = sourceCode
        outputData['timeDownloaded'] = str(datetime.datetime.now())
        

        # Output To File
        # TODO: The following logic is common here and in common.py->Article.save(..)
        # TODO: Refactor this and put in a common location
        fileContents = None
        extension = None
        if outputType == common.OutputType.YAML:
            fileContents = yaml.dump(outputData, default_flow_style = False)
            extension = ".yaml"
        elif outputType == common.OutputType.JSON:
            fileContents = json.dumps(outputData)
            extension = ".json"
    
        fullPath = os.path.join(outputFolderPath, filename + extension)
        outputFile = open(fullPath, 'w+')
        outputFile.write(fileContents)
        outputFile.close()
        
        endTime = time.time()
        timeTaken = endTime - startTime
        print ("file saved. Time taken: " + str("%.2f" % timeTaken))


