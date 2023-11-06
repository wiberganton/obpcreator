import pytest
import pathlib
import pyvista as pv
import obplib as obp
import numpy as np

from obpcreator.data_model import ScanSettings, Part, Build, SlicingSettings
from obpcreator.setup_build import setup_build
from obpcreator.support_functions.slicer import slice_part
from obpcreator.infill import generate_infill
from obpcreator.contour import generate_contour
from obpcreator.generate_scan_patterns import generate_part_layer, generate_build_patterns
from obpcreator.visualisation.basic_vis import vis_keep_matrix, vis_part_layer

path1 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw1.stl"
mesh1 = pv.read(path1)
path2 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw2.stl"
mesh2 = pv.read(path2)
path3 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw3_4.stl"
mesh3 = pv.read(path3)
path4 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw5.stl"
mesh4 = pv.read(path4)
path5 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw6.stl"
mesh5 = pv.read(path5)
path6 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw7.stl"
mesh6 = pv.read(path6)
path7 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw8.stl"
mesh7 = pv.read(path7)
path8 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw9.stl"
mesh8 = pv.read(path8)
path9 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw10_11.stl"
mesh9 = pv.read(path9)
path10 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw12.stl"
mesh10 = pv.read(path10)
path11 = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\geoemtrier\Screw13.stl"
mesh11 = pv.read(path11)

contour_settings = ScanSettings(spot_size=1, beam_power=1000, scan_speed=1, dwell_time=1)
slice_settings = SlicingSettings(layer_height=0.1, outer_offset=0.0, contour_layers=0, contour_offset=0.0, contour_infill_offset=0.0)

infill_settings1 = ScanSettings(spot_size=1, beam_power=540, scan_speed=1800000, dwell_time=83333)
part1 = Part(
        mesh=mesh1, infill_setting=infill_settings1, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part1 = slice_part(part1)

infill_settings2 = ScanSettings(spot_size=1, beam_power=600, scan_speed=1800000, dwell_time=83333)
part2 = Part(
        mesh=mesh2, infill_setting=infill_settings2, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part2 = slice_part(part2)

infill_settings3 = ScanSettings(spot_size=1, beam_power=660, scan_speed=2200000, dwell_time=83333)
part3 = Part(
        mesh=mesh3, infill_setting=infill_settings3, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part3 = slice_part(part3)

infill_settings4 = ScanSettings(spot_size=1, beam_power=720, scan_speed=2600000, dwell_time=83333)
part4 = Part(
        mesh=mesh4, infill_setting=infill_settings4, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part4 = slice_part(part4)

infill_settings5 = ScanSettings(spot_size=1, beam_power=720, scan_speed=3000000, dwell_time=83333)
part5 = Part(
        mesh=mesh5, infill_setting=infill_settings5, infill_strategy="line_snake", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part5 = slice_part(part5)

infill_settings6 = ScanSettings(spot_size=1, beam_power=540, scan_speed=1, dwell_time=83333)
part6 = Part(
        mesh=mesh6, infill_setting=infill_settings6, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part6 = slice_part(part6)

infill_settings7 = ScanSettings(spot_size=1, beam_power=600, scan_speed=1, dwell_time=83333)
part7 = Part(
        mesh=mesh7, infill_setting=infill_settings7, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part7 = slice_part(part7)

infill_settings8 = ScanSettings(spot_size=1, beam_power=600, scan_speed=1, dwell_time=75000)
part8 = Part(
        mesh=mesh8, infill_setting=infill_settings8, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part8 = slice_part(part8)

infill_settings9 = ScanSettings(spot_size=1, beam_power=660, scan_speed=1, dwell_time=68181)
part9 = Part(
        mesh=mesh9, infill_setting=infill_settings9, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part9 = slice_part(part9)

infill_settings10 = ScanSettings(spot_size=1, beam_power=720, scan_speed=1, dwell_time=50000)
part10 = Part(
        mesh=mesh10, infill_setting=infill_settings10, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part10 = slice_part(part10)

infill_settings11 = ScanSettings(spot_size=1, beam_power=740, scan_speed=1, dwell_time=48648)
part11 = Part(
        mesh=mesh11, infill_setting=infill_settings11, infill_strategy="point_random", 
        contour_setting=contour_settings, contour_strategy="line_simple", 
        contour_order=0, point_offset=0.1, layer_rotation=90, 
        slicing_settings=slice_settings)
part11 = slice_part(part11)

build = Build(parts=[part1,part2,part3,part4,part5,part6,part7,part8,part9,part10,part11],layer_height=0.1)

#vis_part_layer(part1.layers[0])
generate_build_patterns(build, r"C:\Users\antwi87\Downloads\TMPX_print_20231011\screw_2023_10_12")
