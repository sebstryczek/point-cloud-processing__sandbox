from time import time
from entities.Visualizer import Visualizer
from entities.PointCloud import PointCloud
from data_formats import line
from utils import files

def main():
    point_cloud_path = files.Path().go_to("./_hough-results").get_absolute_path("point_cloud.dat")
    point_cloud = PointCloud().load_file(point_cloud_path).get()

    lines_path = files.Path().go_to("./_hough-results").get_absolute_path("lines.dat")
    lines = line.load_lines_from_txt(lines_path)

    timestamp = int(time())

    Visualizer() \
        .add(point_cloud) \
        .add(lines) \
        .make_screenshots(output_directory=files.get_absolute_path(f"./_screenshots/hough/{timestamp}/"))
        # .run()
    
if __name__ == "__main__":
    main()
