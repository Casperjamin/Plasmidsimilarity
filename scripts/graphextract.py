
import networkx as nx

class assemblygraph():
    def __init__(self, inputgraph):
        self.graph = graph_read(inputgraph)[0]
        self.contigs = graph_read(inputgraph)[1]


    def graph_to_fasta(self, outputloc):
        with open(f"{outputloc}.fasta", "w") as f:
            for contignumber, sequence in self.contigs.items():
                f.write(f">{contignumber}\n{sequence}\n")





def graph_read(inputfile):
    """take a GFA file and turn in into a networkx graph
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



"""
a = graph_read(inputfile = inputfile)

a.nodes()

comps = list(nx.connected_components(a))


for comp in comps:
    print(sum([int(nx.get_node_attributes(a, "weight")[str(i)]) for i in comp]))
"""
