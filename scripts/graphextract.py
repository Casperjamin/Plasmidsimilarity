
import networkx as nx

class assemblygraph():
    def __init__(self, inputgraph):
        self.graph = graph_read(inputgraph)[0]
        self.contigs = graph_read(inputgraph)[1]


    def graph_to_fasta(self, outputloc):
        with open(f"{outputloc}.fasta", "w") as f:
            for contignumber, sequence in self.contigs.items():
                f.write(f">{contignumber}\n{sequence}\n")



    def graph_to_plasmids(self, outputloc, lower, upper):
        """
        placeholder for now
        """
        graphcomponents = list(nx.connected_components(self.graph))

        count = 0
        for element in graphcomponents:

            size = sum([int(nx.get_node_attributes(self.graph, "weight")[str(i)]) for i in element])
            print(f"graph element of size {size} encountered")
            if not lower < size < upper:
                print(f"The size of this connected component is not inside the specified range of {lower} to {upper}")
                print("Therefore not outputting these contigs")
            else:
                count += 1
                print("outputting this element into a FASTA")
                with open(f"{outputloc}_plasmid_{count}.fasta", "w") as f:
                    for i in element:
                        f.write(f">{i}\n{self.contigs[str(i)]}\n")





def graph_read(inputfile):
    """
    take a GFA file and return a networkx graph and dictionary with the contigs
    """
    graph = nx.Graph()
    contigsdictionary = {}
    with open(inputfile, 'r') as f:
        for line in f.readlines():
            splitline = line.split("\t")

            if splitline[0] == 'S':
                #add the nodes into the graph
                nodelabel = splitline[1]

                contigsdictionary[str(nodelabel)] = splitline[2]

                #size of the contig
                nodesize = splitline[3][5:]
                graph.add_node(nodelabel, weight = nodesize)

            if splitline[0] == "L":
                #add the edges to the previous nodes
                connect1 = splitline[1]
                connect2 = splitline[3]
                graph.add_edge(connect1, connect2)

    return graph, contigsdictionary
