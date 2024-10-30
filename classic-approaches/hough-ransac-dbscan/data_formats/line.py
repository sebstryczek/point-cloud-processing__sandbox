import numpy as np
import open3d as o3d

def load_lines_from_txt(file_path):
    points = []
    lines = []
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("#"):
                continue
            
            try:
                center_x, center_y, center_z, direction_x, direction_y, direction_z, amount_of_points = map(float, line.strip().split())

                if amount_of_points < 10:
                    continue
                
                line_length = 10

                point_a_index = len(points)
                start_x = center_x - direction_x * line_length / 2
                start_y = center_y - direction_y * line_length / 2
                start_z = center_z - direction_z * line_length / 2
                points.append([start_x, start_y, start_z])

                point_b_index = len(points)
                end_x = center_x + direction_x * line_length / 2
                end_y = center_y + direction_y * line_length / 2
                end_z = center_z + direction_z * line_length / 2
                points.append([end_x, end_y, end_z])
                

                lines.append([point_a_index, point_b_index])
                
            except ValueError:
                continue

    line_set = o3d.geometry.LineSet()
    line_set.points = o3d.utility.Vector3dVector(np.array(points))
    line_set.lines = o3d.utility.Vector2iVector(np.array(lines, dtype=np.int32))

    return line_set
