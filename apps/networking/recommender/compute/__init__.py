"""
В этом пакете реализована обертка вокруг усеченного алгоритма рекомендаций контактов,
использованного на Остро1021
"""
from .compute_prereq import compute_similarities
from .old import SimilarityBasedNetworkingRecommender