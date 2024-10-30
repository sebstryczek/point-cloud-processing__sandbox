import numpy as np
import open3d as o3d

def create_plane_mesh(plane_model, size):
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
        
    min_range = -size / 2
    max_range = size / 2

    abs_a = abs(a)
    abs_b = abs(b)
    abs_c = abs(c)

    if abs_a >= abs_b and abs_a >= abs_c:
        # Obliczamy x z równania płaszczyzny: x = -(By + Cz + D) / A
        def calculate_x(y, z):
            return -(b * y + c * z + d) / a
        # Generujemy punkty zmieniając y i z
        points = [
            [calculate_x(min_range, min_range), min_range, min_range],
            [calculate_x(max_range, min_range), max_range, min_range],
            [calculate_x(max_range, max_range), max_range, max_range],
            [calculate_x(min_range, max_range), min_range, max_range]
        ]
    elif abs_b >= abs_a and abs_b >= abs_c:
        def calculate_y(x, z):
            return -(a * x + c * z + d) / b
        points = [
            [min_range, calculate_y(min_range, min_range), min_range],
            [max_range, calculate_y(max_range, min_range), min_range],
            [max_range, calculate_y(max_range, max_range), max_range],
            [min_range, calculate_y(min_range, max_range), max_range]
        ]
    else:
        def calculate_z(x, y):
            return -(a * x + b * y + d) / c
        points = [
            [min_range, min_range, calculate_z(min_range, min_range)],
            [max_range, min_range, calculate_z(max_range, min_range)],
            [max_range, max_range, calculate_z(max_range, max_range)],
            [min_range, max_range, calculate_z(min_range, max_range)]
        ]
        
    vertices = np.array(points)
    triangles = np.array([[0, 1, 2], [0, 2, 3]])
    
    mesh = o3d.geometry.TriangleMesh()
    mesh.vertices = o3d.utility.Vector3dVector(vertices)
    mesh.triangles = o3d.utility.Vector3iVector(triangles)

    mesh.paint_uniform_color([1.0, 1.0, 0.0])
    mesh.compute_vertex_normals()
    
    return mesh
