import math
import numpy as np

import numpy as np

def rotate_matrix_around_point(matrix, angle, rotate_point=(0,0)):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in degree.
    rotate_point is the point around which the rotation should be performed.
    """
    # convert the angle to radians
    angle_rad = np.radians(angle)
    
    # translate the matrix to move the rotation point to the origin
    translated_matrix = matrix - (rotate_point[0] + 1j * rotate_point[1])
    
    # separate the translated matrix into x and y coordinates
    x = translated_matrix.real
    y = translated_matrix.imag
    
    # apply the rotation
    x_new = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_new = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    
    # combine the new x and y coordinates back into complex numbers
    arr_rotated = x_new + 1j * y_new
    
    # translate the rotated matrix back
    arr_rotated += rotate_point[0] + 1j * rotate_point[1]
    
    return arr_rotated


def rotate_matrix(matrix, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in degree.
    """
    # convert the angle to radians
    angle_rad = np.radians(angle)
    # separate the array into x and y coordinates
    x = matrix.real
    y = matrix.imag
    # apply the rotation
    x_new = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_new = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    # combine the new x and y coordinates back into complex numbers
    arr_rotated = x_new + 1j * y_new
    return arr_rotated

def generate_coord_matrix(min_x, max_x, min_y, max_y, spacing, angle=0):
    center = [(max_x+min_x)/2, (max_y+min_y)/2]
    if angle != 0:
        longest_side = max(abs(max_x-min_x),abs(max_y-min_y))/2
        min_x = center[0]-math.sqrt(2)*longest_side
        max_x = center[0]+math.sqrt(2)*longest_side
        min_y = center[1]-math.sqrt(2)*longest_side
        max_y = center[1]+math.sqrt(2)*longest_side
    spacing_x = spacing
    spacing_y = math.sqrt(3/4)*spacing
    points_x = math.ceil((max_x-min_x)/spacing_x)
    points_y = math.ceil((max_y-min_y)/spacing_y)
    max_x = min_x + points_x*spacing_x
    max_y = min_y + points_y*spacing_y
    # Generate arrays of x and y coordinates based on given parameters
    x_coords = np.arange(min_x, max_x, spacing_x)
    y_coords = np.arange(min_y, max_y, spacing_y)
    # Create 2D coordinate matrices for x and y
    X, Y = np.meshgrid(x_coords, y_coords)
    # Combine X and Y to generate the complex matrix
    coord_matrix = X + 1j * Y
    coord_matrix[1::2] += spacing_x/2
    if angle != 0:
        # If angle != 0, apply rotation to all points at once
        coord_matrix = rotate_matrix_around_point(coord_matrix, angle, rotate_point=center)
    return coord_matrix


def get_path_bounds(paths):
    all_vertices = np.vstack([path.vertices for path in paths])
    min_coords = all_vertices.min(axis=0)
    max_coords = all_vertices.max(axis=0)
    return tuple(min_coords), tuple(max_coords)

def check_points_in_path(coord_matrix, paths):
    flatten_coord = coord_matrix.flatten()
    flatten_2D = np.column_stack((flatten_coord.real,flatten_coord.imag))
    inside_all = np.full((len(flatten_2D),), False)
    if type(paths) is list:
        for path in paths:
            inside = path.contains_points(flatten_2D)
            inside_all = np.logical_xor(inside_all, inside)
    else:
        inside = paths.contains_points(flatten_2D)
        inside_all = np.logical_xor(inside_all, inside)
    keep_matrix = inside_all.reshape(coord_matrix.shape)
    return keep_matrix

def create_matrices(paths, spacing, angle):
    (min_x, min_y), (max_x, max_y) = get_path_bounds(paths)
    coord_matrix = generate_coord_matrix(min_x, max_x, min_y, max_y, spacing, angle=angle)
    keep_matrix = check_points_in_path(coord_matrix, paths)
    return coord_matrix, keep_matrix




