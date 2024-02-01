import sys
from tkinter import messagebox
from pydantic import BaseModel, root_validator, ValidationError
from typing import List, Any
from obpcreator.visualisation.pv_mesh_vis import vis_pv_mesh
from obpcreator import data_model, point_infill_creation, generate_build

class SimpleBuild(BaseModel):
    meshes: List[Any] #Pyvista meshes
    spot_size: List[int] #[-] 1-100
    beam_power: List[int] #[W]
    scan_speed: List[int] #[micrometers/second]
    dwell_time: List[int] #[ns]
    infill_strategy: List[str]
    infill_point_distance: List[float] #[mm]
    infill_settings: List[dict] = [{}]
    rotation_angle: List[float] = [0] #[deg]
    layer_height: float #[mm]
    bse_step: int = 0
    bse_melt: bool = False
    contour_strategy: List[str] = []
    contour_settings: List[dict] = []
    contour_spot_size: List[int] = [] #[-] 1-100
    contour_beam_power: List[int] = [] #[W]
    contour_scan_speed: List[int] = [] #[micrometers/second]
    contour_dwell_time: List[int] = [] #[ns]

    def prepare_build(self, out_path):
        vis_pv_mesh(self.meshes, diameter=100, height=100)
        value = messagebox.askokcancel(title=None, message="Do you want to continue with the build preperation?")
        if not value:
            return
        wanted_len = len(self.meshes)
        if len(self.spot_size)==1 and wanted_len!=1:
            self.spot_size = self.spot_size*wanted_len
        if len(self.beam_power)==1 and wanted_len!=1:
            self.beam_power = self.beam_power*wanted_len
        if len(self.scan_speed)==1 and wanted_len!=1:
            self.scan_speed = self.scan_speed*wanted_len
        if len(self.dwell_time)==1 and wanted_len!=1:
            self.dwell_time = self.dwell_time*wanted_len
        if len(self.infill_strategy)==1 and wanted_len!=1:
            self.infill_strategy = self.infill_strategy*wanted_len
        if len(self.infill_point_distance)==1 and wanted_len!=1:
            self.infill_point_distance = self.infill_point_distance*wanted_len
        if len(self.infill_settings)==1 and wanted_len!=1:
            self.infill_settings = self.infill_settings*wanted_len
        if len(self.rotation_angle)==1 and wanted_len!=1:
            self.rotation_angle = self.rotation_angle*wanted_len
        
        parts = []
        sys.stdout.write(f'Slicing parts')  # Print the message
        sys.stdout.flush()  # Ensure the message is displayed
        for i in range(len(self.meshes)):
            sys.stdout.write(f'\rSlicing part {i+1}/{len(self.meshes)}')  # Print the message
            sys.stdout.flush()  # Ensure the message is displayed
            slice_settings = data_model.SlicingSettings(
                point_distance = self.infill_point_distance[i],  #mm
                layer_height = self.layer_height, #mm
                rotation_angle = self.rotation_angle[i] #deg 
            )
            point_geometry = point_infill_creation.create_from_pyvista_mesh(self.meshes[i], slice_settings)
            infill_setting = data_model.ScanParameters(
                spot_size = self.spot_size[i], #[-] 1-100
                beam_power = self.beam_power[i], #[W]
                scan_speed = self.scan_speed[i], #[micrometers/second]
                dwell_time = self.dwell_time[i], #[ns]
            )
            infill = data_model.Infill(
                beam_settings = infill_setting,
                scan_strategy = self.infill_strategy[i],
                strategy_settings = self.infill_settings[i]
                )
            if len(self.contour_strategy) > 0:
                contour_setting = data_model.ScanParameters(
                    spot_size = self.contour_spot_size[i], #[-] 1-100
                    beam_power = self.contour_beam_power[i], #[W]
                    scan_speed = self.contour_scan_speed[i], #[micrometers/second]
                    dwell_time = self.contour_dwell_time[i], #[ns]
                    )
                contour = data_model.Contour(
                    beam_settings = contour_setting,
                    scan_strategy = self.contour_strategy[i],
                    strategy_settings = self.contour_settings[i],
                    numb_of_layers = 1,
                    outer_offset = 0,
                    contour_offset = 0
                    )
                part1 = data_model.Part(
                    point_geometry = point_geometry,
                    infill_setting = infill,
                    contour_setting = contour
                )
            else: 
                part1 = data_model.Part(
                    point_geometry = point_geometry,
                    infill_setting = infill,
                )
            parts.append(part1)
        bse = data_model.BackScatter(
            file="BSE_Scan_PT.obp",
            step = self.bse_step
        )
        build = data_model.Build(
            parts = parts,
            layer_height = self.layer_height, #mm
            back_scatter=bse,
            back_scatter_melting = self.bse_melt
        )
        generate_build.generate_build(build, out_path)
   

