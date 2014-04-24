import networkx as nx
import utilities

FILE_PATH = "../data/sampled_train_small.csv"
SAVE_FILE = "shortestpaths.txt"

def get_shortest_path(nx_graph):
    print 'Calculating the All Pairs Shortest Path Lengths'
    length = nx.all_pairs_shortest_path_length(nx_graph)

    print "Length of Dict", len(length)

    print "Saving to file"
    utilities.save_obj(length, SAVE_FILE)

    print "Reading it back from file"
    written_length = utilities.load_obj(SAVE_FILE)
    print "Length of Dict:", len(written_length)


def main():
    nx_graph = utilities.read_graph(FILE_PATH)
    print "NetworkX Directed Graph (V,E): (", nx_graph.number_of_nodes(), ",", nx_graph.number_of_edges(), ")"

    get_shortest_path(nx_graph)
if __name__ == "__main__":
    main()

