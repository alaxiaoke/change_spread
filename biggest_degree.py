# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 15:51:22 2018

@author: zou
"""

import networkx as nx
import math
import igraph


def biggestDegree(G,vals):   #计算度
    degree=nx.degree(G)
    #print ("Degree:" ,degree)
    nodes=nx.nodes(G)
    s=1
    for i in nodes:
        if len(G.neighbors(i))>s:
            s=len(G.neighbors(i))
            print i,s
        #print i,len(G.neighbors(i))
    print G.predecessors('1015c87980fccc2b2aef26d201280cc0')
    print G.successors('1015c87980fccc2b2aef26d201280cc0')
    return i   
G=nx.read_graphml("NineGridImageView-master.graphml")
biggestDegree(G,G) 
#python changeSpread.py -g Filters.graphml -m 0.1 -f 0.5,0.5 -r 0.5,0.5 -a a344cdfaa840f217285b9fcb64b2b7dd,3d890843264cf3c88a4c0b909f5cdb94 -s ncrd -p cwm
