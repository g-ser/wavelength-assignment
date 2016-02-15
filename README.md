# wavelength-assignment
The scripts of the current repository are intended to solve the problem of wavelength assignment which can be stated as follows: given a graph with a set of nodes connected with fiber links (optical fiber network) and a set of lightpaths and their routes, assign a wavelength to each lightpath, in a way that no two lightpaths share the same wavelength on a given fiber link (any two lightpaths that are sharing the same physical link are assigned different wavelengths). In addition, the assignment of wavelengths should be done in a way that minimizes the number of wavelengths used. The problem can be seen as a graph-coloring problem which consists of the two following steps:
 
* **Construct the auxiliary graph**: Each lightpath becomes a node (vertex) in the auxiliary graph. When two lightpaths share the same fiber link, the corresponding vertices of the auxiliary graph should be connected. 
* **Color the nodes of the auxiliary graph such that no two adjacent nodes have the same color.** Module [assignwavelengths.py](https://github.com/g-ser/wavelength-assignment/blob/master/assignwavelengths.py) includes function coloringGraph which is able to perform the coloring of a given graph using two different algorithms based on the input given to the function:
  * **Coloring in degree order**:
    1. Assign to the node with the highest degree in the auxiliary graph a color. If there are a lot of nodes with the same degree just choose randomly one of them.
    2. Go to the node with the highest degree which is not painted so far. 
    3. For the node that you chose at step b check its neighboring nodes. 
       * If all the colors that have been assigned so far are in the neighbors of the node that you chose at step b then assign a new color to the node
       * If a is not true then assign to the node an already assigned color
    4. Are there more nodes on the auxiliary graph?
       * If d is true then go to step b
       * If d is NOT true then go to step e
    5. Terminate the algorithm 

  * **Coloring in alternate order**:
    1. Assign to the node with the smallest degree in the auxiliary graph a color 
    2. Go to the node that has the next smallest degree (when a node's degree is calculated, the edges with its neighbors that have been proceeded (colored) by the algorithm are not considered) 
    3. For the node that you pick at step b check its neighboring nodes. 
       * If all the colors that have been assigned so far are in the neighbors of the node (that you chose at step b), then assign a new color to the node otherwise assign to the node an already assigned color
    4. Are there elements in delete_order vector that have not been accessed so far?
       * If d is true then go to step b
       * If d is NOT true then go to step e
    5. Terminate the algorithm 


## Illustrative Example
An example will be presented below in order to illustrate how the wavelength assignment works. By running the script named as [testongivengraph.py](https://github.com/g-ser/wavelength-assignment/blob/master/testongivengraph.py), the results shown below are derived. In the example below, the auxiliary graph is colored using both coloring in degree order and then coloring in alternate order. Also, in both cases, we estimate the number of colors that are going to be used.  

First of all we have to introduce the graph which will be the basis for our example. The "original" graph has been decided to be the one depicted below. As can be seen, each of the edges that connect the nodes of the graph (you can imagine the edges as fiber links in an optical fiber network) is assigned with a weight which will be used as an input to the shortest path algorithm in order to find the intermediate nodes based on the source and destination node of a given lightpath. 

![alt tag](https://raw.githubusercontent.com/g-ser/wavelength-assignment/master/pictures/givengraph.png)

### Choose a set of lightpaths and run the shortest path algorithm.

We also have to pick some lightpaths. See the table below for the chosen lightpaths (no particular reason for choosing the ones shown bellow).

 No. of lightpath |   Source node  | Destination node
 -----------------|----------------|------------------
 1                |9               |11
 2                |11              |6
 3                |6               |7
 4                |9               |7
 5                |1               |6
 6                |7               |1
 7                |11              |8

After running the shortest path algorithm, we find the intermediate nodes of each of the above paths. 

 No. of lightpath |   Source node  | Intermediate Nodes |Destination node
 -----------------|----------------|--------------------|------------------
 1                |9               |2,3,5               |11
 2                |11              |5,4                 |6
 3                |6               |4,10,3              |7
 4                |9               |2,3                 |7
 5                |1               |2,4                 |6
 6                |7               |3,2                 |1
 7                |11              |5                   |8

### Construction of the auxiliary graph.

 The next step is to make the **auxiliary graph** as described before. Note that each of the lightpaths, now becomes a node in the auxiliary graph.    

 ![alt tag](https://raw.githubusercontent.com/g-ser/wavelength-assignment/master/pictures/auxiliarygraph.png)

### Estimation of needed colors in degree order

The estimation is based on the auxiliary graph and the identity function. We have to plot the identity function and the degrees of the nodes in descending order that are included in the auxiliary graph (starting from the node with the greatest degree, then moving to the node with the next highest degree etc). The point of the intersection increased by one, gives the estimation of the colors needed colors to color the auxiliary graph in degree order.

