import numpy as np
import networkx as nx
import utilities
from neighbour_features import Features

FILE_NAME = "to_compare_list.txt"
FILE_PATH = "../data/facebook_combined.txt"

# Read the data from the file into numpy array and returns the array
def get_data(filename, delimiter_type):
    data = np.genfromtxt(filename, delimiter=delimiter_type)
    return data

def main():
    nx_graph = utilities.read_graph(FILE_PATH)
    print "NetworkX Directed Graph (V,E): (", nx_graph.number_of_nodes(), ",", nx_graph.number_of_edges(), ")"

    data = get_data(FILE_NAME, ",")

    features_list = []
    for node_pair in data:
        neighbour_feature_list = Features.get_all_features(nx_graph, int(node_pair[0]), int(node_pair[1]))

	features = []
    	features.append(int(node_pair[0]))
    	features.append(int(node_pair[1]))
    	features.append(node_pair[2])
    	features.extend(neighbour_feature_list)
    	features.append(node_pair[3])
	features_list.append(features)

    a = np.asarray(features_list)
    print a.shape
    np.savetxt("features_data.csv", a, delimiter=",")
    

if __name__ == "__main__":
    main()

