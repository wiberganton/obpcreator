from obpcreator.infill import generate_infill
from obpcreator.contour import generate_contour
import obplib as obp

def generate_build_patterns(build, folder_path):
    max_layers = get_max_layers(build)
    for i in range(max_layers):
        layer_obp_elements = []
        for part in build.parts:
            if len(part.layers)>i:
                layer_obp_elements.extend(generate_part_layer(part.layers[i], part.contour_order, part.contour_setting, part.infill_setting))
        output_file = folder_path + f"\layer{i}.obp"
        obp.write_obp(layer_obp_elements,output_file)

def generate_part_layer(part_layer, contour_order, contour_settings, infill_settings):
    obp_objects = []
    #Generate contours
    contour_objects = []
    for contour in part_layer.contours:
        contour_objects = generate_contour(contour.paths, contour_settings)
    if contour_order == 0 or contour_order == 2:
        obp_objects.extend(contour_objects)
    obp_objects.extend(generate_infill(part_layer.infills.point_infill, infill_settings))
    if contour_order == 1 or contour_order == 2:
        obp_objects.extend(contour_objects)
    return obp_objects
    

    #0=contours before infill, 1=contours after  infill, 2=both before and after infill

def get_max_layers(build):
    max_layers = 0
    for part in build.parts:
        max_layers = max(max_layers,len(part.layers))
    return max_layers
