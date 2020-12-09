import ROOT
from collections import OrderedDict
from copy import deepcopy
import sys

csv_dir = sys.argv[1]

# jun 19 results
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_9.0_rad_3_sipmN_5_sipmAC_default_tileAC_default_sipmAC_default_tileAC_default.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_9.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}

#########################################
# Preference order: read bottom to top. #
#########################################

def fsceneA(csv_map):
    return OrderedDict({
        "cast_4": deepcopy(csv_map["cast_4"]),
        "cast_2": deepcopy(csv_map["cast_2"]),
        "mold_4": deepcopy(csv_map["mold_4"]),
        "mold_2": deepcopy(csv_map["mold_2"])
    })

def fsceneA_with9mm2(csv_map):
    return OrderedDict({
        "cast_9": deepcopy(csv_map["cast_9"]),
        "cast_4": deepcopy(csv_map["cast_4"]),
        "cast_2": deepcopy(csv_map["cast_2"]),
        #"mold_9": deepcopy(csv_map["mold_9"]),
        "mold_4": deepcopy(csv_map["mold_4"]),
        "mold_2": deepcopy(csv_map["mold_2"])
    })

def fsceneB(csv_map):
    return OrderedDict({
        "cast_4": deepcopy(csv_map["cast_4"]),
        "mold_4": deepcopy(csv_map["mold_4"]),
        "cast_2": deepcopy(csv_map["cast_2"]),
        "mold_2": deepcopy(csv_map["mold_2"])
    })

def fsceneB_with9mm2(csv_map):
    return OrderedDict({
        "cast_9": deepcopy(csv_map["cast_9"]),
        #"mold_9": deepcopy(csv_map["mold_9"]),
        "cast_4": deepcopy(csv_map["cast_4"]),
        "mold_4": deepcopy(csv_map["mold_4"]),
        "cast_2": deepcopy(csv_map["cast_2"]),
        "mold_2": deepcopy(csv_map["mold_2"])
    })

sceneA_jun19 = fsceneA(csv_map)
sceneA_jun19_with9mm2 = fsceneA_with9mm2(csv_map)
sceneB_jun19 = fsceneB(csv_map)
sceneB_jun19_with9mm2 = fsceneB_with9mm2(csv_map)


# jan 20 results
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_5_sipmAC_default_tileAC_default.csv"}

sceneA_jan20_0 = fsceneA(csv_map)
sceneA_jan20_0_with9mm2 = fsceneA_with9mm2(csv_map)
sceneB_jan20_0 = fsceneB(csv_map)
sceneB_jan20_0_with9mm2 = fsceneB_with9mm2(csv_map)


# jan 20 results + new noise
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_3_sipmN_51_sipmAC_default_tileAC_default.csv"}

sceneA_jan20_1 = fsceneA(csv_map)
sceneA_jan20_1_with9mm2 = fsceneA_with9mm2(csv_map)
sceneB_jan20_1 = fsceneB(csv_map)
sceneB_jan20_1_with9mm2 = fsceneB_with9mm2(csv_map)


# jan 20 results + new noise + new rad damage
csv_map = {}
csv_map["cast_9"] = {"name": "Cast", "sipm": 9.0, "device": "HDR15", "color": ROOT.kYellow + 2,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_9.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_4.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_35_pdeC_34.9_36_sipmA_2.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_9"] = {"name": "Molded", "sipm": 9.0, "device": "HDR15", "color": ROOT.kBlue + 3,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_9.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_4.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_25_pdeC_34.9_36_sipmA_2.0_rad_31_sipmN_51_sipmAC_default_tileAC_default.csv"}

sceneA_jan20_2 = fsceneA(csv_map)
sceneA_jan20_2_with9mm2 = fsceneA_with9mm2(csv_map)
sceneB_jan20_2 = fsceneB(csv_map)
sceneB_jan20_2_with9mm2 = fsceneB_with9mm2(csv_map)


# DESY Oct2020 results
csv_map = {}
csv_map["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_37_pdeC_30.5_37.5_sipmA_4.0_rad_31_sipmN_51_sipmAC_DESY_Oct2020_tileAC_DESY_Oct2020.csv"}
csv_map["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_37_pdeC_30.5_37.5_sipmA_2.0_rad_31_sipmN_51_sipmAC_DESY_Oct2020_tileAC_DESY_Oct2020.csv"}
csv_map["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_20_pdeC_30.5_37.5_sipmA_4.0_rad_31_sipmN_51_sipmAC_DESY_Oct2020_tileAC_DESY_Oct2020.csv"}
csv_map["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_20_pdeC_30.5_37.5_sipmA_2.0_rad_31_sipmN_51_sipmAC_DESY_Oct2020_tileAC_DESY_Oct2020.csv"}

sceneA_DESY_Oct2020 = fsceneA(csv_map)
sceneB_DESY_Oct2020 = fsceneB(csv_map)
