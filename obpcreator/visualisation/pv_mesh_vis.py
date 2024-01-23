import pyvista as pv
import obpcreator.support_functions.pv_mesh_manipulation as pv_mesh_manipulation

def vis_pv_meshes(paths, diameter=100, height=100):
    plotter = pv.Plotter()
    build_plate = pv.Cylinder(radius=diameter/2, height=20, center=[0,0,-10], direction=[0,0,1])
    plotter.add_mesh(build_plate, color='blue', show_edges=False)
    build_chamber = pv.Cylinder(radius=diameter/2, height=height, center=[0,0,height/2], direction=[0,0,1])
    plotter.add_mesh(build_chamber, color='red', show_edges=False, opacity=0.25)
    for path in paths:
        mesh = pv.read(path)
        mesh = pv_mesh_manipulation.place_on_pos(mesh,(-19.5,-19.5,0))
        plotter.add_mesh(mesh)
        
        is_closed = mesh.is_all_triangles()
        print("Mesh:", is_closed)

    plotter.show()
path = r"C:\Users\antwi87\Downloads\OneDrive_1_1-17-2024 (1)\STL"
meshes = [
    path + r"\Solid1.stl",
    path + r"\Solid2.stl",
    path + r"\Solid3.stl",
    path + r"\Solid4.stl",
    path + r"\Solid5.stl"
]
vis_pv_meshes(meshes, diameter=100, height=100)