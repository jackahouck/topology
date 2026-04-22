import gudhi
import numpy as np

def compute_betti(points, complex):
    st = gudhi.SimplexTree()
    
    for dim, simplices in complex.items():
        for simplex in simplices:
            st.insert(list(simplex))
    
    st.compute_persistence()
    betti = st.betti_numbers()
    return betti

if __name__ == "__main__":
    from sampling import place_holes, sample_points
    from cech import cech_complex

    holes = place_holes(N=5, R=0.1)
    points = sample_points(M=30, holes=holes)
    r = 0.2

    complex = cech_complex(points, r)
    betti = compute_betti(points, complex)
    print(f"Betti numbers: {betti}")
    print(f"β0 (components): {betti[0]}")
    print(f"β1 (holes): {betti[1]}")
    print(f"β2 (2-holes): {betti[2] if len(betti) > 2 else 0}")

    