#!/usr/bin/env python
#coding: utf-8
'''
Created on Aug 30, 2018

@author: xingtong
'''
import sys,os,time
from multiprocessing.queues import SimpleQueue as Queue
from multiprocessing.queues import Queue
from ProcessUnit import ProcessUnit
from logger.Statistics import Statistics
from model.StopSignal import StopSignal
from logger.StreamLogger import StreamLogger
from logger.LogConfig import appLogger
from model.StreamBox import StreamBox


class ProcessScheduler(object):
    def __init__(self,streamLineTemplate,processQueueSize=10):
        self.streamLineTemplate=streamLineTemplate
        self.processQueueSize=processQueueSize
        
    def CreateSteamLine(self):
        '''
        create stream line
        @return: a list which contains all processes and streamline output queue
        '''
        processUnitList=[]
        inputQueue=None
        outputQueue=None
        processUnit=None
        if self.streamLineTemplate:
            for (index,processTemplate) in enumerate(self.streamLineTemplate):
                outputQueue=Queue(maxsize=self.processQueueSize)
                pCount=processTemplate.get('pCount')  # get process number
                if index==0:
                    for ind in xrange(pCount):
                        processUnit=ProcessUnit(processTemplate,outputQueue=outputQueue) #create producer process
                        processUnitList.append(processUnit)
                else:
                    for ind in xrange(pCount):
                        processUnit=ProcessUnit(processTemplate,inputQueue=inputQueue,outputQueue=outputQueue)  #create consumer process
                        processUnitList.append(processUnit)
                inputQueue=outputQueue
        return processUnitList,outputQueue
    
    def execute(self):
        '''
        main function to execute this app
        '''
        if self.streamLineTemplate:
            pTotalCount=1  #the total number of process
            processes=[]
            tmpInfo=''
            for index,process in enumerate(self.streamLineTemplate):
                pCount=process.get('pCount')  #process number
                pTotalCount+=pCount
                thread=process.get('Thread')  #thread number
                processes.append([pCount,thread])
            tmpInfo+= 'starts  %s process(including main process)\n' % pTotalCount
            for i,p in enumerate(processes):
                tmpInfo+= 'process stage %d starts %d process:\n' % (i+1,p[0])
                tmpInfo+= 'every bizprocessor thread in the process is the following：\n'
                if i==0:
                    thread=p[1]
                    tmpInfo+= '%40s.%40s * %s\n' % (thread[0],thread[1],thread[2])
                else:
                    for thread in p[1]:
                        tmpInfo+= '%40s.%40s * %d\n' % (thread[0],thread[1],thread[2])
            appLogger.info(tmpInfo)
            
        processList,outputQueue=self.CreateSteamLine()
        for process in processList:
            process.start()  #start processor
        
        process_record=0
        stat=Statistics()
        while True:
            streamBox=outputQueue.get()
            if streamBox:
                if isinstance(streamBox, StreamLogger):
                    stat.addProcessorLog(streamBox)
                if not isinstance(streamBox, StopSignal):
                    process_record+=1
                    if process_record%2==0:
                        appLogger.info('\n%s' % stat.getStatisticInfo())  #print log
                else:
                    time.sleep(20)
                    break
                del(streamBox)
        for process in processList:
            process.terminate()
            process.join()
        appLogger.info('\n%s' % stat.getStatisticInfo())
        appLogger.info('%s thread stop' % self.__class__.__name__)
        appLogger.info('the app stop')          