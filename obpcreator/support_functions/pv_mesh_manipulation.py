import pyvista as pv
import numpy as np

def center_mesh(mesh):
    centroid = mesh.center_of_mass()
    translation = -centroid
    points = mesh.points
    min_z = np.min(points[:, 2])
    translation[2] = -min_z
    mesh_centered = mesh.translate(translation, inplace=False)
    return mesh_centered

def place_on_pos(mesh, position):
    #postion is (posx, posy, posz)
    centered_mesh = center_mesh(mesh)
    placed_mesh = centered_mesh.translate(position, inplace=False)
    return placed_mesh
