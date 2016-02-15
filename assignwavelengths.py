#!/usr/bin/env python
#This python script was written by Georgios Serafeim
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pathdrawer as pathdr
import copy

def printGraph(graph,nodeColor=["blue"]):
    #positions for all nodes
    pos=nx.spring_layout(graph)

    #draw the nodes of the graph
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color=nodeColor)

    #draw the edges of the graph
    nx.draw_networkx_edges(graph, pos, width=4, edge_color="black")

    #print labels
    nx.draw_networkx_labels(graph, pos, font_size=14, font_family="sans-serif")

    #print the labels related to the edges
    labels=nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)

    plt.axis("off") #do not plot any axis
    plt.show() #display

def haveCommonEdge(route_1,route_2):
    """
    This function receives two routes (python lists) and returns True in 
    case they share a common edge
    """
    def returnOneEdgeAtaTime(route):
        """
        This function returns on the fly the successive edges of a route 
        """
        for i in range(0,len(route)-1):
            yield route[i],route[i+1] 
        
    for i in returnOneEdgeAtaTime(route_1):
        for j in returnOneEdgeAtaTime(route_2):
            if i==j or i==j[::-1]: #with j[::-1] the reverse of the j tuple is given back
                return True
                break #The function stops running once it finds a common edge

def constructAuxGraph(path):
    """
    This function constructs the auxiliary graph given a python dictionary as argument wich 
    consists of the # of the path as the key of the dictionary and the path (source, intermediate 
    nodes, destination) that a predifined route has to traverse in order to go from the source 
    node to the destination node. The dictionary should look something like this: 
    {#ofpath:(source_node, interm_node, ...,iterm_node,destination_node),...}
    
    The document that comes with this python script explains what is the auxiliary graph and 
    how it is constructed. Please refer to that document for more details.
    """
    auxGraph=nx.Graph() #create an empty graph object which will be used as the auxiliary graph
    for key in path.iterkeys(): #create a node in the auxGraph for each of the predefined routes
        auxGraph.add_node(key)

    examined_keys=[]
    for key, value in path.iteritems():
        examined_keys.append(key) #this list is used to keep track of the routes that have been examined
        for key2,value2 in path.iteritems():
            if key2 not in examined_keys: #do not examine a route that you examined before
                if haveCommonEdge(list(value),list(value2)) == True:
                    auxGraph.add_edge(key,key2) #connect the routes that share a common edge

    return auxGraph

def estimateColorsDegreeOrder(graph):
    """
    Given a graph, this function is able to estimate the number of colors in degree order
    that will be probably needed to color it. (First of all we have to find the degree of 
    each node of the auxiliary graph and then sort them in descending order. The estimation 
    is given by the point where the identity function and the node degree are intersected 
    increased by one unit)
    """
    points_x=points_degreeOfNodes=[]
    degreeOfNodes=sorted(DegreeOfNodes(graph), reverse=True)
    x=range(1,len(degreeOfNodes)+1) 
    points_x=[(i,i) for i in x] #The points of the identity function
    points_degreeOfNodes=[(x[i],degreeOfNodes[i]) for i in range(0,len(degreeOfNodes))]
    intersect_point=[i for i in points_x if i in points_degreeOfNodes]
    estimated_colors=intersect_point[0][0]+1
    
    """Plot the results"""
    plt.title("Estimation of needed colors in degree order: %d (point of intersection +1)" %estimated_colors)
    p1, = plt.plot(x,x, label="Identity Function", linestyle='None', color='r',marker='o')
    p2, = plt.plot(x, degreeOfNodes, linestyle='None', marker='.', label="Degree of nodes")
    l1 = plt.legend([p1], ["Identity Function"], loc=2)
    l2 = plt.legend([p2], ["Degree of nodes"], loc=4) 
    plt.gca().add_artist(l1)  
    plt.show()
    
def DegreeOfNodes(graph):
    """
    This function receives a graph as argument and returns a list. Each value of the list 
    represents the degree of the node that corresponds to the index of the value 
    """
    
    degreeOfNodes=[]
    [degreeOfNodes.append(graph.degree(node)) for node in graph.nodes()]

    return degreeOfNodes
    
def nodesDescendingOrder(graph):
    """
    This function receives a graph and returns the nodes of the graph in descending order  
    based on their degrees
    """
    
    degreeOfNodes=DegreeOfNodes(graph)
    nodes_descending=[]
    for i in range(0, nx.number_of_nodes(graph)):
        max_index=degreeOfNodes.index(max(degreeOfNodes))
        nodes_descending.append(max_index+1)
        degreeOfNodes[max_index]=0
    
    return nodes_descending

def alternateOrder(graph):
    """
    This function receives a graph and returns a list with the alternate order of its nodes.
    It also returns a list with the corresponding degrees of the nodes.
    """
    tempGraph=graph.copy()
    alt_order, degrees_alt_order = [], []
    for i in range(0, nx.number_of_nodes(graph)-1): 
        minval=min([x for x in DegreeOfNodes(tempGraph) if x !=0]) 
        u=DegreeOfNodes(tempGraph).index(minval)+1
        degrees_alt_order.append(minval)
        alt_order.append(u)
        [tempGraph.remove_edge(u,neighbor) for neighbor in tempGraph.neighbors(u)]
    alt_order.append(list(set(tempGraph.nodes())-set(alt_order))[0])
    degrees_alt_order.append(0) #The last remaining node will always have a 0 degree
    
    return (alt_order, degrees_alt_order)

