import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def vis_part_layer(part_layer):
    keep_matrix = part_layer.infills.point_infill.keep_matrix
    keep_matrix[:] = 1
    coord_matrix = part_layer.infills.point_infill.coord_matrix
    infill_paths = part_layer.infills.paths
    contour_paths=[]
    for contour in part_layer.contours:
        contour_paths.extend(contour.paths)
    vis_keep_matrix(keep_matrix, coord_matrix, infill_paths=infill_paths, contour_paths=contour_paths)

def vis_keep_matrix(keep_matrix, coord_matrix, infill_paths=[], contour_paths=[]):
    # Extract real and imaginary parts
    x_coords = np.real(coord_matrix)
    y_coords = np.imag(coord_matrix)

    # Masking
    x_black = x_coords[keep_matrix == 1]
    y_black = y_coords[keep_matrix == 1]
    x_white = x_coords[keep_matrix == 0]
    y_white = y_coords[keep_matrix == 0]

    # Plott points to keep
    fig, ax = plt.subplots()
    ax.scatter(x_black, y_black, color='black', s=10)  # s is size of marker, adjust as necessary
    ax.scatter(x_white, y_white, color='white', s=10)
    
    # Plot wanted infill paths
    for path in infill_paths:
        path_patch = patches.PathPatch(path, facecolor='none', edgecolor='red') # you can modify color attributes as needed
        ax.add_patch(path_patch)

     # Plot wanted contour paths
    for path in contour_paths:
        path_patch = patches.PathPatch(path, facecolor='none', edgecolor='blue') # you can modify color attributes as needed
        ax.add_patch(path_patch)

    ax.set_aspect('equal', 'box')
    ax.set_facecolor((1, 1, 1))  # set background to white
    plt.show()