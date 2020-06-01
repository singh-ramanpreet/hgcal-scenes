import ROOT
from collections import OrderedDict
from copy import deepcopy

csv_dir = "csv_output"

# jun 19 results
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_9.0_rad_3_sipmN_5.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_9.0_rad_3_sipmN_5.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5.csv"}

sceneA_jun19 = OrderedDict({
    "cast_4": deepcopy(csv_map["cast_4"]),
    "cast_2": deepcopy(csv_map["cast_2"]),
    "mold_4": deepcopy(csv_map["mold_4"]),
    "mold_2": deepcopy(csv_map["mold_2"])
})

# jan 20 results
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_5.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_5.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_5.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_5.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_5.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_5.csv"}

sceneA_jan20_0 = OrderedDict({
    "cast_4": deepcopy(csv_map["cast_4"]),
    "cast_2": deepcopy(csv_map["cast_2"]),
    "mold_4": deepcopy(csv_map["mold_4"]),
    "mold_2": deepcopy(csv_map["mold_2"])
})


# jan 20 results + new noise
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_51.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_51.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_51.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_51.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_51.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_51.csv"}

sceneA_jan20_1 = OrderedDict({
    "cast_4": deepcopy(csv_map["cast_4"]),
    "cast_2": deepcopy(csv_map["cast_2"]),
    "mold_4": deepcopy(csv_map["mold_4"]),
    "mold_2": deepcopy(csv_map["mold_2"])
})


# jan 20 results + new noise + new rad damage
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_31_sipmN_51.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_31_sipmN_51.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_31_sipmN_51.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_31_sipmN_51.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_31_sipmN_51.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_31_sipmN_51.csv"}

sceneA_jan20_full = OrderedDict({
    "cast_4": deepcopy(csv_map["cast_4"]),
    "cast_2": deepcopy(csv_map["cast_2"]),
    "mold_4": deepcopy(csv_map["mold_4"]),
    "mold_2": deepcopy(csv_map["mold_2"])
})
