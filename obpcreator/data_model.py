from typing import Any, List, Dict, Optional
from pydantic import BaseModel

class ScanParameters(BaseModel):
    spot_size: int = 1 #[-] 1-100
    beam_power: int = 1 #[W]
    scan_speed: int = 1800000 #[micrometers/second]
    dwell_time: int = 1 #[ns]

class ScanSettings(BaseModel):
    scan_parameters: ScanParameters = ScanParameters()
    scan_strategy: str = ""
    strategy_settings: Dict[str, Any] = {}

class SlicingSettings(BaseModel):
    outer_offset: float = 0 #Offset between mesh and first manufacturing point, in mm
    contour_layers: int = 0 #nmb of contours
    contour_offset: float = 0 #Offset between contour layers, in mm
    contour_infill_offset: float = 0 #Offset between contours and infill, in mm

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
    infill_setting: ScanSettings = ScanSettings()
    contour_setting: ScanSettings = ScanSettings()
    layers: List[PartLayer] = []
    contour_order: int = 0 #0=contours before infill, 1=contours after  infill, 2=both before and after infill
    #point_offset: float #offset distance between scan points used in mm
    point_offset: Optional[float] = None #offset distance between scan points used in mm
    hatch_distance: Optional[float] = None #Hatch distance distance in mm
    scan_direction: float = 0 #scan angle of first layer
    layer_rotation: float = 0 #rotation between each layer 
    slicing_settings: SlicingSettings = SlicingSettings()

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


