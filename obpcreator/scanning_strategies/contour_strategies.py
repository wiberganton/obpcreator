import obplib as obp

def line_simple(part, layer):
    scan_settings = part.contour_setting.beam_settings
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    contours = part.point_geometry.get_contours(layer)
    obp_elements = []
    for contour in contours:
        line = contour.buffer(-part.contour_setting.outer_offset)
        for i in range(part.contour_setting.numb_of_layers):
            x, y = line.exterior.xy
            for i in range(len(x)-1):
                a = obp.Point(x[i]*1000, y[i]*1000)
                b = obp.Point(x[i+1]*1000, y[i+1]*1000)
                obp_elements.append(obp.Line(a,b,scan_settings.scan_speed,bp))
            line = line.buffer(-part.contour_setting.contour_offset)
    return obp_elements

def point_simple(part, layer):
    def even_sampling(line, distance):
        boundary = line.boundary
        total_length = boundary.length
        sampled_points = []
        current_distance = 0
        while current_distance < total_length:
            # Get a point at the current distance along the boundary
            point = boundary.interpolate(current_distance)
            sampled_points.append(point)
            current_distance += distance
        sampled_points_coords = [point.coords[0] for point in sampled_points]
        return sampled_points_coords
    
    scan_settings = part.contour_setting.beam_settings
    point_distance = part.contour_setting.strategy_settings['step']
    if 'jump' in part.contour_setting.strategy_settings:
        jump = part.contour_setting.strategy_settings['jump']
    else:
        jump = 1
    bp = obp.Beamparameters(scan_settings.spot_size, scan_settings.beam_power)
    contours = part.point_geometry.get_contours(layer)
    obp_elements = []
    for contour in contours:
        line = contour.buffer(-part.contour_setting.outer_offset)
        for i in range(part.contour_setting.numb_of_layers):
            points = even_sampling(line, point_distance)
            for ii in range(jump):
                for i in range(ii,len(points),jump):
                    a = obp.Point(points[i][0]*1000, points[i][1]*1000)
                    obp_elements.append(obp.TimedPoints([a], [scan_settings.dwell_time], bp))
            line = line.buffer(-part.contour_setting.contour_offset)
    return obp_elements
"""
beam_settings: ScanParameters = None
scan_strategy: str = ""
strategy_settings: Dict[str, Any] = {}
numb_of_layers: int = 0
outer_offset: float = 0
contour_offset: float = 0
"""