import open3d as o3d
import numpy as np
from data_formats import off, txt

class PointCloud:
    point_cloud: o3d.geometry.PointCloud = None

    def __init__(self):
        pass

    def load_file(self, file_path: str):
        if self.point_cloud is not None:
            print("Error: Point cloud already loaded.")
            return self
        
        if file_path.endswith(".off"):
            points = off.read(file_path)
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(points)
        elif file_path.endswith(".dat"):
            points = txt.read(file_path)
            point_cloud = o3d.geometry.PointCloud()
            point_cloud.points = o3d.utility.Vector3dVector(np.array(points))
        else:
            point_cloud = o3d.io.read_point_cloud(file_path)

        if not point_cloud.has_points():
            print("Error: File does not contain valid point cloud data.")
        
        if not point_cloud.has_colors():
            print("Warning: Point cloud does not contain color information.")
    
        self.point_cloud = point_cloud
        return self
    
    def load_raw(self, points: np.ndarray, colors: np.ndarray):
        if self.point_cloud is not None:
            print("Error: Point cloud already loaded.")
            return self
        
        point_cloud = o3d.geometry.PointCloud()
        point_cloud.points = o3d.utility.Vector3dVector(points)
        point_cloud.colors = o3d.utility.Vector3dVector(colors)
        self.point_cloud = point_cloud
        return self
    
    def center(self):
        center = self.point_cloud.get_center()
        self.point_cloud.translate(-center)
        return self

    def get(self):
        return self.point_cloud
    
    def get_raw(self):
        return np.asarray(self.point_cloud.points).copy()

