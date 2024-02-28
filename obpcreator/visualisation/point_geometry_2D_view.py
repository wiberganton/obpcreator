import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

class PointGeometry2DView:
    def __init__(self, point_geometry):
        self.point_geometry = point_geometry
        self.plot_size = (point_geometry.coord_matrix[1, 0, 0, 0]-point_geometry.coord_matrix[0, 0, 0, 0])*1
        self.min_x = point_geometry.coord_matrix[0, 0, 0, 0]
        self.max_x = point_geometry.coord_matrix[-1, 0, 0, 0]
        self.min_y = point_geometry.coord_matrix[0, -1, 0, 1]
        self.max_y = point_geometry.coord_matrix[0, 0, 0, 1]
        self.nmb_of_layers = point_geometry.keep_matrix.shape[2]-1

        self.fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.25)

        self.coords = self.generate_data(0)
        self.scatter = self.ax.scatter(self.coords[:, 0], self.coords[:, 1], s=self.plot_size)
        self.ax.set_xlim(self.min_x, self.max_x)
        self.ax.set_ylim(self.min_y, self.max_y)
        self.slider_ax = plt.axes([0.2, 0.1, 0.65, 0.03])
        self.slider = Slider(
            self.slider_ax, 'Layer', 
            valmin=0, valmax=self.nmb_of_layers, 
            valinit=0, valstep=1
        )
        self.slider.on_changed(self.update_plot)

    def generate_data(self, layer):
        keep = self.point_geometry.keep_matrix[:,:,layer]
        x_coords = self.point_geometry.coord_matrix[:, :, layer, 0]
        y_coords = self.point_geometry.coord_matrix[:, :, layer, 1]
        selected_x_coords = x_coords[keep == 1]
        selected_y_coords= y_coords[keep == 1]
        x_array = np.array(selected_x_coords)
        y_array = np.array(selected_y_coords)
        return np.column_stack((x_array, y_array)) 

    def update_plot(self, val):
        self.ax.cla()
        self.current_points = int(self.slider.val)
        self.coords = self.generate_data(self.current_points)
        self.ax.scatter(self.coords[:, 0], self.coords[:, 1], s=self.plot_size)
        self.fig.canvas.draw_idle()
        self.ax.set_xlim(self.min_x, self.max_x)
        self.ax.set_ylim(self.min_y, self.max_y)

    def show(self):
        plt.show()