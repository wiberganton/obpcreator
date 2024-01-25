
import numpy as np
import obplib as obp

def find_start_end_line_positions(arr):
    arr = np.array(arr)
    left_zeros_positions = np.where((np.roll(arr, shift=1, axis=1) == 0) & (arr == 1))
    left_positions = [(r, c) for r, c in zip(*left_zeros_positions)]
    first_elements = np.where(arr[:, 0] == 1)
    left_positions.extend([(r, 0) for r in first_elements[0]])
    right_zeros_positions = np.where((np.roll(arr, shift=-1, axis=1) == 0) & (arr == 1))
    right_positions = [(r, c) for r, c in zip(*right_zeros_positions)]
    last_elements = np.where(arr[:, -1] == 1)
    right_positions.extend([(r, arr.shape[1]-1) for r in last_elements[0]])
    left_positions = sorted(list(set(left_positions)))
    right_positions = sorted(list(set(right_positions)))
    return left_positions, right_positions

def snake_sort(t):
    if t[0] % 2 == 0:  # if the first value is even
        return (t[0], t[1])
    else:  # if the first value is odd
        return (t[0], -t[1])

def right_sort(t):
    return (t[0], -t[1])
    
def line_snake(part, layer):
    coord_matrix, keep_matrix = part.point_geometry.get_layer(layer)
    scan_settings = part.infill_setting.beam_settings
    left, right = find_start_end_line_positions(keep_matrix)
    snake_sorted_left = sorted(left, key=snake_sort)
    snake_sorted_right = sorted(right, key=snake_sort)
    obp_elements = []
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    for i in range(len(snake_sorted_left)):
        start_coord = coord_matrix[snake_sorted_left[i][0]][snake_sorted_left[i][1]]
        end_coord = coord_matrix[snake_sorted_right[i][0]][snake_sorted_right[i][1]]
        if start_coord==end_coord:
            a = obp.Point(start_coord.real*1000, start_coord.imag*1000)
            obp.Point(start_coord.real*1000, start_coord.imag*1000)
            obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
        else:
            a = obp.Point(start_coord.real*1000, start_coord.imag*1000)
            b = obp.Point(end_coord.real*1000, end_coord.imag*1000)
            obp_elements.append(obp.Line(a,b,scan_settings.scan_speed,bp))
    return obp_elements

def line_left_right(part, layer):
    coord_matrix, keep_matrix = part.point_geometry.get_layer(layer)
    scan_settings = part.infill_setting.beam_settings
    left, right = find_start_end_line_positions(keep_matrix)
    obp_elements = []
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    for i in range(len(left)):
        start_coord = coord_matrix[left[i][0]][left[i][1]]
        end_coord = coord_matrix[right[i][0]][right[i][1]]
        if start_coord==end_coord:
            obp.Point(start_coord.real*1000, start_coord.imag*1000)
            obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
        else:
            a = obp.Point(start_coord.real*1000, start_coord.imag*1000)
            b = obp.Point(end_coord.real*1000, end_coord.imag*1000)
            obp_elements.append(obp.Line(a,b,scan_settings.scan_speed,bp))
    return obp_elements

def line_right_left(part, layer):
    coord_matrix, keep_matrix = part.point_geometry.get_layer(layer)
    scan_settings = part.infill_setting.beam_settings
    left, right = find_start_end_line_positions(keep_matrix)
    snake_sorted_left = sorted(left, key=right_sort)
    snake_sorted_right = sorted(right, key=right_sort)
    obp_elements = []
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    for i in range(len(snake_sorted_left)):
        start_coord = coord_matrix[snake_sorted_left[i][0]][snake_sorted_left[i][1]]
        end_coord = coord_matrix[snake_sorted_right[i][0]][snake_sorted_right[i][1]]
        if start_coord==end_coord:
            a = obp.Point(start_coord.real*1000, start_coord.imag*1000)
            obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
        else:
            a = obp.Point(start_coord.real*1000, start_coord.imag*1000)
            b = obp.Point(end_coord.real*1000, end_coord.imag*1000)
            obp_elements.append(obp.Line(a,b,scan_settings.scan_speed,bp))
    return obp_elements

from obpcreator.visualisation.layer_vis import vis_keep_layer

