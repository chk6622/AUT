#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 24, 2018

@author: xingtong
'''

from xploreapi import XPLORE
import json



'''
Key Rate Limits
10    Calls per second
200    Calls per day
'''
class IeeeApiSpider(object):
    API_KEY=r'mghspz84xgsy6sawfgn3tm7k'
    QUERY_RETURN_MAX_RESULTS=2  #max is 200
    MAX_QUERY_LIMIT=200
    TOTAL_MAX_RESULT=0
    
    def __init__(self,apiKEY=None,queryReturnMaxResult=None):
        if apiKEY:
            self.API_KEY=apiKEY
        if queryReturnMaxResult:
            self.QUERY_RETURN_MAX_RESULTS=queryReturnMaxResult
        self.TOTAL_MAX_RESULT=self.MAX_QUERY_LIMIT*self.QUERY_RETURN_MAX_RESULTS
    
    def queryData(self, keyWords):
        '''
        query ieee xplore database to get results
        @param keyWords: key words
        @return: a list which contains query results, and every result is the json formate. The max results count is 40000  
        '''
        lReturn=[]
        try:
            begin=0  #query start record number
            query=XPLORE(self.API_KEY)
            query.maximumResults(self.QUERY_RETURN_MAX_RESULTS)
            query.queryText(keyWords)
            while True:
                query.startingResult(begin)
                results = query.callAPI(debugModeOff=True)
                articles=self.getArticles(results)  #get articles list
                if articles:
                    lReturn.append(articles)  # add articles to result list
                    size=len(articles)  #get query total number
                    if size==self.MAX_RESULTS and size <= self.TOTAL_MAX_RESULT:  #if still has more articles,continue query
                        begin=len(lReturn)+1
                    else:
                        break
                else:
                    break
        except Exception, err:
            print err
        return lReturn
    
    def getArticles(self, jsonResponse):
        '''
        get query articles
        @param jsonResponse: the query results which are from ieee xplore database
        @return: a list which contains article data 
        '''
        pReturn=None
        try:
            if jsonResponse:
                jdatas=json.loads(jsonResponse)
                if jdatas:
                    pReturn=jdatas.get('articles')
        except Exception, err:
            print err
        return pReturn
    
    def getPdfUrl(self, jsonResult):
        '''
        get pdf file url from article data
        @param jsonResult: article data which is json format
        @return: the pdf url of the article
        '''
        uReturn=None
        try:
            if jsonResult:
                uReturn=jsonResult['pdf_url']
        except Exception,err:
            print err
        return uReturn

    
if __name__ == '__main__':
    keyWords=r'sworm'
    idf=IeeeApiSpider()
    idf.queryData(keyWords)

    