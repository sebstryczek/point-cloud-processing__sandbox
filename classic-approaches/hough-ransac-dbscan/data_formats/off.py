import numpy as np

def read(file_path):
    with open(file_path, 'r') as f:
        if 'OFF' != f.readline().strip():
            raise ValueError('Not a valid OFF header')
        n_verts, n_faces, n_edges = tuple(map(int, f.readline().strip().split(' ')))
        
        verts = []
        for i in range(n_verts):
            verts.append(list(map(float, f.readline().strip().split(' '))))

        faces = []
        for i in range(n_faces):
            faces.append(list(map(int, f.readline().strip().split(' ')))[1:])

        return np.array(verts)
