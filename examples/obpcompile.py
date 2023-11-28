import obplib as obp

#path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test20231108\LG_660W-40um_60by60_V.obp"

#elements = obp.read_obp(path)
#out_path = path + "j"
#out_path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test20231108\new_BSE.obpj"
#obp.write_obpj(elements, out_path)

#path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test20231108\LG_660W-40um_60by60_V.obpj"
out_path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test20231108\new_BSE.obp"
in_path = r"C:\Users\antwi87\Downloads\TMPX_print_20231011\cube_test20231108\new_BSE.obpj"
#obpdata = obp.read_obpj(out_path)
#print(obpdata)
#obp.write_obp(obpdata, in_path)
from obpcreator.generate_BSE_scan_pattern import generate_BSE_obp
generate_BSE_obp(
    60, 
    0.05, 
    10000000000,
    660,
    100,
    0.05, 
    10000000000,
    660,
    100,
    out_path)
