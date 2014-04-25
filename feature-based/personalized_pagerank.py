import operator
import networkx as nx
import utilities


FILE_PATH = "../data/facebook-combined.data"

class PersonalizedPageRank:
    NUM_ITERATIONS = 3
    MAX_NODES_TO_COMPARE = 50

    def __init__(self, _nx_graph):
        self.nx_graph = _nx_graph

    def get_page_rank(self, user):
        # Dict from user_id to probability score
        probabilities = {}

        # We start at this user.
        probabilities[user] = 1.0

        # Get the PageRank Probabilities
        pageRankProbabilities = self.page_rank_helper(user, probabilities, self.NUM_ITERATIONS, 0.5)

        # Convert the dict to list of tuples and sort it according to probability
        probabilitiesList = pageRankProbabilities.items()
        probabilitiesList.sort(key=operator.itemgetter(1), reverse=True)

        if len(probabilitiesList) < self.MAX_NODES_TO_COMPARE:
            return probabilitiesList

        return probabilitiesList[:self.MAX_NODES_TO_COMPARE]

    def get_followings(self, user):
        if self.nx_graph.has_node(user):
            return set(self.nx_graph.successors(user))
        else:
            print "Not in Graph"
            return set()

    def get_followers(self, user):
        if self.nx_graph.has_node(user):
            return set(self.nx_graph.predecessors(user))
        else:
            print "Not in Graph"
            return set()

    def page_rank_helper(self, start_user, probabilities, num_iterations, alpha = 0.5):
        # print "Num Iteration:", num_iterations, "Probabilities:", probabilities

        if num_iterations <= 0:
            # print "End of Iteration", num_iterations, "Probabilities:", probabilities
            return probabilities

        # This map holds the updated set of probabilities, after the current iteration.
        probabilities_propagated = {}

        # With probability 1 - alpha, we teleport back to the start node.
        probabilities_propagated[start_user] = 1.0 - alpha

        # Propagate the previous probabilities...
        for user_id, probability in probabilities.iteritems():
            forwards = self.get_followings(user_id)
            backwards = self.get_followers(user_id)

            if len(forwards) == 0 and len(backwards) == 0:
                print "User_id with zero forward and backward:", user_id

            probability_to_propagate = (alpha * probability)/(len(forwards) + len(backwards))
            # print "Probability to propagate:", probability_to_propagate

            neighbours = forwards.union(backwards)

            for neighbour in neighbours:
                if not neighbour in probabilities_propagated:
                    probabilities_propagated[neighbour] = 0
                
                probabilities_propagated[neighbour] += probability_to_propagate

        return self.page_rank_helper(start_user, probabilities_propagated, num_iterations - 1, alpha)

def get_followers_and_followings(filename):
    pass

def save_to_compare_list_to_file(to_compare_list, nx_graph, filename):
    f = open(filename, 'w')

    for user_id, probabilityList in to_compare_list.iteritems():
        for entry in probabilityList:
            if user_id != entry[0]:
                f.write(str(user_id) + ", " + str(entry[0]) + ", " + str(entry[1]))
                if nx_graph.has_edge(user_id, entry[0]):
                    f.write(", 1\n")
                else:
                    f.write(", 0\n")

    f.close()

def main():
    nx_graph = utilities.read_graph(FILE_PATH)
    print "NetworkX Directed Graph (V,E): (", nx_graph.number_of_nodes(), ",", nx_graph.number_of_edges(), ")"

    # Create the Personalized pagerank class object
    ppr = PersonalizedPageRank(nx_graph)

    # Calculate the to compare list for each node by selecting the nodes with the best personalized pagerank score for each node
    to_compare_list = {}
    for user_id in nx_graph.nodes():
        if user_id % 100 == 1:
            print "Running for", user_id

        to_compare_list[user_id] = ppr.get_page_rank(user_id)

    save_to_compare_list_to_file(to_compare_list, nx_graph, "to_compare_list.txt")

if __name__ == "__main__":
    main()
