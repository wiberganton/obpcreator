from obplib.Point import Point
from obplib.Line import Line
from obplib.Beamparameters import Beamparameters
from obplib.SyncPoint import SyncPoint
import obplib as obp

def generate_BSE_obp(
    size, 
    line_offset_pre_scan, 
    scan_speed_pre_scan,
    beam_power_pre_scan,
    spot_size_pre_scan,
    line_offset_scan, 
    scan_speed_scan,
    beam_power_scan,
    spot_size_scan,
    file_path):
    obp_elements = []
    x_pos = -size/2
    while x_pos < size/2:
        PointA = Point(x_pos*1000, -1000*size/2)
        PointB = Point(x_pos*1000, 1000*size/2)
        obp_elements.append(Line(PointA, PointB, scan_speed_pre_scan, Beamparameters(spot_size_pre_scan, beam_power_pre_scan)))
        x_pos = x_pos + line_offset_pre_scan
    obp_elements.append(SyncPoint("BSEGain", True, 0))
    obp_elements.append(SyncPoint("BseImage", True, 0))
    x_pos = -size/2
    while x_pos < size/2:
        PointA = Point(x_pos*1000, -1000*size/2)
        PointB = Point(x_pos*1000, 1000*size/2)
        obp_elements.append(Line(PointA, PointB, scan_speed_scan, Beamparameters(spot_size_scan, beam_power_scan)))
        x_pos = x_pos + line_offset_scan
    obp_elements.append(SyncPoint("BseImage", False, 0))
    obp.write_obp(obp_elements,file_path)





