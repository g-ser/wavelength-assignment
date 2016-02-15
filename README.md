# wavelength-assignment
The scripts of the current repository are intended to solve the problem of wavelength assignment which can be stated as follows: given a graph with a set of nodes connected with fiber links (optical fiber network) and a set of lightpaths and their routes, assign a wavelength to each lightpath, in a way that no two lightpaths share the same wavelength on a given fiber link (any two lightpaths that are sharing the same physical link are assigned different wavelengths). In addition, the assignment of wavelengths should be done in a way that minimizes the number of wavelengths used. The problem can be seen as a graph-coloring problem which consists of the two following steps:
+ Construction of the auxiliary graph: Each lightpath becomes a node (vertex) in the auxiliary graph. When two lightpaths share the same fiber link, the corresponding vertices of the auxiliary graph should be connected. 
+ Color the nodes of the auxiliary graph such that no two adjacent nodes have the same color. Module [assignwavelengths.py](https://github.com/g-ser/wavelength-assignment/blob/master/assignwavelengths.py) includes function coloringGraph which is able to perform the coloring of a given graph using two different algorithms based on the input given to the function.  
⋅⋅*Coloring in degree order
....1. Assign to the node with the highest degree in the auxiliary graph a color. If there are a lot of nodes with the same degree just choose randomly one of them.
....2. Go to the node with the highest degree which is not painted so far. 
....3. For the node that you chose at step 2 check its neighboring nodes. 
........a. If all the colors that have been assigned so far are in the neighbors of the node that you chose at step 2 then assign a new color to the node
........b. If a is not true then assign to the node an already assigned color
....4. Are there more nodes on the auxiliary graph?
........a. If 4 is true then go to step 2
........b. If 4 is NOT true then go to step 5
....5. Terminate the algorithm 

⋅⋅* Coloring in alternate order


##Illustrative Example
An example will be presented below in order to illustrate how the wave length assignment works. In the example below, the auxiliary graph is colored using both the Also the number of colors that are going to be used are estimated 


First of all we have to introduce the graph which will be the basis for our example. The "original" graph has been decided to be the one depicted below. 

![alt tag](https://raw.githubusercontent.com/g-ser/wavelength-assignment/master/pictures/givengraph.png)