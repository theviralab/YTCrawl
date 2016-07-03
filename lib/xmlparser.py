# -*- coding: utf-8 -*-
"""
  The crawler to download YouTube video viewcount history
"""
# Author: Honglin Yu <yuhonglin1986@gmail.com>
# Author: Carlos Afonso <carlos.afonso@glucompany.com>
# License: BSD 3 clause

import datetime
from xml.etree import ElementTree
import json

def parseString(s):
    tree = ElementTree.fromstring(s)
    graphData = tree.find('graph_data')

    if graphData == None:
        raise Exception("can not find data in the xml response")

    jsonDict = json.loads(graphData.text)

    return processResult(jsonDict)

def processResult(jsonDict):
    # get days
    rawdate = [ datetime.date(1970,1,1) + datetime.timedelta( x/86400000 ) for x in  jsonDict['day']['data'] ]

    res = {}
    metrics = ['shares', 'views', 'subscribers', 'watch-time']
    for i, j in enumerate(rawdate):
        data_point = {}

        for m in metrics:
            if m not in jsonDict:
                continue

            data_point[m] = {
                'daily': jsonDict[m]['daily']['data'][i],
                'cumulative': jsonDict[m]['cumulative']['data'][i]
            }


        res[j.strftime('%Y-%m-%d')] = data_point

    return res
