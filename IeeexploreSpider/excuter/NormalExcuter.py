#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 26, 2018

@author: xingtong
'''
from ieeexplorespider.ApiSpider import IeeeApiSpider
from ieeexplorespider.WebPageSpider import WebPageSpider
from dao.MongoDBDAO import MongoDBDAO
from utiles.PrintTool import PrintTool
from ConfigParser import ConfigParser

def getDatabase(appConfig):
    dbName=appConfig.get('DB', 'DB_NAME')
    dbHost=appConfig.get('DB', 'DB_HOST')
    dbPort=appConfig.get('DB', 'DB_PORT')
    dbUser=appConfig.get('DB', 'DB_USER')
    dbPass=appConfig.get('DB', 'DB_PASS')
    dbColl=appConfig.get('DB', 'DB_COLL')
    dbBinColl=appConfig.get('DB', 'DB_COLL_BIN')
    return MongoDBDAO(dbName,dbHost,dbPort,dbUser,dbPass,dbColl,dbBinColl)

def getWebPageSipder(appConfig):
    mainPageUrl=appConfig.get('WebPageSpider','MAIN_PAGE_URL')
    cookiePath=appConfig.get('WebPageSpider','COOKIE_PATH')
    tempDocPath=appConfig.get('WebPageSpider','TEMP_DOC_PATH')
    return WebPageSpider(mainPageUrl,cookiePath,tempDocPath)

def getApiSpider(appConfig):
    apiKey=appConfig.get('ApiSpider','API_KEY')
    queryReturnMaxResult=appConfig.getint('ApiSpider','QUERY_RETURN_MAX_RESULTS')
    maxQueryCountLimit=appConfig.getint('ApiSpider','MAX_QUERY_COUNT_LIMIT')
    return IeeeApiSpider(apiKey,queryReturnMaxResult,maxQueryCountLimit)

def getKeywords(appConfig):
    aReturn=None
    keyWords=appConfig.get('KayWords','KEY_WORDS')
    if keyWords:
        aReturn=keyWords.split(',')
    return aReturn

if __name__ == '__main__':
    #initialize app
    configFilePath='../config.txt'
    cf = ConfigParser()
    cf.read(configFilePath)
    keyWords=getKeywords(cf)
    pt=PrintTool()
    pt.printStartMessage('initiate')
    apiSpider=getApiSpider(cf)
    webPageSpider=getWebPageSipder(cf)
    mongoDBDAO=getDatabase(cf)
    
    #
    pt.printEndMessage('initiate')
    pt.printStartMessage('processes')
    for keyWord in keyWords:
        print '------------------------------------------------------------'
        pt.printStartMessage('query articles by keywords:'+keyWord)
        results=apiSpider.queryData(keyWord)
        pt.printEndMessage('query articles by keywords:'+keyWord)
        if not results or len(results)==0:
            print 'Results number is 0'
            break
        else:
            print 'Results number is %d' % len(results)
        pt.printStartMessage('processes result set')
        resultNum=0
        for result in results:
            print '----------------------------%d--------------------------------' % resultNum
            resultNum+=1
            pt.printStartMessage('processes result:')
            pt.printStartMessage('gets pdf url')
            pdfUrl=apiSpider.getPdfUrl(result)
#             print pdfUrl
            pdfRealUrl=webPageSpider.getRealPdfUrl(pdfUrl)
#             print pdfRealUrl
            pt.printEndMessage('gets pdf url')
            pt.printStartMessage('gets pdf file')
            fileName=result.get('article_number')+'.pdf'
            fileTempPath=webPageSpider.generateTempFilePath(fileName)
            fileId=''
            flag=webPageSpider.getPdfFile(pdfRealUrl, fileTempPath)
            pt.printEndMessage('gets pdf file')
            if flag:  #if get pdf file success then save the file into the database
                pt.printStartMessage('inserts pdf file into the database')
                fileId=mongoDBDAO.insertFile(fileTempPath, fileName, isDelFile=True)
                pt.printEndMessage('inserts pdf file into the database')
            pt.printStartMessage('inserts articles into the database')
            result['fileId']=fileId  #set fileId in the result
            mongoDBDAO.insertOneData(**result)  #save a result into the database
            pt.printEndMessage('inserts articles into the database')
            pt.printEndMessage('processes result:')
            print '---------------------------%d---------------------------------' % resultNum
        pt.printEndMessage('processes result set')
        print '-------------------------------------------------------------'
    pt.printEndMessage('processes')
    