#!/usr/bin/env python
#This python script was written by Georgios Serafeim
import assignwavelengths as assignwl 

"""
Create an empty graph with 11 nodes
"""
fiber_network=assignwl.createGraph(11)

"""
Add edges with weights to the graph 1st & 2nd numbers of each tuple represent 
the nodes, 3rd number of the tuple represents the weight. Weights will be later 
used as input to the shortes path algorithm
"""
edges=[(1,2,2),(2,3,1),(2,9,2),(2,4,3),(4,6,2),(4,8,4),(4,10,1),\
        (4,5,3),(3,10,2),(3,5,4),(3,7,2),(5,8,2),(5,11,1)]

assignwl.addEdges(fiber_network,edges)

"""
Print the graph
"""
assignwl.printGraph(fiber_network, "blue", "Given fiber network")

"""
Define some lightpaths. The key of the dictionary represents the number of the lightpath
The role of this number is just to distinguish between the different lightpaths 
(it is also used throughout the construction of the auxiliary graph)
1st number of each tuple represents the source node
2nd number represents the destination node
"""
lightpaths={1: (9, 11), 2: (11, 6), 3: (6, 7), 4: (9, 7), 5: (1, 6), 6: (7, 1), 7: (11, 8)}

"""
Construct the auxiliary graph. In order to construct the auxiliary graph, 
the route of each of the lightpaths defined above is found using the shortest 
path algorithm which then is used as input to the function that makes the auxiliary 
graph
"""
myAuxiliaryGraph=assignwl.constructAuxGraph(assignwl.shortestPath(fiber_network, lightpaths))
assignwl.printGraph(myAuxiliaryGraph,"blue", "Auxiliary Graph")

"""
Estimate the colors that would be needed to color the graph in degree order
"""
assignwl.estimateColorsDegreeOrder(myAuxiliaryGraph)

"""
Perform coloring of the graph (auxiliary graph) in degree order 
"""
assignwl.printGraph(myAuxiliaryGraph,assignwl.coloringGraph(myAuxiliaryGraph,"degree_order")\
	, "Coloring in degree order")

"""
Estimate the number of the colors needed in case the graph is colored 
in alternate order
"""
assignwl.estimateColorsAlternateOrder(myAuxiliaryGraph)

"""
Perform coloring in alternate order
"""
assignwl.printGraph(myAuxiliaryGraph,assignwl.coloringGraph(myAuxiliaryGraph,"alternate_order"),\
 "Coloring in alternate order")

"""
Color the predefined routes of the initial graph based on the results 
of the coloring algorithm in degree order
"""
assignwl.drawColoredPathsOnGivenGraph(fiber_network, myAuxiliaryGraph, assignwl.shortestPath(fiber_network,\
 lightpaths), "degree_order")

"""
Color the predefined routes of the initial graph based on the results 
of the coloring algorithm in alternate order
"""
assignwl.drawColoredPathsOnGivenGraph(fiber_network, myAuxiliaryGraph, assignwl.shortestPath(fiber_network,\
 lightpaths), "alternate_order")