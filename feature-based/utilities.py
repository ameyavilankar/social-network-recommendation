import csv
import matplotlib.pyplot as plt
import networkx as nx
import pickle

def plot_distribution(nx_graph, filename):
    """
    Plots the in/out degree distribution of the Graph

    :rtype : None
    :param nx_graph: nx.Digraph() - Directed NetworkX Graph
    :param filename: String - Name of the file to save the plot
    """
    in_degrees = nx_graph.in_degree()
    in_values = sorted(set(in_degrees.values()))

    out_degrees = nx_graph.out_degree()
    out_values = sorted(set(out_degrees.values()))

    in_hist = [in_degrees.values().count(x) for x in in_values]
    out_hist = [out_degrees.values().count(x) for x in out_values]

    plt.clf()
    plt.cla()
    plt.figure()
    plt.plot(in_values, in_hist,'ro-') # in-degree
    plt.plot(out_values, out_hist,'bv-') # out-degree
    # plt.yscale('log')
    plt.legend(['In-degree','Out-degree'])
    plt.xlabel('Degree')
    plt.ylabel('Number of nodes')
    plt.title('In-Out Degree Distribution')
    plt.savefig(filename + '.png', format='png')
    plt.close()

def edges_generator(file_name):
    """
    Generator that returns edges given a 2-column csv graph file

    :rtype : list - List of 2 nodes where list[0] is source and list[1] is destination of the edge
    :param file_name: String - The name of the file to read the edges from
    """
    f = open(file_name)
    reader = csv.reader(f)

    # Ignore the header
    reader.next()

    for edges in reader:
        nodes = [int(node) for node in edges]
        yield nodes

    f.close()

def read_graph(file_name):
    """
    Reads a sparsely represented directed graph into a dictionary

    :param file_name: String - The name of the file to read the edges from
    :rtype : nx.DiGraph() - A directed Graph created from edges in the file
    """
    nx_graph = nx.DiGraph()

    for nodes in edges_generator(file_name):
        # Get the destination and the source nodes
        source = nodes[0]
        destination = nodes[1]

        # Add Edge to the Graph
        nx_graph.add_edge(source, destination)
        nx_graph.add_edge(destination, source)

    return nx_graph


def write_submission_file(submission_file, test_nodes, test_predictions):
    """
    Writes the submission file

    :rtype : None
    :param submission_file: String - Name of the file to write the output
    :param test_nodes: list - List of source Nodes
    :param test_predictions: list - List of destination Nodes
    """
    f = open(submission_file, "w")
    writer = csv.writer(f)
    writer.writerow(["source_node", "destination_nodes"])

    for source_node, destination_nodes in zip(test_nodes, test_predictions):
        writer.writerow([str(source_node),
                         " ".join([str(n) for n in destination_nodes])])
    f.close()

def save_obj(obj, name ):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name, 'r') as f:
        return pickle.load(f)

def main():
    nx_graph = read_graph("../data/facebook-combined.data")
    print "NetworkX Directed Graph (V,E): (", nx_graph.number_of_nodes(), ",", nx_graph.number_of_edges(), ")"

    # Plot the in/out degree distribution
    plot_distribution(nx_graph, "graph_distribution")

if __name__ == "__main__":
    main()
