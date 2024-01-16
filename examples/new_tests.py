from obpcreator import data_model, point_infill_creation, generate_build
import pyvista as pv

def test_basic_data_model():
    infill_setting = data_model.ScanParameters(
        spot_size = 1, #[-] 1-100
        beam_power = 1, #[W]
        scan_speed = 1800000, #[micrometers/second]
        dwell_time = 1, #[ns]
        )
    infill = data_model.Infill(
        settings = infill_setting,
        scan_strategy = "",
        strategy_settings = {}
        )
    coords, keep = point_infill_creation.generate_matrices(-10, 10, -10, -10, 10, 1, 1, start_angle=0, rotation_angle=0, uniform_point_dist=True, offset_margin=3)
    point_geometry = data_model.PointGeometry(
        coord_matrix = coords, #3D numpy matrix with the coords of the points as complex numbers in mm
        keep_matrix = keep
    )
    part1 = data_model.Part(
        point_geometry = point_geometry,
        infill_setting = infill
    )
    build = data_model.Build(
        parts = [part1],
        layer_height = 0.1 #mm
    )

def test_basic_cube():
    infill_setting = data_model.ScanParameters(
        spot_size = 1, #[-] 1-100
        beam_power = 680, #[W]
        scan_speed = 1800000, #[micrometers/second]
        dwell_time = 50000, #[ns]
        )
    infill = data_model.Infill(
        beam_settings = infill_setting,
        scan_strategy = "line_right_left",
        strategy_settings = {}
        )
    mesh = pv.Cube(center=(0,0,5), x_length=10, y_length=10, z_length=10)
    point_geometry = point_infill_creation.create_from_pyvista_mesh(mesh, 0.1, 0.1, start_angle=0, rotation_angle=60, uniform_point_dist=True, offset_margin=2)
    part1 = data_model.Part(
        point_geometry = point_geometry,
        infill_setting = infill
    )
    build = data_model.Build(
        parts = [part1],
        layer_height = 0.1 #mm
    )
    return build

def test_obp_generation(path):
    build = test_basic_cube()
    generate_build.generate_build(build, path)
#test_basic_cube()
test_obp_generation(r"C:\Users\antwi87\Downloads\obp_output")