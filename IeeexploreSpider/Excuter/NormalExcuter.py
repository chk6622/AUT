#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 26, 2018

@author: xingtong
'''
from IeeexploreSpider.ApiSpider import IeeeApiSpider
from IeeexploreSpider.WebPageSpider import WebPageSpider
from dao.MongoDBDAO import MongoDBDAO

if __name__ == '__main__':
    keyWords='swarm'
#     maxQueryCount=200
#     todayQueryCount=0
    apiSpider=IeeeApiSpider()
    webPageSpider=WebPageSpider()
    mongoDBDAO=MongoDBDAO()
    while apiSpider.CUR_QUERY_COUNT<=apiSpider.MAX_QUERY_LIMIT:
        
        results=apiSpider.queryData(keyWords)
        for result in results:
            pdfUrl=apiSpider.getPdfUrl(result)
            pdfRealUrl=webPageSpider.getRealPdfUrl(pdfUrl)
            fileName=result['filename']
            fileTempPath=webPageSpider.generateTempFilePath(fileName)
            fileId=''
            if webPageSpider.getPdfFile(pdfRealUrl, fileTempPath):  #if get pdf file success then save the file into the database
                fileId=mongoDBDAO.insertFile(fileTempPath, fileName)
            result['fileId']=fileId  #set fileId in the result
            mongoDBDAO.insertOneData(**result)  #save a result into the database
        if not results or len(results)==0:
            break
    
    