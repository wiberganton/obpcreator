import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters, BackScatter
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

mesh1 = pv.Cube(center=(-20.0, 20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh2 = pv.Cube(center=(-7.5, 20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh3 = pv.Cube(center=(7.5, 20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh4 = pv.Cube(center=(20.0, 20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh5 = pv.Cube(center=(-20.0, 7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh6 = pv.Cube(center=(-7.5, 7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh7 = pv.Cube(center=(7.5, 7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh8 = pv.Cube(center=(20.0, 7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh9 = pv.Cube(center=(-20.0, -7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh10 = pv.Cube(center=(-7.5, -7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh11 = pv.Cube(center=(7.5, -7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh12 = pv.Cube(center=(20.0, -7.5, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh13 = pv.Cube(center=(-20.0, -20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh14 = pv.Cube(center=(-7.5, -20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh15 = pv.Cube(center=(7.5, -20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)
mesh16 = pv.Cube(center=(20.0, -20.0, 7.5), x_length=10.0, y_length=10.0, z_length=15.0)

# [mesh, speed, hatch, power, spot size]
settings = [
    [mesh1, 1600, 0.1, 660, 1],
    [mesh2, 1600, 0.1, 660, 10],
    [mesh3, 1600, 0.1, 660, 1],
    [mesh4, 1600, 0.1, 660, 10],
    [mesh5, 1587, 0.11, 720, 1],
    [mesh6, 1587, 0.11, 720, 10],
    [mesh7, 1587, 0.11, 720, 1],
    [mesh8, 1587, 0.11, 720, 10],
    [mesh9, 1576, 0.12, 780, 1],
    [mesh10, 1576, 0.12, 780, 10],
    [mesh11, 1576, 0.12, 780, 1],
    [mesh12, 1576, 0.12, 780, 10],
    [mesh13, 1566, 0.13, 840, 1],
    [mesh14, 1566, 0.13, 840, 10],
    [mesh15, 1566, 0.13, 840, 1],
    [mesh16, 1566, 0.13, 840, 10]
]

parts = []

for part in settings:
    scan_parameters_infill = ScanParameters(spot_size=int(part[4]), beam_power=int(part[3]), scan_speed=int(part[1]*1000), dwell_time=50000)
    infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "point_random", strategy_settings={})
    scan_parameters_contour = ScanParameters(spot_size=int(part[4]), beam_power=int(part[3]), scan_speed=int(part[1]*1000), dwell_time=50000)
    contour_settings = ScanSettings(scan_parameters=scan_parameters_contour, scan_strategy = "line_simple", strategy_settings={})
    part1 = Part(
        mesh = part[0],
        infill_setting = infill_settings,
        contour_setting = infill_settings,
        contour_order = 0,
        point_offset = part[2],
        scan_direction = 0,
        layer_rotation = 67)
    parts.append(part1)

back_scatter = BackScatter(file=r"path_to_replace/new_BSE.obp", start_layer=0, step=3)
build = Build(parts=parts,layer_height=0.07, back_scatter=back_scatter)

#vis_part_layer(part1.layers[0])
path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test4"
generate_build_patterns(build, path)
generate_build_file(build, path + r"\run_file.yml")
