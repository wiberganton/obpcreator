import pyvista as pv
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
        

def find_in_list_of_tuples(to_find,tuples_list):
    for i in range(len(tuples_list)):
        if tuples_list[i][0] == to_find:
            return i
    return None


def sort_dominoes(dominoes):
    all_paths = []

    sorted_list = [dominoes[0][0],dominoes[0][1]]
    dominoes.pop(0)

    while len(dominoes) > 0:
        result = find_in_list_of_tuples(sorted_list[-1],dominoes)
        if result == None:
            all_paths.append(sorted_list)
            sorted_list = [dominoes[0][0],dominoes[0][1]]
            dominoes.pop(0)
        else:
            sorted_list.append(dominoes[result][1])
            dominoes.pop(result)
    all_paths.append(sorted_list)
    return all_paths


def py_to_mpl_path(pv_path):
    pv_lines = []
    for i in range(1,len(pv_path.lines),3):
        pv_lines.append((pv_path.lines[i],pv_path.lines[i+1]))
    line_points = sort_dominoes(pv_lines)
    
    all_points = pv_path.points

    mpl_paths = []
    for path_points in line_points:
        codes = [Path.MOVETO]
        path_lines = []
        for point in path_points:
            path_lines.append((all_points[point][0],all_points[point][1]))
            codes.append(Path.LINETO)
        codes.pop(1)
        codes[-1] = (Path.CLOSEPOLY)
        mpl_paths.append(Path(path_lines, codes))

    return mpl_paths

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
        mpl_path = py_to_mpl_path(single_slice)
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
    z_pos = min_z+layer_height/2
    while z_pos < max_z:
        single_slice = mesh.slice(normal=[0, 0, 1],origin=(0,0,z_pos))
        mpl_path = py_to_mpl_path(single_slice)
        slices.append([mpl_path])
        z_pos = z_pos + layer_height
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






