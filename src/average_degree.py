#! /usr/bin/env python
"""
 Program Name : average_degree.py
 Date         : 04/02/2016
 Desc         : This program reads tweeter input flat file, parses for timestamp and hastags.
                From the hashtags, it creates a graph of hashtags and calculates average degree 
                of vertex. It maintains a sliding window of 60 seconds for the data.
                It users a dict of dict to store edge information in the 
                node(key1)-->(edge(key2)-->timestamp(value) format.
                
 notes        : per row calc as slow, add batching for large datasets and data structures with
                indexed access to values(timestamp) field for pruning.
                
"""

import json
import datetime 
import itertools
from collections import defaultdict
from collections import Counter
import sys


class Graph(object):
    """
    Manage graph data structure using nested dicts.
   
    Attributes:
        _graph : nested dict for node->edge data. timestamp is stored as value in inner dict.
        
    Methods   : 
       
       add_edge    : for new hashtag set, add 2 entries (node1 --> node2) and (node2-->node1).
       count_nodes : count of number of nodes in the graph
       list_nodes  : list of node names in the graph
       count_edges : list of tuples. tuples are in the (1,n) form where n is count of edges.
       get_avgVertex : returns the degree of vertex in the graph in decimal format rounded to 2 places.
       list_edges  : list of edges for a given node
       prune_nodes : removes edges that fall out of the 60 second window. removes nodes without edges.
       get_defdict : returns the nested dict that has the complete data.
       
       
    """
    def __init__(self):
        """ initializes a dict of dict for data structure node --> Vertex --> timestamp """
        self._graph = defaultdict(dict)
        
    def add_edge(self,edgeDetail):
        """ for every pair of hashtags add a node1 --> node2 and node2 ---> node1 entry to correct timestamp  """
        """ if the node or edge exists the timestamp will be updated """
        self._graph[edgeDetail[1][0]][edgeDetail[1][1]] = edgeDetail[0]
        self._graph[edgeDetail[1][1]][edgeDetail[1][0]] = edgeDetail[0]
        
    def count_nodes(self):
        """ return the count of nodes in the graph. that is same as the outer dicts length. """
        return len(self._graph)
        
    def list_nodes(self):
        """ return a list of node names in the graph """
        return [  node for node,edge in  self._graph.iteritems()]
        
    def count_edges(self):
        """ return a list of tuples in [(1 , N )]format, where N is count of edges per node """
        edgeCount = [(1,len(edge),node) for node,edge in self._graph.iteritems()  ]
        return edgeCount
        
    def get_avgVertex(self):
        """  return the average degree of vertex as nodecount / sum of edgecount per node."""
        edgeCount = [(1,len(edge)) for node,edge in self._graph.iteritems()  ]
        noOfNodes = sum([pair[0] for pair in edgeCount])
        noOfEdges = sum([pair[1] for pair in edgeCount])
        return str(round(round(noOfEdges,2)/noOfNodes,2))
        
    def list_edges(self,nodeName):
        """ return a list of edges for a given node. """
        nodeEdges = [edge  for node,edge in self._graph.iteritems() if nodeName in node ]
        return nodeEdges
        
    def get_defdict(self):
        """ return the nested dict that contains the graph data"""
        return self._graph
        
    def prune_nodes(self,cutoff_at):
        """ scan the dict look for timestamps that are greater than the cutoff_at value.
        the cutoff value is 60 seconds before the last timestamp that you processed """
        for k1 in self._graph.keys():
                """ for each node """
	        for k2,t2 in self._graph[k1].items():
	               """ for each edge """
	               if (t2 < cutoff_at ):
	                   """ remove the edge if it's timestamp is before the cutoff """
		           del(self._graph[k1][k2])
                       if not self._graph[k1]:	
                           """ if you removed all edges, get rid of that node """
                           del(self._graph[k1])	  
    def __str__(self):
        """ return the string format of the dict for printing """
        return '({})'.format(dict(self._graph))

"""  end of class Graph  """

def main(argv):
#    if len(argv) < 2:
#        print >> sys.stderr, argv[0], "please provide a input and output file"   
                  
    tweetFile = sys.argv[1] # file containing the raw tweets in json format   #

    outFileName   = sys.argv[2] # file that records the avgerage degree per record that is read #
    windowSize = 60 # sliding window size of data to keep from the max timestamp #
    g = Graph() # initialize the graph object to store the nodes/edges information that will now be read#
    hashTagList = [] # list to capture the hash tag data from the input tweet #
    outFileW = open(outFileName, 'w') 
    created_at = datetime.datetime.min ## initializing created_dt that holds the timestamp on current record
    maxtime_at = created_at ## initializing maxtime_at that hold the max timestamp ever processed
    
    """ open the outputfile to record the average degree result """

    with open(tweetFile) as f:
        for line in f: 
            """ for every record in the inputfile """
            try:
               """ parse to see if the in record is valid json. ignore the record if not"""
               jline = json.loads(line)
            except:
                pass   
            
            try:
                """ if the record has atleast a pair of hash tags. ignore the ones that don't """
                created_at = datetime.datetime.strptime(jline['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                maxtime_at = max(maxtime_at, created_at)

                """ format the created_at timestamp to py format """
                cutoff_at = maxtime_at - datetime.timedelta(seconds=windowSize)
                """ calc the sliding window limit """
                hashTagList  = [ hashtag['text'] for hashtag in jline['entities']['hashtags']]
                if  ((len(hashTagList) > 1) & ( created_at > cutoff_at)):
                    """ ignore hastags that do not have atleast 2 values"""
                    for pair in itertools.combinations(hashTagList,2):
                        """ create pairs from the list of hash tags. if you receive apache,storm, kafka this will provide
                        apache, storm  storm,kafka and apache,kafka pairs. """
                        edgeDetail = [created_at,list(pair)]
                        g.add_edge(edgeDetail)
                        """ only if you received a pair, add new edges to the graph  """
                
                g.prune_nodes(cutoff_at)
                """ removed old edges and childless nodes regardless """
                outFileW.write( g.get_avgVertex()+'\n')
                """ outFileW.write( str(g.list_nodes()) ) ## test code##
                 outFileW.write( str(g.list_edges('Cassandra')) ) ## test code##
                outFileW.write( str(datetime.datetime.strftime(cutoff_at,'%a %b %d %H:%M:%S +0000 %Y')) ) ## test code##
                outFileW.write( str(datetime.datetime.strftime(created_at,'%a %b %d %H:%M:%S +0000 %Y')) ) ## test code##
                """
                """ write the average degree result to the outputfile"""
            except:
                 pass
        outFileW.close()       
""" close the output file """
if __name__ == "__main__":
     sys.exit(main(sys.argv))
