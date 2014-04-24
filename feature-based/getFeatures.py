import numpy as np
import networkx as nx
import utilities
from neighbour_features import Features

FILE_NAME = "to_compare_list.txt"
FILE_PATH = "../data/sampled_train_small.csv"

# Read the data from the file into numpy array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

def main():
    nx_graph = utilities.read_graph(FILE_PATH)
    print "NetworkX Directed Graph (V,E): (", nx_graph.number_of_nodes(), ",", nx_graph.number_of_edges(), ")"

    data = get_data(FILE_NAME, ",")
    candidate_nodes = data[:, :2]
    candidate_nodes = candidate_nodes.astype(int)

    features = []
    for node_pair in candidate_nodes:
        neighbour_feature_list = Features.get_all_features(nx_graph, node_pair[0], node_pair[1])
        graph_feature_list = []

if __name__ == "__main__":
    main()

