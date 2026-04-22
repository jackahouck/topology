import numpy as np
from scipy.spatial.distance import pdist, squareform
from itertools import combinations
from sampling import place_holes, sample_points


def vietoris_rips(points, r):
    N = len(points)
    dist = squareform(pdist(points))
    threshold = 2 * r

    complex = {0: [], 1: [], 2: [], 3: []}

    complex[0] = list(combinations(range(N), 1))

    for simplex in combinations(range(N), 2):
        i, j = simplex
        if dist[i][j] <= threshold:
            complex[1].append(simplex)

    edge_set = set(complex[1])

    for dim in range(2, 4):
        for simplex in combinations(range(N), dim + 1):
            if any((i, j) not in edge_set for i, j in combinations(simplex, 2)):
                continue
            if all(dist[i][j] <= threshold for i, j in combinations(simplex, 2)):
                complex[dim].append(simplex)

    return complex


if __name__ == "__main__":
    holes = place_holes(N=5, R=0.1)
    points = sample_points(M=50, holes=holes)   
    r = 0.3

    vr = vietoris_rips(points, r)

    for dim, simplices in vr.items():
        print(f"Dimension {dim}: {len(simplices)} simplices")
        for s in simplices:
            print(f"  {s}")
