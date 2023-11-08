# Installation
Install it by cloning the git reprository or from PyPi using:
```bash
pip install obpcreator
```

# Example from stl
import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_part_layer, generate_build_patterns
from obpcreator.visualisation.basic_vis import vis_keep_matrix, vis_part_layer

path1 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw1.stl"
mesh1 = pv.read(path1)
path2 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw2.stl"
mesh2 = pv.read(path2)


contour_settings = ScanSettings(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)

infill_settings1 = ScanSettings(spot_size=1, beam_power=540, scan_speed=1800000, dwell_time=83333)
part1 = Part(
        mesh=mesh1, infill_setting=infill_settings1, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part1 = slice_part(part1)

infill_settings2 = ScanSettings(spot_size=1, beam_power=600, scan_speed=1800000, dwell_time=83333)
part2 = Part(
        mesh=mesh2, infill_setting=infill_settings2, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part2 = slice_part(part2)

build = Build(parts=[part1,part2],layer_height=0.1)

generate_build_patterns(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\screw_2023_10_12")



# To package
- Delete old builds in the \dist folder 
- Update the version in the setup.cfg file
- run "python -m build"
- upload to pip with "twine upload dist/*"
