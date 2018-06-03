#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:44:46 2018

@author: aj
"""
import networkx as nx
import math
import numpy as np
from spreadModel import SpreadModel
from probabilityModel import ProbabilityModel
import copy
from output import Output


class SpreadSimulator:
        def __init__(self,graphml,minThreshold,forwardDecay,reverseDecay,modifiedNodes,addedNodes,removedNodes,startingNodes,modifiedEdges,spreadModels,probabilityModels):
            self.__G=nx.read_graphml(graphml)
            self.__minThreshold=minThreshold
            self.__forwardDecay=forwardDecay
            self.__reverseDecay=reverseDecay
            self.__modifiedNodes=modifiedNodes
            self.__addedNodes=addedNodes
            self.__removedNodes=removedNodes
            self.__startingNodes=startingNodes
            self.__modifiedEdges=modifiedEdges
            self.__spreadModels=spreadModels
            self.__probabilityModels=probabilityModels
            G=self.__G
            self.__closeness=nx.closeness_vitality(G)                                  #紧密度活性:去掉该节点后全图的变化情况
            value=self.__closeness.values()
            tmp_close=0
            for k in value:
                tmp_close=tmp_close+float(k)
            self.__avg_close=tmp_close/float(len(G.nodes()))         
            degree_all=0
            self.__betw=nx.betweenness_centrality(G,k=None, normalized=True, weight=None)
            total=0
            for i in G.nodes():
                total=total+self.__betw[i]
            self.__average_betweenness=float(total)/len(G.nodes()) 
            self.__de=G.degree()
            for n in G.nodes():
                degree_all=degree_all+self.__de[n]
            self.__avg_degree=float(degree_all)/len(G.nodes())   
            for k in value:
                tmp_close=tmp_close+float(k)
            self.__avg_close=tmp_close/float(len(G.nodes()))
        
        def spreadPreperation(self):
            G=self.__G
            for i in G.node:
                G.node[i]['spread']=float(0)    #添加新属性
                #每一次spread值的变动都必须伴随time的变动
            change_list_original=[]
            min_spread=float(self.__minThreshold)      #低于min_spread的影响值spread被忽略为=0
            modified_num=len(self.__modifiedNodes)
            added_num=len(self.__addedNodes)
            removed_num=len(self.__removedNodes)
            starting_num=len(self.__startingNodes)
            edge_num=len(self.__modifiedEdges)
            x_all=self.__forwardDecay             #各节点不同衰减率的列表             
            y_all=self.__reverseDecay
            tmp3=0
            tmp4=0
            x=float(max(x_all))
            y=float(max(y_all))
            #print x,y
            for i in range(1000):               #通过输入的衰减率,变更节点数量和最小阈值来确定矩阵的行
                if math.pow(x,i)>=min_spread:
                    tmp3+=1
                else:
                    x_row=tmp3         #正向衰减的行数为i
            self.x_row=x_row
            #print 'x_row',x_row
            for i in range(1000):               #通过输入的衰减率,变更节点数量和最小阈值来确定矩阵的行
                if math.pow(y,i)>=min_spread:
                    tmp4+=1
                else:
                    y_row=tmp4    
            self.y_row=y_row
            change_nodes=[]
            #print 'y_row=',y_row
            column=modified_num+added_num+removed_num+starting_num+edge_num*2      #输入的变更节点数量来确定矩阵的列数
            for i in G.node:
                G.node[i]['x_matrix']=np.zeros((x_row,column),dtype=np.int)
                G.node[i]['y_matrix']=np.zeros((y_row,column),dtype=np.int)
            tmp=int(0)
            if modified_num!=0 or added_num!=0 or removed_num!=0 or starting_num!=0:    
                change_nodes=self.__addedNodes+self.__modifiedNodes+self.__removedNodes
                #change_nodes=change_nodes.replace('\'', '')    #去掉引号           
                change_list_original=change_nodes
            tmp=0
            if edge_num!=0:
                while (edge_num>0):
                    change_nodes=self.__modifiedEdges
                    #change_nodes=change_nodes.replace(' ', '')     #去掉空格
                    #change_nodes=change_nodes.replace('\'', '')    #去掉引号
                    #change_nodes=change_nodes.split(',')              #按逗号
                    if tmp<edge_num:   
                        change_list_original.append(change_nodes[tmp])               #这是与点修改不同的地方
                        change_list_original.append(change_nodes[tmp+1])
                        #print change_node_list_original
                        tmp=tmp+2
                    edge_num=edge_num-1        
            self.__original_list=change_list_original
            
            #print change_node_list        
            #print change_node_list          #此列表里是修改的节点
            print self.__original_list
            if self.__original_list:
                self.modifiedSpreadSimulate()
            if self.__startingNodes:
                self.startingSpreadSimulate()
            output=Output(G,self.__original_list)
            output.json_data() 
            output.visualize()
        def modifiedSpreadSimulate(self):           #对于变更的节点或者边进行仿真
            G=self.__G
            change_node_list=[]
            affect_node_list=[]
            column_order=0
            x_row=self.x_row
            y_row=self.y_row
            for i in self.__original_list:
                G.node[i]['spread']=1       
                predecessor_i=G.predecessors(i)
                affect_node_list=predecessor_i
                affect_node_list_2=copy.deepcopy(affect_node_list)
            stop_num=0
            for i in self.__original_list:
                G.node[i]['spread']=1       
                successor_i=G.successors(i)
                orientation='1'   #1表示正向，２表示逆向
                affect_node_list=successor_i
                affect_node_list_2=copy.deepcopy(affect_node_list)
                time=0
                for i in range(50):     
                    #print(i,time)                                   
                    print 'affect_node_list',affect_node_list
                    if stop_num<len(affect_node_list):        
                        for p in affect_node_list: 
                            pm=ProbabilityModel(affect_node_list,self.__probabilityModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                            tmp1=pm.choose()
                            print 'tmp1 is',tmp1
                            if tmp1:
                                sm=SpreadModel(G,tmp1,orientation,self.__minThreshold,time,column_order,self.__forwardDecay,self.__reverseDecay,self.__spreadModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                                sm.choose()
                                change_node_list.append(tmp1)           
                    time+=1
                    affect_node_list=[]
                    for i in change_node_list:
                        successor_i=G.successors(i)
                        affect_node_list=affect_node_list+successor_i
                        l2=list(set(affect_node_list))
                        l2.sort(key=affect_node_list.index)
                        affect_node_list=l2
                    if time==x_row:
                        time=0
                        affect_node_list=affect_node_list_2
                    change_node_list=[]
                column_order+=1
            change_node_list=[]
            affect_node_list=[]
            column_order=0          #列序号
            for i in self.__original_list:
                G.node[i]['spread']=1       
                predecessor_i=G.predecessors(i)
                affect_node_list=predecessor_i
                affect_node_list_2=copy.deepcopy(affect_node_list)
                time=0
                for i in range(50):     
                    #print(i,time)                                   
                    print 'affect_node_list',affect_node_list
                    if stop_num<len(affect_node_list):        
                        for p in affect_node_list:   
                            pm=ProbabilityModel(affect_node_list,self.__probabilityModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                            tmp1=pm.choose()
                            print 'tmp1 is',tmp1
                            if tmp1:
                                sm=SpreadModel(G,tmp1,orientation,self.__minThreshold,time,column_order,self.__forwardDecay,self.__reverseDecay,self.__spreadModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                                sm.choose()
                                change_node_list.append(tmp1)           
                    time+=1
                    affect_node_list=[]
                    for i in change_node_list:
                        predecessor_i=G.predecessors(i)
                        affect_node_list=affect_node_list+predecessor_i
                        l2=list(set(affect_node_list))
                        l2.sort(key=affect_node_list.index)
                        affect_node_list=l2
                    stop_num=0
                    if time==y_row:
                        time=0
                        affect_node_list=affect_node_list_2
                    change_node_list=[]
                column_order+=1      
                

        def startingSpreadSimulate(self):       #对入口点的情况进行仿真
            G=self.__G
            change_node_list=[]
            affect_node_list=[]
            column_order=0
            x_row=self.x_row
            for i in self.__original:
                G.node[i]['spread']=1       
                predecessor_i=G.predecessors(i)
                affect_node_list=predecessor_i
                affect_node_list_2=copy.deepcopy(affect_node_list)
            stop_num=0
            for i in self.__startingNodes:
                G.node[i]['spread']=1       
                successor_i=G.successors(i)
                orientation='1'   #1表示正向，２表示逆向
                affect_node_list=successor_i
                affect_node_list_2=copy.deepcopy(affect_node_list)
                time=0
                for i in range(50):     
                    #print(i,time)                                   
                    #print affect_node_list
                    if stop_num<len(affect_node_list):        
                        for p in affect_node_list: 
                            pm=ProbabilityModel(G,affect_node_list,self.__probabilityModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                            tmp1=pm.choose()
                            if tmp1:
                                sm=SpreadModel(G,tmp1,orientation,self.__minThreshold,time,column_order,self.__forwardDecay,self.__reverseDecay,self.__spreadModels,self.__closeness,self.__avg_close,self.__de,self.__avg_degree,self.__betw,self.__average_betweenness)
                                sm.choose()
                                change_node_list.append(tmp1)           
                    time+=1
                    affect_node_list=[]
                    for i in change_node_list:
                        successor_i=G.successors(i)
                        affect_node_list=affect_node_list+successor_i
                        l2=list(set(affect_node_list))
                        l2.sort(key=affect_node_list.index)
                        affect_node_list=l2
                    if time==x_row:
                        time=0
                        affect_node_list=affect_node_list_2
                    change_node_list=[]
                column_order+=1
                
        
            
           
