import numpy as np
import pyvista as pv
from sampling import place_holes, sample_points
from vietoris_rips import vietoris_rips
from cech import cech_complex


def render_complex(points, complex, holes, title="Simplicial Complex"):
    pts3d = np.column_stack([points, np.zeros(len(points))])

    plotter = pv.Plotter()
    plotter.set_background("white")
    plotter.title = title

    # vertices
    point_cloud = pv.PolyData(pts3d)
    plotter.add_mesh(point_cloud, color="red", point_size=12, render_points_as_spheres=True)

    # edges
    lines = []
    for (i, j) in complex[1]:
        lines += [2, i, j]
    if lines:
        edge_mesh = pv.PolyData(pts3d, lines=lines)
        plotter.add_mesh(edge_mesh, color="black", line_width=2)

    # faces
    faces = []
    for (i, j, k) in complex[2]:
        faces += [3, i, j, k]
    if faces:
        face_mesh = pv.PolyData(pts3d, faces)
        plotter.add_mesh(face_mesh, color="steelblue", opacity=0.4, show_edges=True)

    # tetrahedra
    tet_lines = []
    for (i, j, k, l) in complex[3]:
        for a, b in [(i,j),(i,k),(i,l),(j,k),(j,l),(k,l)]:
            tet_lines += [2, a, b]
    if tet_lines:
        tet_mesh = pv.PolyData(pts3d, lines=tet_lines)
        plotter.add_mesh(tet_mesh, color="purple", line_width=3)

    # draw unit disk boundary
    circle = pv.Circle(radius=1.0)
    plotter.add_mesh(circle, color="steelblue", opacity=0.1)

    # draw holes
    for c in holes.centers:
        hole = pv.Circle(radius=holes.R)
        hole.translate([c[0], c[1], 0], inplace=True)
        plotter.add_mesh(hole, color="white", opacity=0.8)
        hole_edge = pv.Circle(radius=holes.R)
        hole_edge.translate([c[0], c[1], 0], inplace=True)
        plotter.add_mesh(hole_edge, color="navy", opacity=1.0, style="wireframe")

    plotter.view_xy()
    plotter.show()

    return complex


if __name__ == "__main__":
    holes = place_holes(N=7, R=0.1)
    points = sample_points(30, holes=holes)
    r = 0.2

    print(len(points))
    # Uncomment for Cech or VR
    #complex = vietoris_rips(points, r)
    complex = cech_complex(points, r)

    result = render_complex(points, complex, holes, title="Cech Complex")
    print(result)