#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 15:49:39 2018

@author: aj
"""
import sys
import getopt
from spreadSimulator import SpreadSimulator


spreadModelSet={'srd':'simplest_ripple_degree','ncrd':'node_closeness_ripple_degree','ndrd':'node_degree_ripple_degree','nbrd':'node_betweenness_ripple_degree','ird':'integrated_ripple_degree'}
probabilityModelSet={'nwm':'not_weighted_model','cwm':'clossness_weighted_model','dwm':'degree_weighted_model','bwm':'betweenness_weighted_model','iwm':'integrated_weighted_model'}
def main(argv):
    graphml=''
    minThreshold=0.0
    forwardDecay=[]
    reverseDecay=[]
    addedNodes=[]        
    removedNodes=[]
    modifiedNodes=[]
    modifiedEdges=[]
    startingNodes=[]
    spreadModels=[]
    probabilityModels=[]
    
    try:
        options,args=getopt.getopt(sys.argv[1:],'hg:m:f:r:a:b:c:d:e:s:p:')
    except getopt.GetoptError:
        sys.exit()
    for name,value in options:
        if name=='-h':
            print ('usage:[-h] -g <arg> -m <arg> -f <arg> -r <arg> -a <arg> -b <arg> -c <arg> -d <arg> -e <arg> -s <arg> -p <arg>')
            print ('-h,\t--help')
            print ('-g,\t--address of the graphml')
            print ('-m,\t--the minThreshold')
            print ('-f,\t--the forward decay')
            print ('-r,\t--the reverse decay')
            print ('-a,\t--ID of the modified nodes')
            print ('-b,\t--ID of the added nodes')
            print ('-c,\t--ID of the removed nodes')
            print ('-d,\t--ID of the starting nodes')
            print ('-e,\t--ID of the modified edges')
            print ('-s,\t--choose the spread models')
            print ('-p,\t--choose the probability models')
            print ('please input the corresponding shorter form after -s\nsrd\tsimplest_ripple_degree\nncrd\tnode_closeness_ripple_degree\nndrd\tnode_degree_ripple_degree\nnbrd\tnode_betweenness_ripple_degree\nird\tintegrated_ripple_degree\nsnr\tstarting_node_relevance\nanr\tarbitrary_node_relevance')
            print ('please input the corresponding shorter form after -p\nnwm\tnot_weighted_model\ncwm\tclossness_weighted_model\ndwm\tdegree_weighted_model\nbwm\tbetweenness_weighted_model\niwm\tintegrated_weighted_model')
        #name=name.trim()
        #value=value.trim()
        if name=='-g':
           graphml=value
        if name=='-m':           
            minThreshold=value
        if name=='-f':          
            forwardDecay=value.split(',')
        if name=='-r':
            reverseDecay=value.split(',')
        if name=='-a':
            modifiedNodes=value.split(',')
        if name=='-b':
            addedNodes=value.split(',')
        if name=='-c':
            removedNodes=value.split(',')
        if name=='-d':
            startingNodes=value.split(',')
        if name=='-e':
            modifiedEdges=value.split(',') 
        if name=='-s':
            spreadModels=value.split(',') 
            for key in spreadModels:
                if not key in spreadModelSet:
                    spreadModels.pop(key)
        if name=='-p':
            probabilityModels=value.split(',') 
            for key in probabilityModels:
                if not key in probabilityModelSet:
                    probabilityModels.pop(key)
    #print 'graphml is ',graphml
    if graphml and forwardDecay and minThreshold and reverseDecay and spreadModels and probabilityModels:
        if addedNodes or removedNodes or modifiedNodes or modifiedEdges or startingNodes:
            simulator=SpreadSimulator(graphml,minThreshold,forwardDecay,reverseDecay,modifiedNodes,addedNodes,removedNodes,startingNodes,modifiedEdges,spreadModels,probabilityModels)
            simulator.spreadPreperation()
        else:
            print 'There are some parameters missing'
    else:
        print 'There are some parameters missing'
            
if __name__ == '__main__':
    print ('usage:[-h] -p <arg> -m <arg> -f <arg> -r <arg> -n <arg> -e <arg> -x <arg> -y <arg> -t <arg> -r <arg>')
    print ('-h,\t--help')
    print ('-g,\t--address of the graphml')
    print ('-m,\t--the minThreshold')
    print ('-f,\t--the forward decay')
    print ('-r,\t--the reverse decay')
    print ('-a,\t--ID of the modified nodes')
    print ('-b,\t--ID of the added nodes')
    print ('-c,\t--ID of the removed nodes')
    print ('-d,\t--ID of the starting nodes')
    print ('-e,\t--ID of the modified edges')
    print ('-s,\t--choose the spread models')
    print ('-p,\t--choose the probability models')
    print ('please input the corresponding shorter form after -s\nsrd\tsimplest_ripple_degree\nncrd\tnode_closeness_ripple_degree\nndrd\tnode_degree_ripple_degree\nnbrd\tnode_betweenness_ripple_degree\nird\tintegrated_ripple_degree\nsnr\tstarting_node_relevance\nanr\tarbitrary_node_relevance')
    print ('please input the corresponding shorter form after -p\nnwm\tnot_weighted_model\ncwm\tclossness_weighted_model\ndwm\tdegree_weighted_model\nbwm\tbetweenness_weighted_model\niwm\tintegrated_weighted_model')
    main(sys.argv)
