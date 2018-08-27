#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 27, 2018

@author: xingtong
'''

import time

class PrintTool(object):
    '''
    classdocs
    '''
    timeMap={}


    def __init__(self):
        '''
        Constructor
        '''
        
    def printStartMessage(self,message):
        sReturn='Beginning '
        if message:
            sReturn=sReturn + message + '...'
            self.timeMap[message]= int(round(time.time() * 1000))
        print sReturn
        
    def printEndMessage(self,message):
        sReturn='Finishing '
        if message:
            beginTime=self.timeMap.get(message)
            if not beginTime:
                beginTime=int(round(time.time() * 1000))
            endTime=int(round(time.time() * 1000))
            period=endTime-beginTime
            sReturn=sReturn + message + ' spending '+str(period) + 'ms'
        print sReturn
        
        
if __name__ == '__main__':
    pt=PrintTool()
    pt.printStartMessage('abc')
    time.sleep( 1 )
    pt.printStartMessage('abcd')
    time.sleep( 1 )
    pt.printEndMessage('abcd')
    time.sleep( 1 )
    pt.printEndMessage('abc')
        
        
        
        
        
        
        