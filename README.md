# wavelength-assignment
The scripts of the current repository are intended to solve the problem of wavelength assignment which can be stated as follows: given a graph with a set of nodes connected with fiber links (optical fiber network) and a set of lightpaths and their routes, assign a wavelength to each lightpath in a way that no two lightpaths share the same wavelength on a given fiber link (any two lightpaths that are sharing the same physical link are assigned different wavelengths). In addition, the assignment of wavelengths should be done in a way that minimizes the number of wavelengths used. The problem can be seen as a graph-coloring problem which consists of the two following steps:
+ Construction of the auxiliary graph: Each lightpath becomes a node (vertex) in the auxiliary graph. When two lightpaths share the same fiber link, the corresponding vertices of the auxiliary graph should be connected. 
+ Color the nodes of the auxiliary graph such that no two adjacent nodes have the same color. Module [assignwavelengths.py](https://github.com/g-ser/wavelength-assignment/blob/master/assignwavelengths.py) includes method 
![alt tag](https://raw.githubusercontent.com/g-ser/wavelength-assignment/master/pictures/givengraph.png)