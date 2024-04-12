from typing import Any, List, Dict, Optional
from pydantic import BaseModel
from numpy import copy
from scipy.ndimage import binary_dilation, binary_erosion
import cv2
import math
from shapely.geometry import Polygon


class ScanParameters(BaseModel):
    spot_size: int = 1 #[-] 1-100
    beam_power: int = 1 #[W]
    scan_speed: int = 1800000 #[micrometers/second]
    dwell_time: int = 1 #[ns]

class SlicingSettings(BaseModel):
    point_distance: float = 0.1  #mm
    layer_height: float = 0.1 #mm
    hatch_distance: float = math.sqrt(3/4)*0.1  #mm
    start_angle: float = 0 #deg 
    rotation_angle: float = 0 #deg 
    uniform_point_dist: bool = True
    offset_margin: float = 1 #mm

    def __init__(self, **data):
        if 'hatch_distance' in data and 'point_distance' not in data:
            data['point_distance'] = data['hatch_distance']/math.sqrt(3/4)
        if 'point_distance' in data:
            data['hatch_distance'] = data['point_distance']*math.sqrt(3/4)
        super().__init__(**data)


class PointGeometry(BaseModel):
    coord_matrix: Any #3D numpy matrix with the coords of the points as complex numbers in mm
    keep_matrix: Any #3D numpy matrix with which points to manufacture
    def get_point_distance(self):
        coord1 = self.coord_matrix[1,0,0,0:2]
        coord2 = self.coord_matrix[0,0,0,0:2]
        distance = math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)
        return distance
    def get_layer(self, layer):
        x_coords = self.coord_matrix[:, :, layer, 0]
        y_coords = self.coord_matrix[:, :, layer, 1]
        coords = x_coords + 1j * y_coords
        return coords, self.keep_matrix[:,:,layer] 
    def get_contours(self, layer):
        matrix = self.keep_matrix[:,:,layer]
        coords = self.coord_matrix[:,:,layer,:]
        contours, _ = cv2.findContours(matrix, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        simplified_contours = []
        epsilon_factor = (self.coord_matrix[1,0,0,0] - self.coord_matrix[0,0,0,0])*1.0 #Simplification factor
        for cnt in contours:
            epsilon = epsilon_factor * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            # Initialize an empty list to hold the mapped real-world coordinates for this contour
            real_world_contour_points = []
            for point in approx.reshape(-1, 2):
                # Map the pixel positions to real-world coordinates
                # Ensure to convert point indices to integers, as they will be used as indices
                x_pixel, y_pixel = point.astype(int)
                real_world_x, real_world_y = coords[y_pixel, x_pixel, 0], coords[y_pixel, x_pixel, 1]
                real_world_contour_points.append((real_world_x, real_world_y))
            
            # Create a Shapely Polygon with the real-world coordinates
            polygon = Polygon(real_world_contour_points)
            simplified_contours.append(polygon)
        return simplified_contours
    def offset_contours(self, offset_distance):
        point_distance = self.get_point_distance()
        offset_steps = round(offset_distance/point_distance)
        keep_matrix = copy(self.keep_matrix)
        for i in range(keep_matrix.shape[2]):
            matrix = keep_matrix[:,:,i]
            if offset_steps > 0:
                for _ in range(offset_steps):
                    matrix = binary_dilation(matrix)
            else:
                for _ in range(abs(offset_steps)):
                    matrix = binary_erosion(matrix)
            keep_matrix[:,:,i] = matrix.astype(int)
        return PointGeometry(coord_matrix=self.coord_matrix, keep_matrix=keep_matrix)
    def offset_contours_layer(self, offset_distance, layer):
        point_distance = self.coord_matrix[1,0,0,0] - self.coord_matrix[0,0,0,0]
        offset_steps = round(offset_distance/point_distance)
        keep_matrix = copy(self.keep_matrix)
        matrix = keep_matrix[:,:,layer]
        if offset_steps > 0:
            for _ in range(offset_steps):
                matrix = binary_dilation(matrix)
        else:
            for _ in range(abs(offset_steps)):
                matrix = binary_erosion(matrix)
        keep_matrix[:,:,layer] = matrix.astype(int)
        return PointGeometry(coord_matrix=self.coord_matrix, keep_matrix=keep_matrix)



class Infill(BaseModel):
    beam_settings: ScanParameters = None
    scan_strategy: str = ""
    strategy_settings: Dict[str, Any] = {}
    infill_offset: float = 0

class Contour(BaseModel):
    beam_settings: ScanParameters = None
    scan_strategy: str = ""
    strategy_settings: Dict[str, Any] = {}
    numb_of_layers: int = 0
    outer_offset: float = 0
    contour_offset: float = 0

class Part(BaseModel):
    point_geometry: PointGeometry
    infill_setting: Infill = None
    contour_setting: Contour = None
    contour_order: int = 0 #0=contours before infill, 1=contours after  infill, 2=both before and after infill

class StartHeat(BaseModel):
    file: str = ""
    temp_sensor: str = "Sensor1"
    target_temperature: int = 800
    timeout:int = 3600

class PreHeat(BaseModel):
    file: str = ""
    repetitions: int = 10

class PostHeat(BaseModel):
    file: str = ""
    repetitions: int = 0

class Layerfeed(BaseModel):
    build_piston_distance: float = -0.07
    powder_piston_distance: float = 0.15
    recoater_advance_speed: float = 100.0
    recoater_retract_speed: float = 100.0
    recoater_dwell_time: float = 0
    recoater_full_repeats: int = 0
    recoater_build_repeats: int = 0
    triggered_start: bool = True

class BackScatter(BaseModel):
    file: str = "" #Which obp file that contains tha backscatter scan
    start_layer: int = 0 #At which layer the backscatter should be applied
    step: int = 0 #At which nth layer it should be run, if 0 not run at all
    after_melting: bool = True #If true the backscatter will be run after after the melting obp, otherwise before the melting

class Build(BaseModel):
    parts: List[Part]
    layer_height: float #mm
    start_heat: StartHeat = StartHeat()
    pre_heat: PreHeat = PreHeat()
    post_heat: PostHeat = PostHeat()
    layerfeed: Layerfeed = Layerfeed()
    back_scatter: BackScatter = BackScatter()
    back_scatter_melting: bool = False
    seperate_parts_obp: bool = False


