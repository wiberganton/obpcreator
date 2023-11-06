import pathlib
import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns
from obpcreator.visualisation.basic_vis import vis_keep_matrix, vis_part_layer

cube1_path = str((pathlib.Path(__file__).parent / "tests" / "models" / "cube1.stl").resolve())
mesh1 = pv.read(cube1_path)
infill_parameters = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
contour_parameters = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=infill_parameters, scan_strategy="line_snake")
contour_settings = ScanSettings(scan_parameters=contour_parameters, scan_strategy="line_simple")
slice_settings = SlicingSettings(layer_height=5, outer_offset=0.05, contour_layers=1, contour_offset=0.1, contour_infill_offset=0.05)
part1 = Part(
        mesh=mesh1, infill_setting=infill_settings, 
        contour_setting=contour_settings, contour_order=0, 
        point_offset=0.1, layer_rotation=90, scan_direction=45,
        slicing_settings=slice_settings)
part1 = slice_part(part1)

cube2_path = str((pathlib.Path(__file__).parent / "tests" / "models" / "cube2.stl").resolve())
mesh2 = pv.read(cube2_path)
infill_parameters = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
contour_parameters = ScanParameters(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
infill_settings = ScanSettings(scan_parameters=infill_parameters, scan_strategy="point_random")
contour_settings = ScanSettings(scan_parameters=contour_parameters, scan_strategy="line_simple")
slice_settings = SlicingSettings(layer_height=5, outer_offset=0.05, contour_layers=1, contour_offset=0.1, contour_infill_offset=0.05)
part2 = Part(
        mesh=mesh2, infill_setting=infill_settings, 
        contour_setting=contour_settings, contour_order=0, 
        point_offset=0.1, layer_rotation=90, scan_direction=45,
        slicing_settings=slice_settings)
part2 = slice_part(part2)

build = Build(parts=[part1,part2],layer_height=0.1)

#vis_part_layer(part1.layers[0])
generate_build_patterns(build, r"C:\Users\antwi87\Documents\GitHub\obpgenerator\obpgenerator\obpviewer")
