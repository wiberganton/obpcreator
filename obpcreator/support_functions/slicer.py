import pyvista as pv
import numpy as np
from shapely.geometry import Polygon
from matplotlib.path import Path
from obpcreator.support_functions.offset_paths import offset_array
from obpcreator.data_model import Infill, Contour, PartLayer, PointInfill
from obpcreator.support_functions.matrix_generation import create_matrices

def find_min_max_z(mesh): #Finds min and max point in the z-direction
      min_value = 0
      max_value = 0
      for point in mesh.points:
            z_value = point[2]
            if z_value < min_value:
               min_value = z_value
            elif z_value > max_value:
               max_value = z_value
      return min_value, max_value
        
def pv2mpl(pvPath): 
    #converts a path from pyvista polydata to a matplotlib path
    def _extract_lines_info(lines):
        offset = 0
        line_conn = []
        while offset < len(lines):
            line_length = lines[offset]
            line_conn.append(tuple(lines[offset + 1 : offset + 1 + line_length]))
            offset += line_length + 1
        return line_conn
    res = pvPath.strip()
    lines = _extract_lines_info(res.lines)
    points = pvPath.points
    paths = []
    for line in lines:
        vertices = [points[index][:2] for index in line]  # Extracting the x and y coordinates
        vertices.append((0, 0))  # Close the path
        codes = [Path.MOVETO] + [Path.LINETO] * (len(line) - 1) + [Path.CLOSEPOLY]
        path = Path(vertices, codes)
        paths.append(path)
    return paths

def combine_arrays(arrays):
    #create a new array with matplotlibs which adds different sliced stl files into different shapes

    numb_of_layers = 0 #Get the numb of layers based on the file with most layers
    for array in arrays:
        if len(array) > numb_of_layers:
            numb_of_layers = len(array)

    new_array = []
    for i in range(numb_of_layers):
        layer_array = []
        for array in arrays:
            if len(array)<=i:
                layer_array.append([])
            else:
                layer_array.append(array[i][0])
        new_array.append(layer_array)
    
    return new_array

def slice_stl_file(stl_string, layer_height):
    mesh = pv.read(stl_string)
    min_z, max_z = find_min_max_z(mesh)
    
    slices = []
    z_pos = min_z+layer_height/2
    while z_pos < max_z:
        single_slice = mesh.slice(normal=[0, 0, 1],origin=(0,0,z_pos))
        mpl_path = pv2mpl(single_slice)
        slices.append([mpl_path])
        z_pos = z_pos + layer_height
    return slices

def slice_stl(paths, layer_height):
    if not type(paths) is list:
        paths = [paths]
    slices = []
    for path in paths:
       slices.append(slice_stl_file(path,layer_height))
    combined_slices = combine_arrays(slices)
    return combined_slices

def slice_mesh(mesh, layer_height):
    min_z, max_z = find_min_max_z(mesh)
    slices = []
    z_pos = layer_height/2
    while z_pos < max_z:
        single_slice = mesh.slice(normal=[0, 0, 1],origin=(0,0,z_pos))
        mpl_path = pv2mpl(single_slice)
        slices.append([mpl_path])  
        z_pos = z_pos + layer_height
        if not not mpl_path:
            single_slice.plot()
    return slices

def slice_part(part, layer_height):
    slices = slice_mesh(part.mesh, layer_height)
    layers = []
    angle = part.scan_direction
    for slice in slices:
        local_slice = slice[0]
        contours = []
        for i in range(part.slicing_settings.contour_layers):
            offset_factor = part.slicing_settings.outer_offset 
            local_slice = offset_array(local_slice, -offset_factor)
            contours.append(Contour(paths=local_slice))
        offset_factor = part.slicing_settings.outer_offset + part.slicing_settings.contour_offset*(part.slicing_settings.contour_layers-1) + part.slicing_settings.contour_infill_offset
        infill = offset_array(local_slice, -offset_factor)
        coord_matrix, keep_matrix = create_matrices(infill, part.point_offset, angle)
        point_infill = PointInfill(coord_matrix=coord_matrix, keep_matrix=keep_matrix)
        layer_infill = Infill(paths=infill, scan_angle=angle, point_infill=point_infill)
        layers.append(PartLayer(infills=layer_infill, contours=contours))
        angle = angle + part.layer_rotation
    part.layers = layers
    return part