def estimateColorsAlternateOrder(graph):
    """
    This function estimates the number of colors that will be needed to color a graph in 
    alternate order
    """
    my_degrees_alt_order = alternateOrder(graph)[1]
    my_degrees_alt_order_est=[i+1 for i in my_degrees_alt_order]
    print("In order to color the graph in alternate order, it is estimated that\
 %d colors will be needed."%(max(my_degrees_alt_order_est)))

def coloringGraph(graph, coloring_order="degree_order"):
    """
    This function performs the coloring of a graph. The colored graph should not include 
    neighboring nodes with the same color. The function is capable of performing the co-
    loring of a graph using two algorithms depending on the value of the attribute 
    coloring_order. The available algorithms are the coloring of the graph in degree_order
    and the coloring of the graph in alternate order.
    """

    """
    The worst case scenario can happen when we need as many colors as the nodes of the graph.
    So the number of available colors should be equal to the number of nodes included in the graph.
    Each number in the "colors" list represents a different color
    """

    colors=["yellow","green","red","blue","orange","grey","purple","azure","violet","brown"]
    adj_nodes, assigned_colors, colorsAssignedtoNeighbors = [], [], [] 
    not_used_colors, existing_colors, nodeAndColor, final_colors = [], [], {}, []
    if coloring_order=="degree_order":
        order_of_nodes=nodesDescendingOrder(graph)
    elif coloring_order=="alternate_order":
        order_of_nodes=alternateOrder(graph)[0]
    #print order_of_nodes
    nodeAndColor[order_of_nodes[0]]=colors[0] #assign a color to the first node of the order_of_nodes list
    assigned_colors.append(colors[0])
    for i in range (1, nx.number_of_nodes(graph)):    
        adj_nodes.extend(graph.neighbors(order_of_nodes[i])) #nodes connected to the node with the highest degree 
        #print("The adj nodes of node %s are: %s" %(order_of_nodes[i],set(adj_nodes)))
        adj_nodes=list(set(adj_nodes))
        for adj_node in adj_nodes:
            for key, value in nodeAndColor.iteritems():
                if adj_node==key:
                    colorsAssignedtoNeighbors.append(value)
        #print("The colors that are assigned to neighbors are %s" %set(colorsAssignedtoNeighbors))
        #print("The colors that have been assigned so far are %s" %set(assigned_colors))
        if set(colorsAssignedtoNeighbors) == set(assigned_colors):
            not_used_colors=list(set(colors)-set(assigned_colors))
            assigned_colors.append(not_used_colors[0])
            nodeAndColor.update({order_of_nodes[i]:not_used_colors[0]})
            #print("The non used colors are %s" %not_used_colors)
            #print("The assigned color of node %s is %s" %(order_of_nodes[i],not_used_colors[0]))
        else:
            existing_colors=list(set(assigned_colors)-set(colorsAssignedtoNeighbors)) 
            nodeAndColor.update({order_of_nodes[i]:existing_colors[0]})
            #print("The colors that exist on the graph and have NOT been assigned to neighbors are %s" %existing_colors)
            #print("*The assigned color of node %s is %s" %(order_of_nodes[i],existing_colors[0]))
        colorsAssignedtoNeighbors, existing_colors, adj_nodes, not_used_colors=[], [], [], []
    
    #print the colored auxiliary graph
    [final_colors.append(nodeAndColor[i]) for i in range(1, len(nodeAndColor)+1)]
       
    #printGraph(graph, final_colors) 
    #print final_colors
    print("Node and color %s" %nodeAndColor)
    return (nodeAndColor,final_colors)

def drawColoredPathsOnGivenGraph(graph, auxiliaryGraph, followed_path, coloring_algorithm):
    print("The followed path is %s" %followed_path)
    paths=[]
    for no_of_route, path in followed_path.iteritems():
        paths.append(list(path))
    print paths
    #colors=[]
    if coloring_algorithm=="degree_order":
        colors=copy.copy(coloringGraph(auxiliaryGraph, "degree_order")[1])
        #for no_of_route, color in coloringGraph(graph, "degree_order")[0].iteritems():
        #    colors.append(color)
    elif coloring_algorithm=="alternate_order":
        colors=copy.copy(coloringGraph(auxiliaryGraph, "alternate_order")[1])
    print("This is what is returned %s" %(coloringGraph(auxiliaryGraph, "degree_order")[1]))
    #colors=tuple(colors)
    print colors
    print("The paths are %s" %paths)
    pos=nx.drawing.spring_layout(graph)
    pathdr.normalize_layout(pos)
    nx.draw_networkx_labels(graph, pos, font_size=14, font_family="sans-serif")
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="red")
    nx.draw_networkx_edges(graph, pos, width=4, edge_color="black")
    plt.axis("off")  
    pathdr.draw_many_paths(graph, pos, paths, colors, max_shift=0.03)
    plt.show()