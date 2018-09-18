# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 01:41:59 2018
"""

import sys
sys.path.append('publishers/')
sys.path.append('../common/')
import common

import matplotlib.pyplot as plt;
import numpy as np

inputFolders = ["C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\artifacts\\articles-with-features"]
outputPath = "C:\\Users\\drzah\\Desktop\\newspaper\\newspaper-project\\artifacts\\applications\\tag-vs-article-length.png"

dataset = common.loadDataset(inputFolders)

tags = {}
for article in dataset:
    for tag in article["article"]["tags"]:
        if tag not in tags:
            tags[tag] = [0, 0]
        tags[tag][0] += article["features"]["CountWords"]["totalWords"]
        tags[tag][1] += 1
        
        
tagNames = []
avgLengths = []
for tag in tags:
    tagNames.append(tag)
    avgLengths.append(tags[tag][0] / tags[tag][1])
    
y_pos = np.arange(len(tagNames))
 
plt.rcdefaults()
plt.bar(y_pos, avgLengths, align='center', alpha=0.5)
plt.xticks(y_pos, tagNames)
plt.ylabel('Average Article Length')
plt.title('Tag vs Article Length')
 
plt.savefig(outputPath)
plt.show()