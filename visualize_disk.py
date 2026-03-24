import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sampling import place_holes, sample_points


def visualize_holes(N, R, ax=None):
    centers = sample_holes(N, R)

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))

    # Draw the unit disk
    disk = plt.Circle((0, 0), 1, color="steelblue", alpha=0.3, zorder=1)
    disk_edge = plt.Circle((0, 0), 1, color="steelblue", fill=False, linewidth=2, zorder=2)
    ax.add_patch(disk)
    ax.add_patch(disk_edge)

    # Draw each hole and its center point
    for c in centers:
        hole = plt.Circle(c, R, color="white", zorder=3)
        hole_edge = plt.Circle(c, R, color="navy", fill=False, linewidth=1, zorder=4)
        ax.add_patch(hole)
        ax.add_patch(hole_edge)
        ax.plot(*c, "o", color="red", markersize=4, zorder=5)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect("equal")
    ax.set_title(f"Unit disk with {N} holes of radius {R}")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    visualize_holes(N=8, R=0.2)