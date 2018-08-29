#!/usr/bin/env python
#_*_coding:utf-8_*_
'''
2016-6-8 下午3:23:30
XingTong
'''
import sys,time
from log.StreamLogger import StreamLogger

#修改系统的默认编码模式为utf-8
reload(sys)
sys.setdefaultencoding('utf-8')

class Statistics(object):
    
    def __init__(self):
        self.startTime=time.time()  #整条流水线的开始时间
        self.totalTime=0
        self.totalCount=0  #系统处理总数据
        self.totalPod=0  #系统运行总耗时
        self.totalAvg=0  #系统总的平均处理速度 条/s
        self.singlePod=0 #处理单条数据所消耗时间
        
        self.processorList=[]
        self.processorTimeDic={}
        
    def addProcessorLog(self,streamLogger):
        if streamLogger and isinstance(streamLogger, StreamLogger):
            self.totalCount+=1  #系统处理总数据加一
            self.totalPod=time.time()-self.startTime  #计算系统运行总耗时
            self.totalAvg=self.totalCount/self.totalPod  #计算系统总的平均处理速度
            self.singlePod=streamLogger.getTotalPod()
#             print self.singlePod
            
#             print streamLogger.processorList
            for (clazz,beginTime,endTime) in streamLogger.processorList:
                
                if clazz not in self.processorList:
                    self.processorList.append(clazz)  #将处理器类加入处理器列表
                statList=self.processorTimeDic.get(clazz)
                if not statList:
                    statList=[]
                    self.processorTimeDic[clazz]=statList
                pod=endTime-beginTime  #数据在每个处理器中处理的耗时
                if statList:
                    totalPod=pod+statList[1]  #处理器的总耗时
                    avgPod=totalPod/self.totalCount  #处理器平均耗时
                    maxPod=statList[2]   #最高耗时
                    if pod>maxPod:
                        maxPod=pod
                    minPod=statList[3]  #最低耗时
                    if pod<minPod:
                        minPod=pod
                    statList=[]
                    self.processorTimeDic[clazz]=statList
                    statList.append(pod)    #最近一个周期内处理器的耗时
                    statList.append(totalPod) 
                    statList.append(maxPod)
                    statList.append(minPod) 
                    statList.append(avgPod)  
                else:
                    avgPod=totalPod=maxPod=minPod=pod   
                    statList.append(pod)
                    statList.append(totalPod)
                    statList.append(maxPod)
                    statList.append(minPod)
                    statList.append(avgPod)
#                 print '%s,%s,%s,%s' % (clazz,pod,totalPod,avgPod)
#                 statList.append(endTime)
#                 statList.append(beginTime)
                
                
                
    def getStatisticInfo(self):
        sReturn='开始运行时间:%s,总处理时间:%.2f s,处理数据总数:%s条,平均处理速度:%.2f 条/s,处理单条数据所消耗时间:%.3f s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.startTime)),self.totalPod,self.totalCount,self.totalAvg,self.singlePod)
        for key in self.processorList:
            statList=self.processorTimeDic.get(key)
            sReturn+='%-50s:实时耗时%8.3fs；最长耗时%8.3fs；最短耗时%8.3fs；平均耗时%8.3fs\n' % (key,statList[0],statList[2],statList[3],statList[4])
        return sReturn
                