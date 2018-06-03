#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:51:45 2018

@author: sdrgroup
"""
import json
import networkx as nx
from matplotlib import colors
import matplotlib.pyplot as plt      


class Output:
    def __init__(self,G,change_list_original):
        self.G=G
        self.change_list_original=change_list_original
        
    def json_data(self):
        G=self.G
        change_node_list_original=self.change_list_original
        affected=[]
        for i in G.nodes():
            if G.node[i]['spread']!=0:
                affected.append(i)
        for i in affected:
            node_data={}
            node_data['node_ID']=i
            node_data['belongTo']=G.node[i]['belongTo']
            node_data['spread of this node']=G.node[i]['spread']
            json_data_1=json.dumps(node_data,sort_keys=True,indent=4,separators=(',', ':'),encoding="utf-8")
            print json_data_1
            node_data_2={}
            tt=0
            try_list=[]
            ok=[]
            for p in change_node_list_original:
                try_list=G.node[i]['x_matrix'][:,tt]
                for a in range(len(try_list)):
                    ok.append(try_list[a])
                node_data_2[p]=ok
                tt+=1
                ok=[]
                try_list=[]
            json_data_2=json.dumps(node_data_2,sort_keys=True,indent=4,separators=(',', ':'),encoding="utf-8")
            print json_data_2
            node_data_3={}
            tt=0
            try_list=[]
            ok=[]
            for p in change_node_list_original:
                try_list=G.node[i]['y_matrix'][:,tt]
                for a in range(len(try_list)):
                    ok.append(try_list[a])
                node_data_3[p]=ok
                tt+=1
                ok=[]
                try_list=[]
            json_data_3=json.dumps(node_data_3,sort_keys=True,indent=4,separators=(',', ':'),encoding="utf-8")
            print json_data_3
    
    def visualize(self):        
        G=self.G
        node_spread={}
        for i in nx.nodes(G):
            node_spread[i]=G.node[i]['spread']
        x=nx.get_node_attributes(G,"x")         #获取x坐标，得到以点的代号为key，x坐标为value的字典
        y=nx.get_node_attributes(G,"y")         
        pos={}                                    # 创建pos用于存放以点的代号为key，以（x,y）二维坐标为value的字典
        node_size={}
        x_y=[]                                    #x_y用于存放(x,y)  
        x_list=[]                       #x_list 存放所有x
        y_list=[]                        #y_list 存放所有y
        for i in x:
            x_list.append(float(x[i]))              #由于x是unicode编码，转化为float 
        for i in y:
            y_list.append(float(y[i]))              
            
        for i in range(0,len(x_list)):
            tup=(x_list[i],y_list[i])     #tup元祖用于存放单个（x,y）     
            x_y.append(tup)
        #print x_y    
        node=nx.nodes(G)                        
        w=0
        tmp=0
        total=0
        for n in node:
            if G.node[n]['spread']!=0:
                tmp+=1
                total=total+G.node[n]['spread']       
        ave=float(total)/tmp
        for n in node:
            G.node[n]['spread']=float(G.node[n]['spread'])/ave            
        for n in node:
            pos[n]=x_y[w]                       #挨个把坐标（x,y）给点
            w+=1
            node_size[n]=G.node[n]['spread']*75
            node_size[n]=node_size[n]+float(30)       
        colors_list=['#D3D3D3','#FA8072','#FF0000']           #列表中是红色和白色的颜色代码,红在后.
        cmap=colors.LinearSegmentedColormap.from_list('test',colors_list,N=10)
        nx.draw_networkx(G, pos=pos,
                         node_list=node_spread.keys(), 
                         node_color=node_size.values(),
                         node_size=node_size.values(),
                         width=0.1,
                         cmap=cmap,
                         with_labels=False)       
        x_min=min(x_list)               #获取x,y的最大值和最小值，用于确定坐标图的范围
        x_max=max(x_list)
        y_min=min(y_list)
        y_max=max(y_list)
        #print x_min
       # print x_max
       # print y_min
       # print y_max    
        plt.xlim(x_min-10.0,x_max+10.0)             #设置界面X轴坐标范围  
        plt.ylim(y_min-10.0,y_max+10.0)             #设置界面Y轴坐标范围 
        plt.show()