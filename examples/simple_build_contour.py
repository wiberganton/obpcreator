from obpcreator.simple_input import SimpleBuild
import pyvista as pv

cube1 = pv.Cube(center=(10,-10,5),x_length=10,y_length=10,z_length=10)
cube2 = pv.Cube(center=(10,10,5),x_length=10,y_length=10,z_length=10)
cube3 = pv.Cube(center=(-10,-10,5),x_length=10,y_length=10,z_length=10)
cube4 = pv.Cube(center=(-10,10,5),x_length=10,y_length=10,z_length=10)

build = SimpleBuild(
    meshes = [cube1, cube2],
    spot_size = [1],
    beam_power = [660],
    scan_speed = [2031000],
    dwell_time = [515000],
    infill_strategy = [""],
    infill_settings = [{}],
    infill_point_distance = [0.1],
    layer_height = 0.1,
    rotation_angle = [0],
    contour_strategy = ["line_simple", "point_simple"],
    contour_settings = [{},{'step': 0.1, 'jump': 2}],
    contour_spot_size = [1,1], #[-] 1-100
    contour_beam_power = [660,660] ,#[W]
    contour_scan_speed = [2031000,2031000] ,#[micrometers/second]
    contour_dwell_time = [515000,515000] #[ns]
    )
build.prepare_build(r"C:\Users\antwi87\Downloads\slicerTest2")