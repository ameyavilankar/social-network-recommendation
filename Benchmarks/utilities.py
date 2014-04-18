import csv
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

def plot_distribution(distribution, filename):
    plt.clf()
    plt.cla()
    plt.plot(distribution, 'b-')
    plt.xlabel('Degree (Number of Edges)')
    plt.ylabel('Number of Nodes')
    plt.grid(True)
    plt.title(filename)
    plt.savefig(filename + '.png', format='png')

# Generator that returns edges given a 2-column csv graph file
def edges_generator(file_name):
    f = open(file_name)
    reader = csv.reader(f)

    # Ignore the header
    reader.next()

    for edges in reader:
        nodes = [int(node) for node in edges]
        yield nodes

    f.close()

# Reads a sparsely represented directed graph into a dictionary
def read_graph(file_name):
    # Store the graph as a dictionary of edges
    graph = {}

    # Used to get the in and out degree distributions
    num_followings = defaultdict(int)
    num_followers = defaultdict(int)

    def initialize_node(node):
        if node not in graph:
            graph[node] = []

    for nodes in edges_generator(file_name):
        for node in nodes:
            initialize_node(node)

        # Get the destination and the source nodes
        source = nodes[0]
        destination = nodes[1]

        # Add Edge to the Graph
        graph[source].append(destination)

        # Update the counts for the distributions
        num_followings[source] += 1
        num_followers[destination] += 1

    return (graph, num_followings, num_followers)


# Reads of single-column list of nodes
def read_nodes_list(test_file):
    f = open(test_file)
    reader = csv.reader(f)
    reader.next()  # ignore header

    nodes = []
    for row in reader:
        nodes.append(int(row[0]))
    return nodes
    f.close()


# Writes the submission file
def write_submission_file(submission_file, test_nodes, test_predictions):
    f = open(submission_file, "w")
    writer = csv.writer(f)
    writer.writerow(["source_node", "destinationination_nodes"])

    for source_node, destination_nodes in zip(test_nodes, test_predictions):
        writer.writerow([str(source_node),
                         " ".join([str(n) for n in destination_nodes])])
    f.close()


# Returns the Degree Distribution of the In/Out Graph
def degree_distribution(graph):
    # Find the maximum Degree in the graph
    max_degree = 0
    for node, num_edges in graph.iteritems():
        if num_edges > max_degree:
            max_degree = num_edges

    print "Max Degree:", max_degree

    # Calculate the Degree Distribution
    distribution = np.zeros(max_degree + 1)
    for node, num_edges in graph.iteritems():
        distribution[num_edges] += 1

    return distribution

def main():
    (graph, num_followings, num_followers) = read_graph("../Data/train.csv")
    print "Number of Nodes:", len(graph)

    following_distribution = degree_distribution(num_followings)
    followers_distribution = degree_distribution(num_followers)

    print "Following Distribution:", following_distribution.shape
    print "Follower Distribution:", followers_distribution.shape

    plot_distribution(following_distribution, "following_distribution")
    plot_distribution(followers_distribution, "followers_distribution")

if __name__ == "__main__":
    main()