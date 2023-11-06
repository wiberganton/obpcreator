from obpcreator.support_functions.slicer import slice_stl
from obpcreator.support_functions.offset_paths import offset_array
from obpcreator.data_model import Infill, Contour, PartLayer, Part, Build

def setup_build(stl_paths, layer_height, infill_settings, point_offset, layer_rotation=0, contour_settings = None, contour_order=0, out_offset=0, contour_layers=0, contour_offset=0.1, contour_infill_offset=0.1):
    """
    stl_paths = List of str paths to stl files
    layer_height = height of layers in mm
    infill_settings = manufacturing settings for the infill, May be a list if different values is wanted for different parts
    contour_settings = manufacturing settings for the contour, May be a list if different values is wanted for different parts
    out_offset = outer compensation of geometry in mm. May be a list if different values is wanted for different parts
    contour_layers = number of contours. May be a list if different values is wanted for different parts
    contour_offset = distance between each contour layer in mm. May be a list if different values is wanted for different parts
    contour_infill_offset = distance between inner counter layer and infill. May be a list if different values is wanted for different parts
    """
    def make_list(value, nmb):
        if not isinstance(value, list):
            return [value] * nmb
        else:
            return value
    out_offset = make_list(out_offset, len(stl_paths))
    contour_layers = make_list(contour_layers, len(stl_paths))
    contour_offset = make_list(contour_offset, len(stl_paths))
    contour_infill_offset = make_list(contour_infill_offset, len(stl_paths))
    infill_settings = make_list(infill_settings, len(stl_paths))
    contour_settings = make_list(contour_settings, len(stl_paths))
    contour_order = make_list(contour_order, len(stl_paths))
    point_offset = make_list(point_offset, len(stl_paths))
    layer_rotation = make_list(layer_rotation, len(stl_paths))
    parts = []
    for i in range(len(stl_paths)):
        slices = slice_stl(stl_paths[i], layer_height)
        part_layers = []
        for slice in slices[0]:
            part = slice
            contour_paths = []
            offset_factor = out_offset[i]
            for ii in range(contour_layers[i]):
                offset_factor += contour_offset[i]*ii
                part = offset_array(part, offset_factor)
                contour_paths.extend(part)
                if ii == contour_layers[i] - 1:
                    offset_factor += contour_infill_offset[i]
            infill_paths = offset_array(part, offset_factor)
            infill = Infill(paths=infill_paths)
            contour = Contour(paths=contour_paths)
            part_layers.append(PartLayer(infills=[infill], contours=[contour]))
        parts.append(Part(infill_setting=infill_settings[i], contour_setting=contour_settings[i], layers=part_layers, contour_order=contour_order[i], point_offset=point_offset[i], layer_rotation=layer_rotation[i]))
    
    return Build(parts=parts, layer_height=layer_height)
    