import numpy as np
from numpy.linalg import norm
from itertools import chain
from scipy.stats import hmean, gmean


def get_similarity_matrix(embeddings) -> np.ndarray:
    similarity_matrix = custom_matmul(embeddings, embeddings)
    return similarity_matrix


def custom_matmul(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    def memo_vectors_norm(mat: np.ndarray):
        """
        for Dynamic Programming
        """
        vectors_norm_dict = dict()
        for idx, vector in enumerate(mat):
            vectors_norm_dict[idx] = norm(vector)
        return vectors_norm_dict
    A_norms = memo_vectors_norm(A)
    B_norms = memo_vectors_norm(B)
    inner_prod_mat = A @ B.T
    for i in range(len(A)):
        for j in range(len(B)):
            regularization_term = A_norms[i] * B_norms[j]
            inner_prod_mat[i][j] /= regularization_term
    return inner_prod_mat


def calculate_threshold(vs: list, mean: str):
    if mean == "geometric":
        growths = [vs[i+1]/v for i, v in enumerate(vs[:-1])]
        return gmean(growths)
    elif mean == "harmonic":
        return hmean(vs)
    elif mean == "weighted harmonic":
        def weighted_harmonic_mean(vs):
            weights = list(range(len(vs), 0, -1))
            return sum(weights) / sum([weight*(1/vs[i]) for i, weight in enumerate(weights)])
        return weighted_harmonic_mean(vs)


def initialize_adjacency_matrix(similarity_matrix: np.ndarray) -> float:
    similarities = list(chain(*similarity_matrix.tolist()))
    similarities = list(filter(lambda similarity: similarity < 1, similarities))
    similarities = list(sorted(similarities, reverse=True))
    threshold = calculate_threshold(similarities, mean='weighted harmonic')
    similarity_matrix[similarity_matrix<threshold] = 0
    similarity_matrix[similarity_matrix>threshold] = 1
    return similarity_matrix


def initialize_adjacency_dict(adjcency_matrix: np.ndarray) -> dict:
    adjacency_dict = dict()
    adjcency_matrix = adjcency_matrix.tolist()
    for i, connections in enumerate(adjcency_matrix):
        for j, connection in enumerate(connections):
            if connection > 0:
                adjacency_dict.setdefault(i, list()).append(j)
    return adjacency_dict



if __name__ == "__main__":
    embeddings = np.random.random(size=(3, 20))
    similarity_matrix = get_similarity_matrix(
            embeddings
    )
    adjacency_matrix = initialize_adjacency_matrix(similarity_matrix)
    initialize_adjacency_dict(adjacency_matrix)
    
