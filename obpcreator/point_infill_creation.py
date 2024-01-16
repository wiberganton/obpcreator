import math 
import numpy as np
import pyvista as pv

from obpcreator.data_model import PointGeometry

def visualise_point_geometry_pyvista(point_geometry, show_plot=True):
    # Flatten the arrays
    reshaped_coords = point_geometry.coord_matrix.reshape(-1, 3)
    reshaped_keep = point_geometry.keep_matrix.flatten()
    # Separate the coordinates based on keep_matrix values
    coords_to_keep = reshaped_coords[reshaped_keep == 1]
    coords_to_tune_down = reshaped_coords[reshaped_keep == 0]
    # Create a PyVista plotter
    plotter = pv.Plotter()
    if coords_to_keep.size > 0:
        plotter.add_points(coords_to_keep, color='blue', point_size=5, label='Kept Points')
    #if coords_to_tune_down.size > 0:
    #    plotter.add_points(coords_to_tune_down, color='red', point_size=5, opacity=0.3, label='Tuned Down Points')
    plotter.add_axes(xlabel='X Axis', ylabel='Y Axis', zlabel='Z Axis')
    if show_plot:
        plotter.show()
    else:
        return plotter
    
# Function to rotate a point in the xy-plane
def rotate_point(x, y, theta, center_x, center_y):
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    x_new = cos_theta * (x - center_x) - sin_theta * (y - center_y) + center_x
    y_new = sin_theta * (x - center_x) + cos_theta * (y - center_y) + center_y
    return x_new, y_new

def generate_matrices(min_x, max_x, min_y, max_y, max_z, xy_spacing, z_spacing, start_angle=0, rotation_angle=0, uniform_point_dist=True, offset_margin=3):
    center = [(max_x+min_x)/2, (max_y+min_y)/2]
    longest_side = max(abs(max_x-min_x),abs(max_y-min_y))/2+2*offset_margin
    min_x = center[0]-math.sqrt(2)*longest_side
    max_x = center[0]+math.sqrt(2)*longest_side
    min_y = center[1]-math.sqrt(2)*longest_side
    max_y = center[1]+math.sqrt(2)*longest_side
    spacing_x = xy_spacing
    spacing_y = math.sqrt(3/4)*xy_spacing
    points_x = math.ceil((max_x-min_x)/spacing_x)
    points_y = math.ceil((max_y-min_y)/spacing_y)
    max_x = min_x + points_x*spacing_x
    max_y = min_y + points_y*spacing_y
    max_z = max_z - z_spacing/2
    # Generate arrays of x and y coordinates based on given parameters
    x_coords = np.arange(min_x, max_x, spacing_x)
    y_coords = np.arange(min_y, max_y, spacing_y)
    z_coords = np.arange(z_spacing/2, max_z, z_spacing)
    # Using np.meshgrid to create 3D grids for X, Y, and Z
    X_grid, Y_grid, Z_grid = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')
    # Combining the grids to form a 4D array with coordinates in the last dimension
    combined_coords = np.stack([X_grid, Y_grid, Z_grid], axis=-1)
    if uniform_point_dist:
        combined_coords[:, 1::2, :, 0] += spacing_x/2

    # Rotate points in myArray
    for i in range(combined_coords.shape[2]):  # Loop over the third dimension
        theta = np.radians(start_angle + rotation_angle * i)  # Convert angle to radians
        x, y = combined_coords[:, :, i, 0], combined_coords[:, :, i, 1]  # Extract x, y coordinates
        x_rot, y_rot = rotate_point(x, y, theta, center[0], center[1])  # Apply rotation
        combined_coords[:, :, i, 0], combined_coords[:, :, i, 1] = x_rot, y_rot  # Update array

    keep_matrix = np.zeros(combined_coords.shape[:-1])

    return combined_coords, keep_matrix
    

def create_from_pyvista_mesh(mesh, xy_spacing, z_spacing, start_angle=0, rotation_angle=0, uniform_point_dist=True, offset_margin=3):
    points = mesh.points
    # Find min and max for each coordinate
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    z_min, z_max = np.min(points[:, 2]), np.max(points[:, 2])
    combined_coords, keep_matrix = generate_matrices(x_min, x_max, y_min, y_max, z_max, xy_spacing, z_spacing, start_angle=start_angle, rotation_angle=rotation_angle, uniform_point_dist=uniform_point_dist, offset_margin=offset_margin)
    # Check keep matrix
    reshaped_coords = combined_coords.reshape(-1, 3)
    point_cloud = pv.PolyData(reshaped_coords)
    inside_points = point_cloud.select_enclosed_points(mesh, tolerance=0.0, check_surface=True)
    keep_list = inside_points['SelectedPoints']
    keep_matrix = keep_list.reshape(combined_coords.shape[:-1])
    
    return PointGeometry(coord_matrix=combined_coords, keep_matrix=keep_matrix)
