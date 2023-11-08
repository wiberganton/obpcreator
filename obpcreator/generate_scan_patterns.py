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
    #0=contours before infill, 1=contours after  infill, 2=both before and after infill
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
    
def generate_build_file(build, path):
    nmb_of_layers = get_max_layers(build)
    lines_to_write = []
    lines_to_write.append(f"build:")
    lines_to_write.append(f"  start_heat:")
    lines_to_write.append(f"    file: {build.start_heat.file}")
    lines_to_write.append(f"    temp_sensor: {build.start_heat.temp_sensor}")
    lines_to_write.append(f"    target_temperature: {build.start_heat.target_temperature}")
    lines_to_write.append(f"    timeout: {build.start_heat.timeout}")
    lines_to_write.append(f"  preheat:")
    lines_to_write.append(f"    file: {build.pre_heat.file}")
    lines_to_write.append(f"    repetitions: {build.pre_heat.repetitions}")
    lines_to_write.append(f"  postheat:")
    lines_to_write.append(f"    file: {build.post_heat.file}")
    lines_to_write.append(f"    repetitions: {build.post_heat.repetitions}")
    lines_to_write.append(f"  build:")
    lines_to_write.append(f"    layers: {nmb_of_layers}")
    lines_to_write.append(f"    files:")
    for i in range(nmb_of_layers):
        obp_files = []
        obp_files.append(f"path_to_replace/layer{i}.obp")
        if build.back_scatter.step != 0 and (i-build.back_scatter.start_layer)%build.back_scatter.step == 0:
            if build.back_scatter.after_melting:
                obp_files.append(build.back_scatter.file)
            else:
                obp_files.insert(0, build.back_scatter.file)
        if len(obp_files) == 1:
            lines_to_write.append(f"      - " + obp_files[0])
        else:
            for ii in range(len(obp_files)):
                if ii == 0:
                    lines_to_write.append(f"      - - " + obp_files[ii])
                else:
                    lines_to_write.append(f"        - " + obp_files[ii])
    lines_to_write.append("  layerfeed:")
    lines_to_write.append(f"    build_piston_distance: {build.layerfeed.build_piston_distance}")
    lines_to_write.append(f"    powder_piston_distance: {build.layerfeed.powder_piston_distance}")
    lines_to_write.append(f"    recoater_advance_speed: {build.layerfeed.recoater_advance_speed}")
    lines_to_write.append(f"    recoater_retract_speed: {build.layerfeed.recoater_retract_speed}")
    lines_to_write.append(f"    recoater_dwell_time: {build.layerfeed.recoater_dwell_time}")
    lines_to_write.append(f"    recoater_full_repeats: {build.layerfeed.recoater_full_repeats}")
    lines_to_write.append(f"    recoater_build_repeats: {build.layerfeed.recoater_build_repeats}")
    lines_to_write.append(f"    triggered_start: {build.layerfeed.triggered_start}")
    lines_with_newlines = [line + '\n' for line in lines_to_write]
    f = open(path, "w")
    f.writelines(lines_with_newlines)
    f.close()


def get_max_layers(build):
    max_layers = 0
    for part in build.parts:
        max_layers = max(max_layers,len(part.layers))
    return max_layers
