
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











