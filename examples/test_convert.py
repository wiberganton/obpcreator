import obplib as obp

obp_element = obp.read_obp(r"C:\Users\antwi87\Downloads\LG_660W-40um_60by60_V.obp")
obp.write_obpj(obp_element, r"C:\Users\antwi87\Downloads\LG_660W-40um_60by60_V.obpj")