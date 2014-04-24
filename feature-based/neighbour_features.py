import math
import networkx as nx

class Features:
    def __init__(self):
        pass

    @staticmethod
    def num_common_neighbors(nx_graph, user1, user2):
        common_neighbors = set(nx_graph.neighbors(user1)).intersection(set(nx_graph.neighbors(user2)))
        return len(common_neighbors)

    @staticmethod
    def adar_adamic_score(nx_graph, user1, user2):
        common_neighbors = nx_graph[user1].intersection(nx_graph[user2])

        if len(common_neighbors) == 0:
            return 0.0

        adar_adamic = 0.0
        for neigbor in common_neighbors:
            adar_adamic += (-math.log10(len(nx_graph[neigbor])))

        return adar_adamic

    @staticmethod
    def jaccard_coefficient(nx_graph, user1, user2):
        common_neighbors = nx_graph[user1].intersection(nx_graph[user2])
        union_neighbours = nx_graph[user1].union(nx_graph[user2])

        if len(union_neighbours) == 0:
            return 0

        return float(len(common_neighbors))/len(union_neighbours)

    @staticmethod
    def preferential_attachment(nx_graph, user1, user2):
        return (len(nx_graph[user1]) * len(nx_graph[user2]))

    @staticmethod
    def cosine_similarity(nx_graph, user1, user2):
        if len(nx_graph[user1]) == 0 or len(nx_graph[user2]) == 0:
            return 0

        common_neighbors = nx_graph[user1].intersection(nx_graph[user2])
        return float(len(common_neighbors))/(len(nx_graph[user1]) * len(nx_graph[user2]))

    @staticmethod
    def get_all_features(nx_graph, user1, user2):
        # To hold all the feature values
        features = []

        # Get the neighbors for both the users
        user1_neighbors = set(nx_graph.neighbors(user1))
        user2_neighbors = set(nx_graph.neighbors(user2))

        # Get the Intersection and the union of the neighbors
        common_neighbors = user1_neighbors.intersection(user2_neighbors)
        union_neighbors = user1_neighbors.union(user2_neighbors)

        # Append the number of common neighbors
        features.append(float(len(common_neighbors)))

        # Append the Adar-Adamic Score and Jaccard Coefficent
        if len(common_neighbors) == 0:
            features.append(0.0)
            features.append(0.0)
        else:
            adar_adamic = 0.0
            for neighbor in common_neighbors:
                adar_adamic += (-math.log10(len(nx_graph[neighbor])))
            features.append(adar_adamic)
            features.append(float(len(common_neighbors))/len(union_neighbors))

        # Append the Preferential Attachment
        features.append(float(len(user1_neighbors) * len(user2_neighbors)))

        # Append the cosine Similarity
        if len(user1_neighbors) == 0 or len(user2_neighbors) == 0:
            features.append(0.0)
        else:
            features.append(float(len(common_neighbors))/(len(user1_neighbors) * len(user2_neighbors)))

        return features






