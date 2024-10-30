from time import time
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from utils import files
from entities.PointCloud import PointCloud
from entities.Visualizer import Visualizer


def main():
    point_cloud_path = files.Path() \
        .go_to("../_datasets/Others/") \
        .log_tree(skip=True) \
        .log_contents(skip=True) \
        .log_absolute_path("depth_2_pcd_downsampled.ply", skip=True) \
        .get_absolute_path("depth_2_pcd_downsampled.ply")

    input_point_cloud = PointCloud().load_file(point_cloud_path).center()

    # Ransac
    points = input_point_cloud.get_raw()
    
    scaled_points = StandardScaler().fit_transform(points)
    model = DBSCAN(eps=0.15, min_samples=10)
    model.fit(scaled_points)
    labels = model.labels_
    number_of_clusters = len(set(labels))

    colors_rgba = plt.get_cmap("tab20")(labels / (number_of_clusters if number_of_clusters > 0 else 1))
    colors_rgba[labels < 0] = 0
    colors_rgb = colors_rgba[:, :3]

    clustered_point_cloud = PointCloud().load_raw(points=scaled_points, colors=colors_rgb)
    # ###

    timestamp = int(time())

    Visualizer() \
        .add(clustered_point_cloud.get()) \
        .make_screenshots(output_directory=files.get_absolute_path(f"./_screenshots/dbscan/{timestamp}/"))
        # .run()

if __name__ == "__main__":
    main()
