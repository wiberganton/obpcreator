import pyvista as pv
import obpcreator.support_functions.pv_mesh_manipulation as pv_mesh_manipulation
from obpcreator import data_model, point_infill_creation, generate_build

mesh1 = pv.Cube(center=(0,0,5), x_length=10, y_length=10, z_length=10)
mesh2 = pv.Cube(center=(0,0,5), x_length=10, y_length=10, z_length=10)
meshes = [mesh1, mesh2]

# settings order: spot_size, beam_power, scan_speed, dwell_time, scan_strategy, point_distance, rotation_angle
settings = [
    [10, 660, 2031000, 515000, "point_random", 0.3, 0],
    [10, 660, 2031000, 515000, "line_spiral_inward", 0.3, 0]
]
layer_height = 0.07



parts = []
for i in range(len(meshes)):
    print("slicing part ", i+1, " out of ", len(meshes))
    slice_settings = data_model.SlicingSettings(
        point_distance = settings[i][5],  #mm
        layer_height = layer_height, #mm
        rotation_angle = settings[i][6] #deg 
    )
    point_geometry = point_infill_creation.create_from_pyvista_mesh(meshes[i], slice_settings)
    infill_setting = data_model.ScanParameters(
        spot_size = settings[i][0], #[-] 1-100
        beam_power = settings[i][1], #[W]
        scan_speed = settings[i][2], #[micrometers/second]
        dwell_time = settings[i][3], #[ns]
    )
    infill = data_model.Infill(
        beam_settings = infill_setting,
        scan_strategy = settings[i][4],
        strategy_settings = {}
        )
    print("sliced part ", i+1, " out of ", len(meshes))
    part1 = data_model.Part(
        point_geometry = point_geometry,
        infill_setting = infill
    )
    parts.append(part1)
bse = data_model.BackScatter(
    file="BSE_Scan_PT.obp",
    step = 1
)
build = data_model.Build(
    parts = parts,
    layer_height = 0.07, #mm
    back_scatter=bse,
    back_scatter_melting = True
)
out_path = r"C:\Users\antwi87\Downloads\slicerTest2"
generate_build.generate_build(build, out_path)