import numpy as np

def read(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            
            try:
                x, y, z = map(float, line.strip().split(","))
                points.append([x, y, z])
            except ValueError:
                continue

    return np.array(points)
