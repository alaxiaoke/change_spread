# -*- coding: utf-8 -*-
import numpy as np
import random


class ProbabilityModel:
    
    def __init__(self,affect_node_list,probability_models,closeness,avg_close,de,avg_degree,betw,average_betweenness):
        self.model=probability_models
        self.affect_node_list=affect_node_list
        self.closeness=closeness
        self.avg_close=avg_close
        self.de=de
        self.avg_degree=avg_degree
        self.betw=betw
        self.average_betwenness=average_betweenness
        self.choose()
        
        
    def choose(self):
        model=self.model
        if 'nwm' in model:
            ran=self.notWeighted()
            #print 'ran in tne notWeighted is',ran
            return ran 
            #print 'ran',ran
        if 'cwm' in model:
            ran=self.closenessWeighted()
            return ran 
        if 'dwm' in model:
            ran=self.degreeWeighted()
            return ran             
        if 'bwm' in model:
            ran=self.betweennessWeighted()
            return ran 
        if 'iwm' in model:
            ran=self.allWeighted()
            return ran 

            
    def notWeighted(self):
        affect_node_list=self.affect_node_list
        tmp=np.random.randint(0,len(affect_node_list))
        ran=affect_node_list[tmp]
        #print 'ran in tne notWeighted is',ran
        return ran
    
        
    def closenessWeighted(self):                 #计算了紧密度活性的算法 
        affect_node_list=self.affect_node_list
        closeness=self.closeness
        avg_close=self.avg_close                
        totals = []
        running_total = 0
        weights=[]
        for tmp1 in affect_node_list:
            closeness_tmp1=10*(closeness[tmp1]/avg_close)
            #print tmp1,closeness_tmp1
            weights.append(closeness_tmp1)
        for w in weights:
            running_total += w
            totals.append(running_total)
        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                #print affect_node_list[i]
                return affect_node_list[i]

                
                
                
    def degreeWeighted(self):
        affect_node_list=self.affect_node_list
        de=self.de
        avg_degree=self.avg_degree        
        totals = []
        running_total = 0
        weights=[]
        for tmp1 in affect_node_list:
            de_tmp1=10*(de[tmp1]/avg_degree)
            #print tmp1,closeness_tmp1
            weights.append(de_tmp1)
        for w in weights:
            running_total += w
            totals.append(running_total)
        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                #print affect_node_list[i]
                return affect_node_list[i] 

        
    def betweennessWeighted(self):
        affect_node_list=self.affect_node_list
        betw=self.betw
        average_betweenness=self.average_betwenness
        totals = []
        running_total = 0
        weights=[]
        for tmp1 in affect_node_list:
            betw_tmp1=100*(betw[tmp1]/average_betweenness)
            #print tmp1,closeness_tmp1
            weights.append(betw_tmp1)
        for w in weights:
            running_total += w
            totals.append(running_total)
        rnd = random.random() * running_total
        #print running_total
        #print totals
        for i, total in enumerate(totals):
            if rnd < total:
                print affect_node_list[i]
                return affect_node_list[i]
            
    
    def allWeighted(self):
        affect_node_list=self.affect_node_list
        betw=self.betw
        average_betweenness=self.average_betwenness
        de=self.de
        avg_degree=self.avg_degree 
        closeness=self.closeness
        avg_close=self.avg_close 
        totals = []
        running_total = 0
        weights=[]
        for tmp1 in affect_node_list:
            all_tmp1=10*(betw[tmp1]/average_betweenness)*(de[tmp1]/avg_degree)*(closeness[tmp1]/avg_close)
            #print tmp1,closeness_tmp1
            weights.append(all_tmp1)
        for w in weights:
            running_total += w
            totals.append(running_total)
        rnd = random.random() * running_total
        for i, total in enumerate(totals):
            if rnd < total:
                print affect_node_list[i]
                return affect_node_list[i]    
