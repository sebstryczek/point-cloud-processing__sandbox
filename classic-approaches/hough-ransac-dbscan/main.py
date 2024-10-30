from entities.Visualizer import Visualizer
from entities.PointCloud import PointCloud
from utils import files

def main():
    point_cloud_path = files.Path().go_to("../_datasets/Others/").get_absolute_path("depth_2_pcd_downsampled.ply")
    point_cloud = PointCloud().load_file(point_cloud_path).center().get()
    
    Visualizer().add(point_cloud).run()
    
if __name__ == "__main__":
    main()