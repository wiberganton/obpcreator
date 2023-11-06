import matplotlib.path as mpath
from shapely.geometry import Polygon

def offset_mpl_path(mpl_path, offset_factor):
    # mpl_path is a maptplotlib.path
    # offset_factor is the factor you want to offset (in same units as path)
    # returns array with offseted paths
    polygon = Polygon(mpl_path.vertices)
    offset_polygon = polygon.buffer(offset_factor)
    offset_mpl_path = mpath.Path(offset_polygon.exterior.coords)
    return offset_mpl_path

def offset_array(mpl_paths, offset_factor):
    # mpl_paths is an array with maptplotlib.path
    # offset_factor is the factor you want to offset (in same units as path). If one path is inside another it will offset that in opposite direction to offset factor
    
    # Convert to shapely Polygons
    shapely_paths = []
    for path in mpl_paths:
        shapely_path = Polygon(path.vertices)
        shapely_paths.append(shapely_path)
    # Check nesting
    nesting_array = [0] * len(mpl_paths)
    for i in range(len(shapely_paths)):
        for ii in range(len(shapely_paths)):
            if i != ii:
                is_contained = shapely_paths[ii].contains(shapely_paths[i])
                if is_contained:
                    nesting_array[i] = nesting_array[i] + 1
    # Offset paths
    offset_paths = []
    for i in range(len(shapely_paths)):
        if (nesting_array[i] % 2) == 0:
            offset_polygon = shapely_paths[i].buffer(offset_factor)
        else:
            offset_polygon = shapely_paths[i].buffer(-offset_factor)
        offset_mpl_path = mpath.Path(offset_polygon.exterior.coords) # Convert to mpl path
        offset_paths.append(offset_mpl_path)
    return offset_paths

def get_min_max_in_paths(paths):
    min_x_array = []
    max_x_array = []
    min_y_array = []
    max_y_array = []
    for path in paths:
        x_coords, y_coords = zip(*path.vertices)
        min_x_array.append(min(x_coords))
        max_x_array.append(max(x_coords))
        min_y_array.append(min(y_coords))
        max_y_array.append(max(y_coords))
    return min(min_x_array), max(max_x_array), min(min_y_array), max(max_y_array)


    