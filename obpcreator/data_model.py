import json
from typing import Any, List, Literal, Optional, Dict
import numpy as np
from pydantic import BaseModel

class ScanParameters(BaseModel):
    spot_size: int #[-] 1-100
    beam_power: int #[W]
    scan_speed: int #[micrometers/second]
    dwell_time: int #[ns]

class ScanSettings(BaseModel):
    scan_parameters: ScanParameters
    scan_strategy: str
    strategy_settings: Dict[str, Any] = {}

class SlicingSettings(BaseModel):
    layer_height: float #in mm
    outer_offset: float #Offset between mesh and first manufacturing point, in mm
    contour_layers: int #nmb of contours
    contour_offset: float #Offset between contour layers, in mm
    contour_infill_offset: float #Offset between contours and infill, in mm

class PointInfill(BaseModel):
    coord_matrix: Any #numpy matrix with the coords of the points as complex numbers in mm
    keep_matrix: Any #numpy matrix with which points to manufacture

class Infill(BaseModel):
    paths: List[Any] #List of matplotlib paths
    scan_angle: float = 0 #Angle (deg) in which normal scanning happens
    point_infill: PointInfill

class Contour(BaseModel):
    paths: List[Any] #List of matplotlib paths
    start_angle: float = 0 #Angle (deg) where to start the contour

class PartLayer(BaseModel):
    infills: Infill = None
    contours: List[Contour] = []

class Part(BaseModel):
    mesh: Any #Pyvista mesh
    infill_setting: ScanSettings
    contour_setting: ScanSettings
    layers: List[PartLayer] = []
    contour_order: int = 0 #0=contours before infill, 1=contours after  infill, 2=both before and after infill
    point_offset: float #offset distance between scan points used in mm
    scan_direction: float = 0 #scan angle of first layer
    layer_rotation: float = 0 #rotation between each layer 
    slicing_settings: SlicingSettings


class Build(BaseModel):
    parts: List[Part]
    layer_height: float #mm


