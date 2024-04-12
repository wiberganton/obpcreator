from typing import Any, List, Dict, Optional
from pydantic import BaseModel
from numpy import copy
from scipy.ndimage import binary_dilation, binary_erosion
import cv2
import math
from shapely.geometry import Polygon
import numpy as np
import matplotlib.pyplot as plt

class PointGeometry(BaseModel):
    keep_matrix: Any #3D numpy matrix with which points to keep
    center: List[int] = [0 , 0] #The coordinate of centrum in a 2D layer 
    point_distance: float = 0.1 #Distance between the keep points
    start_angle: float = 0 #Rotation of the first layer
    rotation_angle: float = 0 #Rotation between each layer
    uniform_point_dist: bool = True #If True it will create a triangular grid between the keep points, otherwise a quadratic
    
    def get_point_distance(self):
        return self.point_distance
    
    def get_layer(self, layer):
        spacing_x = self.point_distance
        if self.uniform_point_dist:
            spacing_y = math.sqrt(3/4)*spacing_x
        else: 
            spacing_y = spacing_x

        (points_x, points_y) = self.keep_matrix[:,:,layer].shape
        min_x = self.center[0]-spacing_x*math.ceil(points_x/2)
        max_x = self.center[0]+spacing_x*math.floor(points_x/2)
        min_y = self.center[1]-spacing_y*math.ceil(points_y/2)
        max_y = self.center[1]+spacing_y*math.floor(points_y/2)
        
        # Generate arrays of x and y coordinates based on given parameters
        x_coords = np.arange(min_x, max_x, spacing_x)
        y_coords = np.arange(min_y, max_y, spacing_y)
        # Using np.meshgrid to create 3D grids for X and Y
        X_grid, Y_grid = np.meshgrid(x_coords, y_coords, indexing='ij')
        # Combining the grids to form a 3D array with coordinates in the last dimension
        combined_coords = np.stack([X_grid, Y_grid], axis=-1)
        if self.uniform_point_dist and layer % 2 == 0:
            combined_coords[:, 1::2, 0] += spacing_x/2
            print("odd")
        elif self.uniform_point_dist and not layer % 2 == 0:
            combined_coords[:, 0::2, 0] += spacing_x/2
            print("even")

        # Rotate points in myArray
        theta = np.radians(self.start_angle + self.rotation_angle * layer)  # Convert angle to radians
        x, y = combined_coords[:, :, 0], combined_coords[:, :, 1]  # Extract x, y coordinates
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        x_new = cos_theta * (x - self.center[0]) - sin_theta * (y - self.center[1]) + self.center[0]
        y_new = sin_theta * (x - self.center[0]) + cos_theta * (y - self.center[1]) + self.center[1]
        combined_coords[:, :, 0], combined_coords[:, :, 1] = x_new, y_new  # Update array

        return combined_coords, self.keep_matrix[:,:,layer] 
    
    def get_contours(self, layer):
        matrix, coords = self.get_layer(layer)
        contours, _ = cv2.findContours(matrix, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        simplified_contours = []
        epsilon_factor = (self.coord_matrix[1,0,0,0] - self.coord_matrix[0,0,0,0])*1.0 #Simplification factor
        for cnt in contours:
            epsilon = epsilon_factor * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # Initialize an empty list to hold the mapped real-world coordinates for this contour
            real_world_contour_points = []
            for point in approx.reshape(-1, 2):
                # Map the pixel positions to real-world coordinates
                # Ensure to convert point indices to integers, as they will be used as indices
                x_pixel, y_pixel = point.astype(int)
                real_world_x, real_world_y = coords[y_pixel, x_pixel, 0], coords[y_pixel, x_pixel, 1]
                real_world_contour_points.append((real_world_x, real_world_y))
            
            # Create a Shapely Polygon with the real-world coordinates
            polygon = Polygon(real_world_contour_points)
            simplified_contours.append(polygon)
        return simplified_contours
    
    def offset_contours_layer(self, offset_distance, layer):
        point_distance = self.point_distance
        offset_steps = round(offset_distance/point_distance)
        keep_matrix = copy(self.keep_matrix)
        matrix = keep_matrix[:,:,layer]
        if offset_steps > 0:
            for _ in range(offset_steps):
                matrix = binary_dilation(matrix)
        else:
            for _ in range(abs(offset_steps)):
                matrix = binary_erosion(matrix)
        keep_matrix[:,:,layer] = matrix.astype(bool)
        return PointGeometry(coord_matrix=self.coord_matrix, keep_matrix=keep_matrix)

def vis_layer(point_geometry, layer):
    c, k = point_geometry.get_layer(layer)
    flattened_c = c.reshape(-1, 2)
    flattened_k = k.reshape(-1)
    filtered_data = flattened_c[flattened_k]
    x_coords_filtered = filtered_data[:, 0]
    y_coords_filtered = filtered_data[:, 1]

    # Plotting
    plt.figure(figsize=(10, 8))  # Set the figure size
    plt.scatter(x_coords_filtered, y_coords_filtered, c='red', marker='o')  # Create a scatter plot
    plt.title("Filtered 2D Coordinates Plot")
    plt.xlabel("X coordinate")
    plt.ylabel("Y coordinate")
    plt.grid(True)  # Enable grid for better visualization
    plt.show()
