import pyvista as pv

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings, ScanParameters, BackScatter
from obpcreator.support_functions.slicer import slice_part
from obpcreator.generate_scan_patterns import generate_build_patterns, generate_build_file

mesh12 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw12_2.stl")
mesh13 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw13_2.stl")
mesh14 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw14.stl")
mesh15 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw15.stl")
mesh16 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw16.stl")
mesh17 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw17.stl")
mesh18 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw18.stl")
mesh19 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw19.stl")
mesh20 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw20.stl")
mesh21 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw21.stl")
mesh22 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw22.stl")
mesh23 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw23.stl")
mesh24 = pv.read(r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\Screw24.stl")

settings = [
    [mesh12, 720, 400, 50000, 140000],
    [mesh13, 680, 400, 52941, 140000],
    [mesh14, 850, 400, 42352, 140000],
    [mesh15, 850, 0, 42352, 0],
    [mesh16, 680, 0, 52941, 0],
    [mesh17, 720, 0, 50000, 0],
    [mesh18, 720, 400, 58333, 140000],
    [mesh19, 680, 400, 61764, 140000],
    [mesh20, 850, 400, 49411, 140000],
    [mesh21, 850, 0, 49411, 0],
    [mesh22, 680, 0, 61764, 0],
    [mesh23, 720, 0, 58333, 0],
    [mesh24, 900, 0, 46666, 0]
]

parts = []

for part in settings:
    scan_parameters_contour = ScanParameters(spot_size=1, beam_power=part[2], scan_speed=part[4], dwell_time=1)
    scan_parameters_infill = ScanParameters(spot_size=1, beam_power=part[1], scan_speed=1800000, dwell_time=part[3])
    contour_settings = ScanSettings(scan_parameters=scan_parameters_contour, scan_strategy = "line_simple", strategy_settings={})
    infill_settings = ScanSettings(scan_parameters=scan_parameters_infill, scan_strategy = "point_random", strategy_settings={})
    if part[2]>0:
        slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=1, contour_offset=0.0, contour_infill_offset=0.05)
    else:
        slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)
    part1 = Part(
        mesh = part[0],
        infill_setting = infill_settings,
        contour_setting = contour_settings,
        contour_order = 0,
        point_offset = 0.1,
        scan_direction = 0,
        layer_rotation = 90,
        slicing_settings = slice_settings)
    part1 = slice_part(part1)
    parts.append(part1)

#back_scatter = BackScatter(file=r"path_to_replace/LG_660W-40um_60by60_V.obp", start_layer=0, step=1)
build = Build(parts=parts,layer_height=0.1,back_scatter_melting=True) #, back_scatter=back_scatter)

#vis_part_layer(part1.layers[0])
path = r"C:\Users\antwi87\OneDrive - Linköpings universitet\Undervisning\TMPx\2023\Print_nr2_STLs\print_2023_11_15"
generate_build_patterns(build, path)
generate_build_file(build, path + r"\run_file.yml")
