import pyvista as pv
import obpcreator.support_functions.pv_mesh_manipulation as pv_mesh_manipulation
from obpcreator import data_model, point_infill_creation, generate_build

path = r"C:\Users\antwi87\Downloads\OneDrive_1_1-17-2024 (1)\STL"
mesh1 = pv.read(path + r"\Solid1.stl")
mesh1 = pv_mesh_manipulation.place_on_pos(mesh1,(0,0,0))
mesh2 = pv.read(path + r"\Solid2.stl")
mesh2 = pv_mesh_manipulation.place_on_pos(mesh2,(19.5,19.5,0))
mesh3 = pv.read(path + r"\Solid3.stl")
mesh3 = pv_mesh_manipulation.place_on_pos(mesh3,(-19.5,19.5,0))
mesh4 = pv.read(path + r"\Solid4.stl")
mesh4 = pv_mesh_manipulation.place_on_pos(mesh4,(-19.5,-19.5,0))
mesh5 = pv.read(path + r"\Solid5.stl")
mesh5 = pv_mesh_manipulation.place_on_pos(mesh5,(19.5,-19.5,0))
meshes = [mesh1, mesh2, mesh3, mesh4, mesh5]

infill_setting = data_model.ScanParameters(
    spot_size = 10, #[-] 1-100
    beam_power = 660, #[W]
    scan_speed = 2031000, #[micrometers/second]
    dwell_time = 515000, #[ns]
    )
infill = data_model.Infill(
    beam_settings = infill_setting,
    scan_strategy = "point_random",
    strategy_settings = {}
    )
slice_settings = data_model.SlicingSettings(
    point_distance = 0.3,  #mm
    layer_height = 0.07, #mm
    rotation_angle = 0 #deg 
    )
parts = []
for i in range(len(meshes)):
    print("slicing part ", i+1, " out of ", len(meshes))
    point_geometry = point_infill_creation.create_from_pyvista_mesh(meshes[i], slice_settings)
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