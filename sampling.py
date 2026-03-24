import numpy as np

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

    return np.array(centers)

def sample_points(M, hole_centers, R, max_attempts=10000):
    points = []
    attempts = 0

    while len(points) < M:
        if attempts >= max_attempts:
            raise ValueError(
                f"Could only sample {len(points)}/{M} points after {max_attempts} attempts. "
                "Try fewer points or smaller holes."
            )

        # Sample uniformly from the unit disk
        angle = np.random.uniform(0, 2 * np.pi)
        r = np.sqrt(np.random.uniform(0, 1))
        candidate = np.array([r * np.cos(angle), r * np.sin(angle)])

        # Reject if inside any hole
        in_hole = any(
            np.linalg.norm(candidate - c) < R for c in hole_centers
        )

        if not in_hole:
            points.append(candidate)

        attempts += 1

    return np.array(points)


if __name__ == "__main__":
    hole_centers = place_holes(N=5, R=0.1)
    points = sample_points(M=50, hole_centers=hole_centers, R=0.1)
    print(f"Placed {len(hole_centers)} holes")
    print(f"Sampled {len(points)} points")
    print(points)