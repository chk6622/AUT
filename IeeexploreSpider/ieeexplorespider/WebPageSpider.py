#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 21, 2018

@author: xingtong
'''
import urllib2
import urllib
from bs4 import BeautifulSoup
import socket
import requests
import cookielib
import os
from utiles.PrintTool import PrintTool
from logger.logConfig import appLogger

class WebPageSpider(object):
    
    MAIN_PAGE_URL=r'https://www.ieee.org/'
    COOKIE_PATH=r'../temp/cookie.txt'
    TEMP_DOC_PATH=r'../temp/'
    
    def __init__(self,mainPageUrl=None,cookiePath=None,tempDocPath=None):
        if mainPageUrl:
            self.MAIN_PAGE_URL=mainPageUrl
        if cookiePath:
            self.COOKIE_PATH=cookiePath
        if tempDocPath:
            self.TEMP_DOC_PATH=tempDocPath
       
        try:
            if not os.path.exists(self.COOKIE_PATH):  #if cookie is not exist
                #claim a MozillaCookieJar instance to save cookie
                cookie = cookielib.MozillaCookieJar(self.COOKIE_PATH)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                #access main page, and save attributes to the cookie
                opener.open(self.MAIN_PAGE_URL)
                #save cookie
                cookie.save(ignore_discard=True, ignore_expires=True)
        except Exception, err:
            appLogger.error(err)
        
    def generateTempFilePath(self,fileName):
        '''
        get temp file path
        @param fileName:temp file name
        @return: temp file path  
        '''
        sReturn=None
        if fileName:
            sReturn=self.TEMP_DOC_PATH+fileName
        return sReturn
    
    def getRealPdfUrl(self,pdfUrl):
        '''
        get real pdf url by pdfUrl
        @param pdfUrl: the pdfUrl which is gotten from ieee xplore api
        @return: real pdf url
        '''
        sReturn=None
        try:
            if pdfUrl:
#                 pt=PrintTool()
                
                #claim a MozillaCookieJar instance to save cookie
                cookie = cookielib.MozillaCookieJar(self.COOKIE_PATH)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                #access pdfUrl
#                 pt.printStartMessage('get real pdf url from the internet')
                result = opener.open(pdfUrl)
#                 pt.printEndMessage('get real pdf url from the internet')
                soup = BeautifulSoup(result,features='lxml')
                sReturn=soup.iframe.attrs.get('src')  #get real pdf url
        except Exception, err:
            appLogger.error(err)
        return sReturn
#            
    def getPdfFile(self,pdfRealUrl,filePath):
        '''
        get pdf file by pdf real url
        @param pdfRealUrl:pdf file's real url
        @param filePath:local disk path which will save pdf file
        @return: success return true, or return false  
        '''
        bReturn=False
        f=None
        try:
            response = requests.get(pdfRealUrl, stream=True)
            f = open(filePath, "wb")
            for chunk in response.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
            appLogger.info('success get file from the internet. the file size is %s bytes' % os.path.getsize(filePath))
            bReturn=True
        except Exception, err:
            appLogger.error(err)
        finally:
            if f:
                f.close()
        return bReturn


if __name__ == '__main__':
    print os.path.getsize('../temp/8359016.pdf')
#     spider=WebPageSpider()
#     realUrl=spider.getRealPdfUrl(r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6931434')
#     pdfUrl='https://ieeexplore.ieee.org/ielx5/74/5723204/05723276.pdf?tp=&arnumber=5723276&isnumber=5723204'
#     print spider.getPdfFile(pdfUrl,'../temp/test.pdf')
    
#     print spider.getRealPdfUrl(r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=5723276')
    
#     url=r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6931434&tag=1'
#     request = urllib2.Request(url)
#     request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
#     filename = 'cookie.txt'
#     #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
#     cookie = cookielib.MozillaCookieJar(filename)
#     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#     #模拟登录，并把cookie保存到变量
#     result = opener.open(url)
# #     print result.read()
#     #保存cookie到cookie.txt中
# #     cookie.save(ignore_discard=True, ignore_expires=True)
#     #利用cookie请求访问另一个网址，此网址是成绩查询网址
# #     gradeUrl = r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6931434&tag=1'
#     #请求访问成绩查询网址
#     result = opener.open(url)
#     soup = BeautifulSoup(result)
#     pdfUrl=soup.iframe.attrs.get('src')
#     print soup.iframe
#     print pdfUrl
#     result = opener.open(url)
#     soup = BeautifulSoup(result)
#     pdfUrl=soup.iframe.attrs.get('src')
#     print soup.iframe
#     print pdfUrl
#     result = opener.open(url)
# #     print result.read()
#     
# #     response = urllib2.urlopen(request).read()
# #     print response
#     soup = BeautifulSoup(result)
#     pdfUrl=soup.iframe.attrs.get('src')
#     print soup.iframe
#     print pdfUrl
#     
#     r = requests.get(pdfUrl, stream=True)
#     f = open("06877226.pdf", "wb")
#     for chunk in r.iter_content(chunk_size=512):
#         if chunk:
#             f.write(chunk)
#  
#     #设置超时时间为30s
# #     socket.setdefaulttimeout(30)
#     #解决下载不完全问题且避免陷入死循环
# #     try:
# #         urllib2.request.urlretrieve(url,image_name)
# #     except socket.timeout:
# #         count = 1
# #         while count <= 5:
# #             try:
# #                 urllib.request.urlretrieve(url,image_name)                                                
# #                 break
# #             except socket.timeout:
# #                 err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
# #                 print(err_info)
# #                 count += 1
# #         if count > 5:
# #             print("downloading picture fialed!")
# #     headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
# #     timeout=1000
# #     letters_list={}
# #     response = urllib2.urlopen(targetUrl)
# #     webPage=response.read()
# #     
# #     request = urllib2.Request(targetUrl)
# #     request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
# #     response = urllib2.urlopen(request).read()
# #     print response
# #     urllib.urlretrieve(targetUrl, "test.pdf")
# #     soup = BeautifulSoup(webPage) 
# #     letters=soup.find_all('ul',attrs={'class': 'results'}).select('li')
# #     for letter in letters:
# #         authors=''
# #         for author in letter.find_all('a',attrs={'class': 'authorPreferredName prefNameLink'}):
# #             authors=authors+author.get_text()+';'
# #         authors=''.join(authors.split())
# #         title=letter.find('a',attrs={'class': 'art-abs-url'}).get_text().replace('\n','')
# #         letters_list[title]=[authors,'http://ieeexplore.ieee.org'+letter.find('img',attrs={'alt': 'HTML icon'}).parent['href'],'http://ieeexplore.ieee.org'+letter.find('img',attrs={'alt': 'PDF file icon'}).parent['href']]
# #         print soup.select(r'.List-results-items ng-scope')
    



    
    
    