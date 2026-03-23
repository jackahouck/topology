import numpy as np

def sample_holes(N, R, max_attempts=10000):
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

    return np.array(centers)

if __name__ == "__main__":
    points = sample_holes(N=10, R=0.1)
    print(points)