def line_spiral_inward(part, layer):
    def flatten_nested_list(nested_list):
        """ Recursively flattens a nested list. """
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(flatten_nested_list(item))
            else:
                flat_list.append(item)
        return flat_list
    def perpendicular_distance(pt, line_start, line_end):
        """Calculate the perpendicular distance from a point to a line."""
        return np.abs(np.cross(line_end-line_start, line_start-pt)) / np.linalg.norm(line_end-line_start)
    def rdp(points, epsilon):
        """Ramer-Douglas-Peucker algorithm to reduce the number of points in a line."""
        dmax = 0.0
        index = 0
        for i in range(1, len(points) - 1):
            d = perpendicular_distance(points[i], points[0], points[-1])
            if d > dmax:
                index, dmax = i, d
        if dmax >= epsilon:
            # Recursive call
            rec_results1 = rdp(points[:index+1], epsilon)
            rec_results2 = rdp(points[index:], epsilon)
            # Combine results
            result = np.concatenate((rec_results1[:-1], rec_results2))
        else:
            result = np.array([points[0], points[-1]])
        return result
    
    scan_settings = part.infill_setting.beam_settings
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    all_spirals = []
    offset_distance = part.point_geometry.coord_matrix[1,0,0,0] - part.point_geometry.coord_matrix[0,0,0,0]
    contours = part.point_geometry.get_contours(layer)
    all_spirals.append(contours)
    point_geomtry = part.point_geometry.offset_contours_layer(-offset_distance, layer)
    part.point_geometry = point_geomtry
    while np.any(part.point_geometry.keep_matrix[:,:,layer] == 1):
        contours = part.point_geometry.get_contours(layer)
        all_spirals.append(contours)
        point_geomtry = part.point_geometry.offset_contours_layer(-offset_distance, layer)
        part.point_geometry = point_geomtry
    contour = flatten_nested_list(all_spirals)
    points = np.array([[z.real, z.imag] for z in contour])
    simplified_line = rdp(points, offset_distance*0.9)
    obp_elements = []
    for i in range(len(simplified_line)-1):
        a = obp.Point(simplified_line[i][0]*1000, simplified_line[i][1]*1000)
        b = obp.Point(simplified_line[i+1][0]*1000, simplified_line[i+1][1]*1000)
        obp_elements.append(obp.Line(a,b,scan_settings.scan_speed,bp))
    return obp_elements

def point_random(part, layer):
    coord_matrix, keep_matrix = part.point_geometry.get_layer(layer)
    scan_settings = part.infill_setting.beam_settings
    selected_values = coord_matrix[keep_matrix == 1]
    np.random.shuffle(selected_values)
    obp_elements = []
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    for point in selected_values:
        a = obp.Point(point.real*1000, point.imag*1000)
        obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
    return obp_elements

def point_ordered(part, layer):
    def n_stack(keep_array, coord_array, n_to_stack, stack_row):
        num_rows = keep_array.shape[0]
        extended_shape = (num_rows, keep_array.shape[1] + n_to_stack)
        extended_keep = np.zeros(extended_shape, dtype=keep_array.dtype)
        extended_coord = np.zeros(extended_shape, dtype=coord_array.dtype)
        indices = np.arange(num_rows)
        start_stack = np.floor_divide(indices, stack_row) % 2 == 1
        end_stack = ~start_stack
        extended_keep[end_stack, :keep_array.shape[1]] = keep_array[end_stack]
        extended_coord[end_stack, :coord_array.shape[1]] = coord_array[end_stack]
        extended_keep[start_stack, n_to_stack:] = keep_array[start_stack]
        extended_coord[start_stack, n_to_stack:] = coord_array[start_stack]
        return extended_keep, extended_coord
    
    coord_matrix, keep_matrix = part.point_geometry.get_layer(layer)
    scan_settings = part.infill_setting.beam_settings
    scan_strategy_settings = part.infill_setting.strategy_settings
    x_jump = scan_strategy_settings["x_jump"]
    y_jump = scan_strategy_settings["y_jump"]

    new_keep, new_coord = n_stack(keep_matrix, coord_matrix, int(x_jump/2), y_jump)

    len_x = new_keep.shape[1]
    len_y = new_keep.shape[0]

    new_new_keep = new_keep.reshape(-1)
    new_new_coord = new_coord.reshape(-1)
    Y, X = np.meshgrid(np.arange(len_y), np.arange(len_x), indexing='ij')
    ordered_Y = np.concatenate([Y[i::y_jump, j::x_jump].flatten() for i in range(y_jump) for j in range(x_jump)])
    ordered_X = np.concatenate([X[i::y_jump, j::x_jump].flatten() for i in range(y_jump) for j in range(x_jump)])
    order = ordered_Y * len_x + ordered_X
    coords_reordered = new_new_coord[order]
    keep_reordered = new_new_keep[order]
    keep_bool = keep_reordered.astype(bool)
    filtered_coords2 = coords_reordered[keep_bool]
    
    obp_elements = []
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    for point in filtered_coords2:
        a = obp.Point(point.real*1000, point.imag*1000)
        obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
    return obp_elements
