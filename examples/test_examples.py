import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

path1 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw1.stl"
mesh1 = pv.read(path1)
path2 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw2.stl"
mesh2 = pv.read(path2)

scan_parameters_contour = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
scan_parameters_infill = ScanParameters(spot_size=1, beam_power=540, scan_speed=1800000, dwell_time=83333)
contour_settings = ScanSettings(scan_parameters=scan_parameters_contour, scan_strategy = "line_simple", strategy_settings={})
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part1 = Part(
    mesh = mesh1,
    infill_setting = infill_settings,
    contour_setting = contour_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 90,
    slicing_settings = slice_settings)
part1 = slice_part(part1)

scan_parameters_contour = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
scan_parameters_infill = ScanParameters(spot_size=1, beam_power=540, scan_speed=1800000, dwell_time=83333)
contour_settings = ScanSettings(scan_parameters=scan_parameters_contour, scan_strategy = "line_simple", strategy_settings={})
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part2 = Part(
    mesh = mesh2,
    infill_setting = infill_settings,
    contour_setting = contour_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 90,
    slicing_settings = slice_settings)
part2 = slice_part(part2)


build = Build(parts=[part1,part2],layer_height=0.1)

#vis_part_layer(part1.layers[0])
#generate_build_patterns(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\screw_2023_10_12")
#generate_build_file(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\screw_2023_10_12\run_file.yml")
