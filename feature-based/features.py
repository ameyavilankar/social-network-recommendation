import math

class Features:
    def __init__(self):
        pass

    @staticmethod
    def num_common_neighbours(graph, user1, user2):
        common_neighbours = graph[user1].intersection(graph[user2])
        return len(common_neighbours)

    @staticmethod
    def adar_adamic_score(graph, user1, user2):
        common_neighbours = graph[user1].intersection(graph[user2])

        if len(common_neighbours) == 0:
            return 0.0

        adar_adamic = 0.0
        for neigbour in common_neighbours:
            adar_adamic += (-math.log10(len(graph[neigbour])))

        return adar_adamic

    @staticmethod
    def jaccard_coefficient(graph, user1, user2):
        common_neighbours = graph[user1].intersection(graph[user2])
        union_neighbours = graph[user1].union(graph[user2])

        if len(union_neighbours) == 0:
            return 0

        return float(len(common_neighbours))/len(union_neighbours)

    @staticmethod
    def preferential_attachment(graph, user1, user2):
        return (len(graph[user1]) * len(graph[user2]))

    @staticmethod
    def cosine_similarity(graph, user1, user2):
        if len(graph[user1]) == 0 or len(graph[user2]) == 0:
            return 0

        common_neighbours = graph[user1].intersection(graph[user2])
        return float(len(common_neighbours))/(len(graph[user1]) * len(graph[user2]))

    @staticmethod
    def get_all_features():
        pass