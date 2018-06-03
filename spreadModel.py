#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 16:35:38 2018

@author: aj
"""
import math


class SpreadModel:
    def __init__(self,G,tmp1,orientation,minThreshold,time,column_order,forwardDecay,reverseDecay,spreadModels,closeness,avg_close,de,avg_degree,betw,average_betweenness):
        self.G=G
        self.orientation=orientation
        self.minThreshold=minThreshold
        self.node=tmp1
        self.forwardDecay=forwardDecay
        self.time=time
        self.column_order=column_order
        self.reverseDecay=reverseDecay
        self.spreadModels=spreadModels
        self.closeness=closeness
        self.avg_close=avg_close
        self.de=de
        self.avg_degree=avg_degree
        self.betw=betw
        self.average_betweenness=average_betweenness
        
    def choose(self):
        model=self.spreadModels
        orientation=self.orientation
        if 'srd' in model:
            if orientation=='1':
                self.spreadCalculate_x()
            elif orientation=='2':
                self.spreadCalculate_y()
            #print 'ran',ran
        if 'ncrd' in model:
            if orientation=='1':
                self.spreadCalculate_closeness_x()
            elif orientation=='2':
                self.spreadCalculate_closeness_y()
        if 'ndrd' in model:
            if orientation=='1':
                self.spreadCalculate_degree_x()
            elif orientation=='2':
                self.spreadCalculate_degree_y()
        if 'nbrd' in model:
            if orientation=='1':
                self.spreadCalculate_betweenness_x()
            elif orientation=='2':
                self.spreadCalculate_betweenness_y()
        if 'ird' in model:
            if orientation=='1':
                self.spreadCalculate_integrated_x()
            elif orientation=='2':
                self.spreadCalculate_integrated_y()
        
        
    
    def spreadCalculate_closeness_x(self):
        G=self.G
        closeness=self.closeness
        avg_close=self.avg_close
        column_order=self.column_order
        tmp1=self.node
        x_all=self.forwardDecay
        time=self.time
        closeness_tmp1=closeness[tmp1]/avg_close
        increase_tmp1=math.pow(float(x_all[column_order]),time)
        increase_tmp1=increase_tmp1*closeness_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
       
    def spreadCalculate_closeness_y(self):
        G=self.G
        closeness=self.closeness
        avg_close=self.avg_close
        column_order=self.column_order
        tmp1=self.node
        y_all=self.reverseDecay
        time=self.time
        closeness_tmp1=closeness[tmp1]/avg_close
        increase_tmp1=math.pow(float(y_all[column_order]),time)
        increase_tmp1=increase_tmp1*closeness_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        y_matrix=G.node[tmp1]['y_matrix']
        y_matrix[time][column_order]+=1
        G.node[tmp1]['y_matrix']=y_matrix
    
          
      
    #此函数用来计算影响传播较小的情况
    def spreadCalculate_x(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        x_all=self.forwardDecay
        time=self.time
        increase_tmp1=math.pow(float(x_all[column_order]),time)
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
       
    def spreadCalculate_y(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        y_all=self.reverseDecay
        time=self.time
        increase_tmp1=math.pow(float(y_all[column_order]),time)
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        y_matrix=G.node[tmp1]['y_matrix']
        y_matrix[time][column_order]+=1
        G.node[tmp1]['y_matrix']=y_matrix
    
    
    
    #此函数考虑节点的度对其的影响
    def spreadCalculate_degree_x(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        x_all=self.forwardDecay
        time=self.time
        de=self.de
        avg_degree=self.avg_degree
        degree_tmp1=de[tmp1]/avg_degree
        increase_tmp1=math.pow(float(x_all[column_order]),time)
        increase_tmp1=increase_tmp1*degree_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
       
    def spreadCalculate_degree_y(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        y_all=self.reverseDecay
        time=self.time
        de=self.de
        avg_degree=self.avg_degree
        degree_tmp1=de[tmp1]/avg_degree
        increase_tmp1=math.pow(float(y_all[column_order]),time)
        increase_tmp1=increase_tmp1*degree_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        y_matrix=G.node[tmp1]['y_matrix']
        y_matrix[time][column_order]+=1
        G.node[tmp1]['y_matrix']=y_matrix
    
    
    #此函数考虑介数的影响
    def spreadCalculate_betweenness_x(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        x_all=self.forwardDecay
        time=self.time
        betw=self.betw
        average_betweenness=self.average_betweenness
        betw_tmp1=betw[tmp1]/average_betweenness
        increase_tmp1=math.pow(float(x_all[column_order]),time)
        increase_tmp1=increase_tmp1*betw_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
       
    
    def spreadCalculate_betweenness_y(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        y_all=self.reverseDecay
        time=self.time
        betw=self.betw
        average_betweenness=self.average_betweenness
        betw_tmp1=betw[tmp1]/average_betweenness
        increase_tmp1=math.pow(float(y_all[column_order]),time)
        increase_tmp1=increase_tmp1*betw_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        y_matrix=G.node[tmp1]['y_matrix']
        y_matrix[time][column_order]+=1
        G.node[tmp1]['y_matrix']=y_matrix
           
    
    
    #此函数同时考虑介数,度,紧密度活性的影响
    def spreadCalculate_integrated_x(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        x_all=self.forwardDecay
        time=self.time
        betw=self.betw
        average_betweenness=self.average_betweenness
        de=self.de
        avg_degree=self.avg_degree
        closeness=self.closeness
        avg_close=self.avg_close
        close_tmp1=closeness[tmp1]/avg_close
        degree_tmp1=de[tmp1]/avg_degree
        betw_tmp1=betw[tmp1]/average_betweenness
        increase_tmp1=math.pow(float(x_all[column_order]),time)
        increase_tmp1=increase_tmp1*betw_tmp1*degree_tmp1*close_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
       
       
    def spreadCalculate_integrated_y(self):
        G=self.G
        column_order=self.column_order
        tmp1=self.node
        y_all=self.reverseDecay
        time2=self.time
        betw=self.betw
        average_betweenness=self.average_betweenness
        de=self.de
        avg_degree=self.avg_degree
        closeness=self.closeness
        avg_close=self.avg_close
        close_tmp1=closeness[tmp1]/avg_close
        degree_tmp1=de[tmp1]/avg_degree
        betw_tmp1=betw[tmp1]/average_betweenness
        increase_tmp1=math.pow(float(y_all[column_order]),time2)
        increase_tmp1=increase_tmp1*betw_tmp1*degree_tmp1*close_tmp1
        G.node[tmp1]['spread']=G.node[tmp1]['spread']+increase_tmp1
        x_matrix=G.node[tmp1]['x_matrix']
        x_matrix[time2][column_order]+=1
        G.node[tmp1]['x_matrix']=x_matrix
        
    
    

