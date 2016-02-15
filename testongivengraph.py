#!/usr/bin/env python
#This python script was written by Georgios Serafeim
import assignwavelengths as assignwl 
import networkx as nx
"""
Create an empty graph
"""
myGraph=nx.Graph() 

"""
Add 11 nodes to the graph
"""
myGraph.add_nodes_from(range(1,12))

"""
add edges with weights to the graph 1st & 2nd numbers of each tuple represent 
the nodes, 3rd number of the tuple represents the weight. Weights will be later 
used as input to the shortes path algorithm
"""
edges=[(1,2,2),(2,3,1),(2,9,2),(2,4,3),(4,6,2),(4,8,4),(4,10,1),\
        (4,5,3),(3,10,2),(3,5,4),(3,7,2),(5,8,2),(5,11,1)]

for i in edges:
    myGraph.add_edge(i[0],i[1], weight=i[2])

assignwl.printGraph(myGraph)
"""
define some routes
1st number of the tuple represents the source
2nd number represents the destination
"""
routes=[(9,11),(11,6),(6,7),(9,7),(1,6),(7,1),(11,8)]

"""
Assign a number to each of the routes above. The role of the number is just 
to distinguish between the different routes (it is also used throughout the 
construction of the auxiliary graph)
"""
routes={i+1: routes[i] for i in range(0,len(routes))}

"""
Run the shortest path algorithm given the above routes (weights are considered)
(The method shortest_path which implements the shortest path algorithm and is 
included in the NetworkX package will be used)
"""
followed_path={}
for key, value in routes.iteritems():
    z=nx.shortest_path(myGraph,source=value[0],target=value[1], weight="weight")
    followed_path.update({key:tuple(z)})

print followed_path
"""
Construct the auxiliary graph
"""
myAuxiliaryGraph=assignwl.constructAuxGraph(followed_path)
assignwl.printGraph(myAuxiliaryGraph)

"""
Estimate the colors that would be needed to color the graph in degree order
"""

assignwl.estimateColorsDegreeOrder(myAuxiliaryGraph)

"""
Perform coloring of the graph (auxiliary graph) in degree order 
"""

assignwl.printGraph(myAuxiliaryGraph,assignwl.coloringGraph(myAuxiliaryGraph,"degree_order")[1])
"""
Estimate the number of the colors needed in case the graph is colored 
in alternate order
"""

assignwl.estimateColorsAlternateOrder(myAuxiliaryGraph)

"""
Perform coloring in alternate order
"""
assignwl.printGraph(myAuxiliaryGraph,assignwl.coloringGraph(myAuxiliaryGraph,"alternate_order")[1])

"""
Color the predefined routes of the initial graph based on the results 
of the coloring algorithm in degree order
"""
assignwl.drawColoredPathsOnGivenGraph(myGraph, myAuxiliaryGraph, followed_path, "degree_order")


"""
Color the predefined routes of the initial graph based on the results 
of the coloring algorithm in alternate order
"""
assignwl.drawColoredPathsOnGivenGraph(myGraph, myAuxiliaryGraph, followed_path, "alternate_order")

