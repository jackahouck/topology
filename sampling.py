import numpy as np

class Holes:
    def __init__(self, centers, R):
        self.centers = centers
        self.R = R

def place_holes(N, R, max_attempts=10000):
    if R >= 1:
        raise ValueError("R must be less than 1 to fit any hole in the unit disk.")

    centers = []
    attempts = 0

    while len(centers) < N:
        if attempts >= max_attempts:
            raise ValueError(
                f"Could only place {len(centers)}/{N} holes after {max_attempts} attempts. "
                "Try smaller R or fewer holes."
            )

        # Sample uniformly from the disk of radius (1 - R)
        # so the hole stays inside the unit disk
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, (1 - R) ** 2))
        candidate = np.array([r * np.cos(angle), r * np.sin(angle)])

        # Check no overlap with existing holes
        too_close = any(
            np.linalg.norm(candidate - c) < 2 * R for c in centers
        )

        if not too_close:
            centers.append(candidate)

        attempts += 1

    return Holes(centers=np.array(centers), R=R)

def sample_points(M, holes, max_attempts=10000):
    points = []
    batch_size = M * 10  

    while len(points) < M:
        angles = np.random.uniform(0, 2 * np.pi, batch_size)
        radii = np.sqrt(np.random.uniform(0, 1, batch_size))
        candidates = np.column_stack([radii * np.cos(angles), radii * np.sin(angles)])

        for candidate in candidates:
            dists = np.linalg.norm(holes.centers - candidate, axis=1)
            if np.all(dists >= holes.R):
                points.append(candidate)
            if len(points) == M:
                break

        if len(points) < M:
            batch_size *= 2  

    return np.array(points[:M])


if __name__ == "__main__":
    holes = place_holes(N=5, R=0.1)
    points = sample_points(M=100, holes=holes)
    print(f"Placed {len(holes.centers)} holes")
    print(f"Sampled {len(points)} points")
    print(points)