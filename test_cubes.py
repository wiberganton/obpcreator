import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters, BackScatter
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

mesh1 = pv.Cube(center=(-15.0, 15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh2 = pv.Cube(center=(-5.0, 15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh3 = pv.Cube(center=(5.0, 15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh4 = pv.Cube(center=(15.0, 15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh5 = pv.Cube(center=(-15.0, 5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh6 = pv.Cube(center=(-5.0, 5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh7 = pv.Cube(center=(5.0, 5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh8 = pv.Cube(center=(15.0, 5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh9 = pv.Cube(center=(-15.0, -5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh10 = pv.Cube(center=(-5.0, -5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh11 = pv.Cube(center=(5.0, -5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh12 = pv.Cube(center=(15.0, -5.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh13 = pv.Cube(center=(-15.0, -15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh14 = pv.Cube(center=(-5.0, -15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh15 = pv.Cube(center=(5.0, -15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh16 = pv.Cube(center=(15.0, -15.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)

scan_parameters_infill = ScanParameters(spot_size=1, beam_power=480, scan_speed=1164000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part1 = Part(
    mesh = mesh1,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part1 = slice_part(part1)

part3 = Part(
    mesh = mesh3,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part3 = slice_part(part3)

scan_parameters_infill = ScanParameters(spot_size=10, beam_power=480, scan_speed=1164000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part2 = Part(
    mesh = mesh2,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part2 = slice_part(part2)

part4 = Part(
    mesh = mesh4,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part4 = slice_part(part4)

scan_parameters_infill = ScanParameters(spot_size=1, beam_power=660, scan_speed=1600000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part5 = Part(
    mesh = mesh5,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part5 = slice_part(part5)

part7 = Part(
    mesh = mesh7,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part7 = slice_part(part7)

scan_parameters_infill = ScanParameters(spot_size=10, beam_power=660, scan_speed=1600000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part6 = Part(
    mesh = mesh6,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part6 = slice_part(part6)

part8 = Part(
    mesh = mesh8,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.1,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part8 = slice_part(part8)

scan_parameters_infill = ScanParameters(spot_size=1, beam_power=840, scan_speed=1566000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part9 = Part(
    mesh = mesh9,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part9 = slice_part(part9)

part11 = Part(
    mesh = mesh11,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part11 = slice_part(part11)

scan_parameters_infill = ScanParameters(spot_size=10, beam_power=840, scan_speed=1566000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part10 = Part(
    mesh = mesh10,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part10 = slice_part(part10)

part12 = Part(
    mesh = mesh12,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part12 = slice_part(part12)

scan_parameters_infill = ScanParameters(spot_size=1, beam_power=1020, scan_speed=1902000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part13 = Part(
    mesh = mesh13,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part13 = slice_part(part13)

part15 = Part(
    mesh = mesh15,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part15 = slice_part(part15)

scan_parameters_infill = ScanParameters(spot_size=10, beam_power=1020, scan_speed=1902000, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "line_snake", strategy_settings={})
slice_settings = SlicingSettings(layer_height=0.07, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
part14 = Part(
    mesh = mesh14,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part14 = slice_part(part14)

part16 = Part(
    mesh = mesh16,
    infill_setting = infill_settings,
    contour_order = 0,
    point_offset = 0.13,
    scan_direction = 0,
    layer_rotation = 67,
    slicing_settings = slice_settings)
part16 = slice_part(part16)

back_scatter = BackScatter(file="path_to_replace/back_scatter.obp", start_layer=0, step=2)
build = Build(parts=[part16, 
                     part15, 
                     part14, 
                     part13, 
                     part12, 
                     part11, 
                     part10, 
                     part9, 
                     part8, 
                     part7, 
                     part6, 
                     part5,
                     part4,
                     part3,
                     part2,
                     part1],layer_height=0.07, back_scatter=back_scatter)

#vis_part_layer(part1.layers[0])
generate_build_patterns(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test3")
generate_build_file(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test3\run_file.yml")
