from time import time
from entities.Visualizer import Visualizer
from entities.PointCloud import PointCloud
from utils import files, geometry

def main():
    point_cloud_path = files.Path() \
        .go_to("../_datasets/Others/") \
        .log_tree(skip=True) \
        .log_contents(skip=True) \
        .log_absolute_path("depth_2_pcd_downsampled.ply", skip=True) \
        .get_absolute_path("depth_2_pcd_downsampled.ply")

    input_point_cloud = PointCloud().load_file(point_cloud_path).center()

    # Ransac
    point_cloud = input_point_cloud.get()
    plane_model, inliers = point_cloud.segment_plane(
        distance_threshold=0.01,
        ransac_n=4,
        num_iterations=1000
    )

    inlier_cloud = point_cloud.select_by_index(inliers)
    inlier_cloud.paint_uniform_color([1.0, 0, 0])

    outlier_cloud = point_cloud.select_by_index(inliers, invert=True)
    outlier_cloud.paint_uniform_color([0, 1.0, 0])

    plane_mesh = geometry.create_plane_mesh(plane_model, size=10)
    # ###

    timestamp = int(time())

    Visualizer() \
        .add(inlier_cloud) \
        .add(outlier_cloud) \
        .add(plane_mesh) \
        .make_screenshots(output_directory=files.get_absolute_path(f"./_screenshots/ransac/{timestamp}/"))
        # .run()

if __name__ == "__main__":
    main()
