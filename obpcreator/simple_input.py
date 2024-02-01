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
    scan_strategy: List[str]
    point_distance: List[float] #[mm]
    scan_settings: List[dict] = [{}]
    rotation_angle: List[float] = [0] #[deg]
    layer_height: float #[mm]
    bse_step: int = 0
    bse_melt: bool = False
    @root_validator(pre=True)
    def initial_processing(cls, values):
        meshes = values.get('meshes')
        spot_size = values.get('spot_size')
        beam_power = values.get('beam_power')
        scan_speed = values.get('scan_speed')
        dwell_time = values.get('dwell_time')
        scan_strategy = values.get('scan_strategy')
        point_distance = values.get('point_distance')
        scan_settings = values.get('scan_settings')
        rotation_angle = values.get('rotation_angle')
        if spot_size is not None:
            if not (len(spot_size) == 1 or len(spot_size)==len(meshes)):
                raise ValueError('Length of spot_size is wrong')
        if beam_power is not None:
            if not (len(beam_power) == 1 or len(beam_power)==len(meshes)):
                raise ValueError('Length of beam_power is wrong')
        if scan_speed is not None:
            if not (len(scan_speed) == 1 or len(scan_speed)==len(meshes)):
                raise ValueError('Length of scan_speed is wrong')
        if dwell_time is not None:
            if not (len(dwell_time) == 1 or len(dwell_time)==len(meshes)):
                raise ValueError('Length of dwell_time is wrong')
        if scan_strategy is not None:
            if not (len(scan_strategy) == 1 or len(scan_strategy)==len(meshes)):
                raise ValueError('Length of scan_strategy is wrong')
        if point_distance is not None:
            if not (len(point_distance) == 1 or len(point_distance)==len(meshes)):
                raise ValueError('Length of point_distance is wrong')
        if scan_settings is not None:
            if not (len(scan_settings) == 1 or len(scan_settings)==len(meshes)):
                raise ValueError('Length of scan_settings is wrong')
        if rotation_angle is not None:
            if not (len(rotation_angle) == 1 or len(rotation_angle)==len(meshes)):
                raise ValueError('Length of rotation_angle is wrong')

        return values
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
        if len(self.scan_strategy)==1 and wanted_len!=1:
            self.scan_strategy = self.scan_strategy*wanted_len
        if len(self.point_distance)==1 and wanted_len!=1:
            self.point_distance = self.point_distance*wanted_len
        if len(self.scan_settings)==1 and wanted_len!=1:
            self.scan_settings = self.scan_settings*wanted_len
        if len(self.rotation_angle)==1 and wanted_len!=1:
            self.rotation_angle = self.rotation_angle*wanted_len
        
        parts = []
        sys.stdout.write(f'Slicing parts')  # Print the message
        sys.stdout.flush()  # Ensure the message is displayed
        for i in range(len(self.meshes)):
            sys.stdout.write(f'\rSlicing part {i+1}/{len(self.meshes)}')  # Print the message
            sys.stdout.flush()  # Ensure the message is displayed
            slice_settings = data_model.SlicingSettings(
                point_distance = self.point_distance[i],  #mm
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
                scan_strategy = self.scan_strategy[i],
                strategy_settings = self.scan_settings[i]
                )
            part1 = data_model.Part(
                point_geometry = point_geometry,
                infill_setting = infill
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
   

import pyvista as pv


build = SimpleBuild(
    meshes = [pv.Cube(center=(0,0,5),x_length=10,y_length=10,z_length=10), pv.Cube(center=(0,20,5),x_length=10,y_length=10,z_length=10)],
    spot_size = [1],
    beam_power = [660],
    scan_speed = [2031000],
    dwell_time = [515000],
    scan_strategy = ["line_concentric"],
    scan_settings = [{'direction': 'inward'}, {'direction': 'outward'}],
    point_distance = [0.1],
    layer_height = 0.1,
    rotation_angle = [90])
build.prepare_build(r"C:\Users\antwi87\Downloads\slicerTest2")
