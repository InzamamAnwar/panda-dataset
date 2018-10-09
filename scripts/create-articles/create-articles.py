# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 16:22:20 2018
"""

import sys
sys.path.append('publishers/')
sys.path.append('../common/')
import common

import os
import yaml
import glob
import time
import pdb
from multiprocessing.dummy import Pool as ThreadPool
import threading

startTime = time.time()

if len(sys.argv) is 1:
    print ("Error: Please specify the config file path")
    sys.exit()

# Get config filepath from command-line parameter
configFilePath = sys.argv[1]
# configFilePath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\configurations\\create-articles.yaml"

# Load Configuration data
outputFolderPath, inputSources, chunkSize, threads = common.loadConfiguration(configFilePath, ["outputFolderPath", "inputSources", "chunkSize", "threads"])

# Create folder if not exists
if not os.path.exists(outputFolderPath):
    os.makedirs(outputFolderPath)

def saveArticleToDataset(articleSourceFile):
    global fileID
    global globalID
    global datasetForCurrentFeature

    if not os.path.exists(articleSourceFile):
        print ("Error: file does not exists: " + articleSourceFile)
        return

    # Fix: 123
    articleSourceCode = None
    try:
        articleSourceCode = open(articleSourceFile,"r", encoding='utf8').read()
    except Exception as e:
            print ("Error opening file: " + articleSourceFile + "\n" + str(e) + "\n\n")
            return

    article, status = publisherClass.createArticleObject(globalID = None, \
                                                         articleSourceFilename = articleSourceFile, \
                                                         articleSourceCode = articleSourceCode)

    # Write file to dataset only if status == ""
    if len(status) > 0:
        print ("File: " + articleSourceFile)
        print (status)
        return


    lock.acquire()
    # setting the globalID here instead of article constructor to enable multiple thread create articles
    # without worrying about unique globalIDs
    article.globalID = globalID
    yamlOutput = "---\n" + yaml.dump(article.__dict__, default_flow_style = False) + "\n"
    datasetForCurrentFeature.append(yamlOutput)
    globalID += 1

    # Add publisher count
    if publisherName in publisherCounts:
        publisherCounts[publisherName] += 1
    else:
        publisherCounts[publisherName] = 0
    # Print update on every 1000th article, might be useful if scripts crashes for some reason
    if globalID % chunkSize == 0:
        fullPath = os.path.join(outputFolderPath, "dataset-" + str(fileID) + ".yaml")
        outputFile = open(fullPath, 'w+')
        outputText = "\n".join(datasetForCurrentFeature)
        outputFile.write(outputText)
        outputFile.close()
        fileID += 1
        # Clear the current feature buffer
        datasetForCurrentFeature = []

    lock.release()

# Get a list of article files
'''
File filtered on 3 parameters
- must end with .html
- must be larger than 3KB in size
- cannot have amp as a folder in its path
'''

publisherCounts = {}
fileID = 1
globalID = 1

# Create a lock
lock = threading.Lock()

datasetForCurrentFeature = []

for inputSource in inputSources:

    publisherName = inputSource['publisher']
    inputFolder = inputSource['folder']

    articleSourceFiles = []
    for filename in glob.iglob(inputFolder + '/**/*.html', recursive=True):
        if "/amp/" not in filename and "\\amp\\" not in filename:
            if os.path.getsize(filename) > 3 * 1024:
                articleSourceFiles.append(filename)

    # Dynamically load the right publisher
    publisherModule = common.dynamicImport(publisherName)
    if publisherModule is None:
        print ("Error: Publisher class '" + publisherName + "' not found" )
        continue
    publisherClass = getattr(publisherModule, publisherName)()

    '''
    Logic:
    For each file:
        get the file contents
        get publisher name
        create article object
        log errors and warnings
        save article object in output folder in yaml/json format
    '''

    # for articleSourceFile in articleSourceFiles:
    #     saveArticleToDataset(articleSourceFile)

    # Make the Pool of workers
    pool = ThreadPool(threads)
    # Extract Feature for given article
    featureForDataset = pool.map(saveArticleToDataset, articleSourceFiles)
    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

# Add left over articles to a new dataset file
if len(datasetForCurrentFeature) > 0:
    fullPath = os.path.join(outputFolderPath, "dataset-" + str(fileID) + ".yaml")
    outputFile = open(fullPath, 'w+')
    outputFile.write("\n".join(datasetForCurrentFeature))
    outputFile.close()

endTime = time.time()
print ("Time taken: " + str(endTime - startTime) + " for " + str(globalID) + " articles\n\n")
print ("Summary: ")
for publisher in publisherCounts:
    print ("name: " + str(publisher) + ", count: " + str(publisherCounts[publisher]))

print ("\nDone")
