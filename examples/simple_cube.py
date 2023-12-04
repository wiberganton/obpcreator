import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters, BackScatter
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

mesh1 = pv.Cube(center=(0, 0, 0), x_length=10.0, y_length=10.0, z_length=5)


scan_parameters_infill = ScanParameters(spot_size=1, beam_power=720, scan_speed=140000, dwell_time=50000)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "point_random", strategy_settings={})
scan_parameters_contour = ScanParameters(spot_size=1, beam_power=400, scan_speed=140000, dwell_time=50000)
contour_settings = ScanSettings(scan_parameters=scan_parameters_contour, scan_strategy = "line_simple", strategy_settings={})
slicing_settings = SlicingSettings(outer_offset = 0, contour_layers=1, contour_offset=1, contour_infill_offset=1)
part1 = Part(
    slicing_settings=slicing_settings,
    mesh = mesh1,
    infill_setting = infill_settings,
    contour_setting = contour_settings,
    contour_order = 1,
    point_offset = 1,
    scan_direction = 0,
    layer_rotation = 67)


build = Build(parts=[part1],layer_height=1.0)

#vis_part_layer(part1.layers[0])
path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test4"
generate_build_patterns(build, path)
generate_build_file(build, path + r"\run_file.yml")
