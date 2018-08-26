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



if __name__ == '__main__':
    
    url=r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6931434&tag=1'
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    filename = 'cookie.txt'
    #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    #模拟登录，并把cookie保存到变量
    result = opener.open(url)
#     print result.read()
    #保存cookie到cookie.txt中
#     cookie.save(ignore_discard=True, ignore_expires=True)
    #利用cookie请求访问另一个网址，此网址是成绩查询网址
#     gradeUrl = r'https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6931434&tag=1'
    #请求访问成绩查询网址
    result = opener.open(url)
    soup = BeautifulSoup(result)
    pdfUrl=soup.iframe.attrs.get('src')
    print soup.iframe
    print pdfUrl
    result = opener.open(url)
    soup = BeautifulSoup(result)
    pdfUrl=soup.iframe.attrs.get('src')
    print soup.iframe
    print pdfUrl
    result = opener.open(url)
#     print result.read()
    
#     response = urllib2.urlopen(request).read()
#     print response
    soup = BeautifulSoup(result)
    pdfUrl=soup.iframe.attrs.get('src')
    print soup.iframe
    print pdfUrl
    
#     r = requests.get(pdfUrl, stream=True)
#     f = open("06877226.pdf", "wb")
#     for chunk in r.iter_content(chunk_size=512):
#         if chunk:
#             f.write(chunk)
 
    #设置超时时间为30s
#     socket.setdefaulttimeout(30)
    #解决下载不完全问题且避免陷入死循环
#     try:
#         urllib2.request.urlretrieve(url,image_name)
#     except socket.timeout:
#         count = 1
#         while count <= 5:
#             try:
#                 urllib.request.urlretrieve(url,image_name)                                                
#                 break
#             except socket.timeout:
#                 err_info = 'Reloading for %d time'%count if count == 1 else 'Reloading for %d times'%count
#                 print(err_info)
#                 count += 1
#         if count > 5:
#             print("downloading picture fialed!")
#     headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
#     timeout=1000
#     letters_list={}
#     response = urllib2.urlopen(targetUrl)
#     webPage=response.read()
#     
#     request = urllib2.Request(targetUrl)
#     request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
#     response = urllib2.urlopen(request).read()
#     print response
#     urllib.urlretrieve(targetUrl, "test.pdf")
#     soup = BeautifulSoup(webPage) 
#     letters=soup.find_all('ul',attrs={'class': 'results'}).select('li')
#     for letter in letters:
#         authors=''
#         for author in letter.find_all('a',attrs={'class': 'authorPreferredName prefNameLink'}):
#             authors=authors+author.get_text()+';'
#         authors=''.join(authors.split())
#         title=letter.find('a',attrs={'class': 'art-abs-url'}).get_text().replace('\n','')
#         letters_list[title]=[authors,'http://ieeexplore.ieee.org'+letter.find('img',attrs={'alt': 'HTML icon'}).parent['href'],'http://ieeexplore.ieee.org'+letter.find('img',attrs={'alt': 'PDF file icon'}).parent['href']]
#         print soup.select(r'.List-results-items ng-scope')
    



    
    
    