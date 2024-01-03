import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters, BackScatter
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

path = r"C:\Users\antwi87\Downloads\OneDrive_1_1-2-2024"
mesh1 = pv.read(path + "\STL\Solid 1.stl")
mesh2 = pv.read(path + "\STL\Solid 2.stl")
mesh3 = pv.read(path + "\STL\Solid 3.stl")
mesh4 = pv.read(path + "\STL\Solid 4.stl")
mesh5 = pv.read(path + "\STL\Solid 5.stl")



# [mesh, speed, hatch, power, spot size]
settings = [
    [mesh1, 1600, 0.4, 660, 10,"point_random", 808000],
    [mesh2, 1600, 0.4, 660, 10,"point_random", 808000],
    [mesh3, 1600, 0.4, 660, 10,"point_random", 808000],
    [mesh4, 1600, 0.4, 660, 10,"point_random", 808000],
    [mesh5, 1600, 0.4, 660, 10,"point_random", 808000],
]
 
parts = []
 
for part in settings:
    scan_parameters_infill = ScanParameters(spot_size=int(part[4]), beam_power=int(part[3]), scan_speed=int(part[1]*1000), dwell_time=part[6])
    infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = part[5], strategy_settings={})
    part1 = Part(
        mesh = part[0],
        infill_setting = infill_settings,
        contour_setting = infill_settings,
        contour_order = 0,
        point_offset = part[2],
        scan_direction = 0,
        layer_rotation = 90)
    parts.append(part1)
 
#back_scatter = BackScatter(file=r"path_to_replace/LG_660W-40um_60by60_H.obp", start_layer=0, step=12)
build = Build(parts=parts,layer_height=0.07)
 
#vis_part_layer(part1.layers[0])
path2 = path + "\OBP"
generate_build_patterns(build, path)
generate_build_file(build, path2 + r"\run_file.yml")