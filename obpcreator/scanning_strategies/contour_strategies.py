import obplib as obp

def line_simple(paths, scan_settings):
    obp_elements = []
    for path in paths:
        try:
            x_coords, y_coords = zip(*path.vertices)
            x_list = list(x_coords)
            y_list = list(y_coords)
            bp = obp.Beamparameters(scan_settings.scan_parameters.spot_size, scan_settings.scan_parameters.beam_power)
            for i in range(len(x_list)-1):
                a = obp.Point(x_list[i]*1000, y_list[i]*1000)
                b = obp.Point(x_list[i+1]*1000, y_list[i+1]*1000)
                obp_elements.append(obp.Line(a,b,scan_settings.scan_parameters.scan_speed,bp))
            a = obp.Point(x_list[-1]*1000, y_list[-1]*1000)
            b = obp.Point(x_list[0]*1000, y_list[0]*1000)
            obp_elements.append(obp.Line(a,b,scan_settings.scan_parameters.scan_speed,bp))
        except:
            pass
    return obp_elements


