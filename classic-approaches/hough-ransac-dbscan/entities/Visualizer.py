import os
import math
import open3d as o3d

ROTATION_RADIAN_PER_PIXEL = 0.003
AMOUNT_OF_SCREENSHOTS_PER_ITEM = 10
ANGLE_X_DELTA = math.radians(360 / AMOUNT_OF_SCREENSHOTS_PER_ITEM) / ROTATION_RADIAN_PER_PIXEL

class Visualizer:
    geometries = []

    def __init__(self):
        pass

    '''
    '''
    def add(self, geometry):
        self.geometries.append(geometry)
        return self
    
    '''
    '''
    def create_viewer(self):
        viewer = o3d.visualization.Visualizer()
        viewer.create_window()

        render_option = viewer.get_render_option()
        render_option.mesh_show_back_face = True
        render_option.mesh_show_wireframe = True
        render_option.show_coordinate_frame = True

        for geometry in self.geometries:
            viewer.add_geometry(geometry)

        return viewer
    
    '''
    '''
    def run(self):
        viewer = self.create_viewer()
        viewer.run()
        viewer.destroy_window()

    '''
    '''
    def make_screenshots(self, output_directory: str):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        viewer = self.create_viewer()
        view_control = viewer.get_view_control()

        for i in range(AMOUNT_OF_SCREENSHOTS_PER_ITEM):
            viewer.update_renderer()
            viewer.poll_events()
            viewer.capture_screen_image(os.path.join(output_directory, f"image_{i}.png"))
            view_control.rotate(ANGLE_X_DELTA, 0)

        viewer.destroy_window()

        return self
