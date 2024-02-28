import pyvista as pv

def point_vis(point_geometry, size = 5):
    #plotter = pv.Plotter()
    coord_matrix = point_geometry.coord_matrix
    #3D numpy matrix with the coords of the points as complex numbers in mm
    keep_matrix = point_geometry.keep_matrix 
    #3D numpy matrix with which points to manufacture

    flattened_coord = coord_matrix.reshape(-1, coord_matrix.shape[-1])
    flattened_keep = keep_matrix.flatten()
    filtered_coords_1 = flattened_coord[flattened_keep == 1]
    filtered_coords_0 = flattened_coord[flattened_keep == 0]
    
    cloud_1 = pv.PolyData(filtered_coords_1)
    cloud_0 = pv.PolyData(filtered_coords_0)
    print(cloud_1)
    # Add points to the mesh
    # This step is actually redundant if you're directly creating PolyData from numpy array
    # cloud.points = data

    # Plot the points
    plotter = pv.Plotter()
    plotter.add_mesh(cloud_1, point_size=size, render_points_as_spheres=False, color='blue')
    plotter.add_mesh(cloud_0, point_size=size, render_points_as_spheres=False, color='red', opacity=0.1)
    plotter.show()
