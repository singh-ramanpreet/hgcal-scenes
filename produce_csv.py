#!/usr/bin/env python3

import os
import math
import pandas as pd
import sys
sys.path.append("hgcal-scint-tools/performance")

from ec_radiation import fluence
from ec_radiation import dose
from ec_dimensions import r_inner
from ec_dimensions import r_outer, r_scint


def run_sim(
    lumi=3000,
    radscen=3,
    sipmscen=2,
    mip_pe=40,
    pde_ov_base=40.0,
    pde_ov_corr=34.3,
    sipm_area=2.0
):
    """
    lumi -> Integrated luminosity in /fb
    radscen -> Scintillator radiation damage scenario, see code for details
    sipmscen -> 2 or 1: 3 OV HE device
                3: 2 OV HE device at 2e13, -23.5C
                4: 2 OV 10um device at 2.1e12, -30C
                5: 2 OV 15um device at 2.1e12, -30C
                6: 2 OV HE device   at 2.1e12, -30C
    mip_pe -> MIP PE
    pde_ov_base ->
    pde_ov_corr ->
    sipm_area -> sipm area in mm^2, default: "2.0"
    """

    dphi_degrees = 1.25
    dphi = math.radians(dphi_degrees)

    #fixed_point = 1049
    fixed_point = 1554
    r_outer_max = r_outer(21)
    si_boundary_min = r_scint(21)

    # ---------
    def si_boundary_layer(layer):
        return r_scint(layer)

    # ----------
    def generate_cell_data():
        centers = []
        center = fixed_point
        hwidth = math.tan(dphi / 2) * center
        while (center + hwidth*0.5 < float(r_outer_max)):
            centers.append(center)
            center = (1 + math.tan(dphi / 2)) / (1 - math.tan(dphi / 2)) * center
            hwidth = math.tan(dphi / 2) * center

        # inbound
        center = fixed_point
        while (center > si_boundary_min):
            center = (1 - math.tan(dphi / 2)) / (1 + math.tan(dphi / 2)) * center
            hwidth = math.tan(dphi / 2) * center
            if (center + hwidth * 1.5 > r_outer_max): continue
            if (center > si_boundary_min):
                centers.append(center)
        centers=sorted(centers)
        # now, we redo this by determining the average sizes in pairs
        cells=[]
        for i in range(0, len(centers), 2):
            nominal_even = math.tan(dphi / 2) * centers[i] # half width
            nominal_odd = math.tan(dphi / 2) * centers[i+1] # half width
            average_height = (nominal_even + nominal_odd) # average _height_ since no divide by two
            # we keep the inner bound at the nominal position (arbitrary)
            rinner_even = centers[i] - nominal_even
            new_center_even = rinner_even + average_height * 0.5
            width = math.tan(dphi / 2) * new_center_even * 2
            cell_even={
                "center" : new_center_even,
                "ring" : i,
                "inner" : rinner_even,
                "outer" : rinner_even + average_height,
                "width" : width,
                "height" : average_height,
                "area" : width * average_height
            }
            new_center_odd = rinner_even + average_height * 1.5
            cell_odd={
                "center" : new_center_odd,
                "ring" : i + 1,
                "inner" : rinner_even + average_height,
                "outer" : rinner_even + average_height * 2,
                "width" : width,
                "height" : average_height,
                "area" : width * average_height
            }
            cells.append(cell_even)
            cells.append(cell_odd)
        return cells

    cell_geometries = generate_cell_data()

    # ----------
    def cell_area(ring):
        return cell_geometries[ring]["area"]
        # return (math.tan(dphi) * cell_center) ** 2

    # ----------
    def cell_perimeter(ring):
        return 2 * (cell_geometries[ring]["width"] + cell_geometries[ring]["height"])
        # return 4 * math.tan(dphi) * cell_center

    # ----------
    def cell_amplitude(ring):

        cell_area_      = cell_area(ring)
        #cell_perimeter_ = cell_perimeter(ring)
    
        pde_correction = pde_ov_corr / pde_ov_base
        
        sipm_area_correction      = sipm_area / (1.3*1.3)
        cell_area_correction      = math.sqrt(30*30) / math.sqrt(cell_area_)
        #cell_perimeter_correction = math.sqrt( 4*30) / math.sqrt(cell_perimeter_)

        return pde_correction * mip_pe * cell_area_correction * sipm_area_correction
    
    # ----------
    def cell_bounds(ring):
        return [cell_geometries[ring]["inner"],cell_geometries[ring]["outer"]]


    def ring_in_layer(layer, ring):
        if (cell_geometries[ring]["inner"] < si_boundary_layer(layer)): return False
        if (cell_geometries[ring]["outer"] > r_outer(layer)): return False
        return True

    # ----------
    def sipm_noise(layer, ring):
        cell_center=cell_geometries[ring]["center"]
        shaping_time       = 15.0 # ns
        sipm_temp_constant = 1.88 # per 10 degrees
        sipm_temperature   = -30
        sipm_base_noise    = 0
        
        sipm_base_temp     = 23.5
        sipm_base_fluence  = 2e13
        sipm_base_area     = (3.14159*1.4*1.4)

        if sipmscen == 2 or sipmscen == 1:
            sipm_base_noise = 15 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 2V OV
            
        if sipmscen == 3:
            sipm_base_noise = 22 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 3V OV
        
        if sipmscen == 4:
            sipm_base_noise   = math.sqrt(170e6*15e-9) # 10um 170 MHz at -30, 2mm2 device at 2.1e12, 2V OV
            sipm_base_temp    = 30 # -30
            sipm_base_fluence = 2.1e12
            sipm_base_area    = 2
        
        if sipmscen == 5:
            sipm_base_noise   = math.sqrt(370e6*15e-9) # 15um 370 MHz at -30, 2mm2 device at 2.1e12, 2V OV
            sipm_base_temp    = 30 # -30
            sipm_base_fluence = 2.1e12
            sipm_base_area    = 2

        if sipmscen == 51:
            sipm_base_noise   = math.sqrt(15.6e9*15e-9) # 15um 15.6 GHz at -30, 2mm2 device at 2.1e12, 2V OV
            sipm_base_temp    = 30 # -30
            sipm_base_fluence = 5e13
            sipm_base_area    = 2
        
        if sipmscen == 6:
            sipm_base_noise   = math.sqrt(150e6*15e-9) # HE 150 MHz at -30, 2mm2 device at 2.1e12, 2V OV
            sipm_base_temp    = 30 # -30
            sipm_base_fluence = 2.1e12
            sipm_base_area    = 2

        if sipmscen == 1 or sipmscen == 2 or sipmscen == 3:
            sipm_constant = sipm_base_noise * math.sqrt(sipm_area / sipm_base_area) * math.sqrt(shaping_time/50.0) 
        else:
            sipm_constant = sipm_base_noise * math.sqrt(sipm_area / sipm_base_area)
        sipm_constant = sipm_constant   * math.sqrt(math.pow(sipm_temp_constant, (sipm_temperature + sipm_base_temp) / 10))

        return sipm_constant * math.sqrt(fluence(layer, cell_center) / sipm_base_fluence * lumi / 3000)

    # ----------
    def sipm_power(layer, ring):
        cell_center=cell_geometries[ring]["center"]
        sipm_base_current = 200e-6
        sipm_voltage = 62.0 # "HE"
        
        if sipmscen == 4: # 10um
            sipm_voltage=36
        
        if sipmscen == 5: # 15um
            sipm_voltage=36

        sipm_temp_constant = 1.88 # per 10 degrees
        sipm_temperature = -30

        sipm_current = sipm_base_current  * fluence(layer, cell_center) / 2e13 * lumi / 3000
        sipm_current = sipm_current * (sipm_area / (3.14159*1.4*1.4))
        sipm_current = sipm_current * math.pow(sipm_temp_constant, (sipm_temperature + 23.5) / 10)
        
        return sipm_current * sipm_voltage

    # -----------
    def radiation_loss(layer, cell_center):
        d = dose(layer, cell_center) * lumi / 3000

        # in krad/hr
        drate = d/1000/16.7e3

        if radscen == 3:
            # using fit of D=3.6 * R^0.5 (HB Phase 2 TDR)
            dose_constant = 3.6 * pow(drate, 0.5) * 1e6
            return math.exp(-d / dose_constant)
        
        if radscen == 31:
            # using fit of D= 6.0 * R^0.5 (HB Phase 2 TDR)
            dose_constant = 6.0 * pow(drate, 0.5) * 1e6
            return math.exp(-d / dose_constant)

    # -----------------
    board_map = {"layer 9": (18, "J8", "K4"),
                 "layer 10": (18, "J8", "K6"),
                 "layer 11": (18, "J8", "K7"),
                 "layer 12": (18, "J8", "K8"),
                 "layer 13": (13, "C5", "D8", "E8", "G3"),
                 "layer 14": (13, "C5", "D8", "E8", "G5"),
                 "layer 15": (6, "B12", "D8", "E8", "G7"),
                 "layer 16": (6, "B12", "D8", "E8", "G8"),
                 "layer 17": (6, "B12", "D8", "E8", "G8"),
                 "layer 18": (6, "B12", "D8", "E8", "G8"),
                 "layer 19": (0, "A6", "B12", "D8", "E8", "G8"),
                 "layer 20": (0, "A6", "B12", "D8", "E8", "G8"),
                 "layer 21": (0, "A6", "B12", "D8", "E8", "G8"),
                 "layer 22": (0, "A6", "B12", "D8", "E8", "G6")}

    # -------------------
    def tileboards_name(layer, ring):
        expand_board_map = {}
        for key in board_map:
            initial_ring = board_map[key][0]
            boards = {}
            for i in board_map[key][1:]:
                for j in range(initial_ring, initial_ring + int(i[1:])):
                    boards[f"ring {j}"] = i
                initial_ring = initial_ring + int(i[1:])
            expand_board_map[key] = boards.copy()

        layer_key = f"layer {layer}"
        ring_key = f"ring {ring}"
        if layer_key in expand_board_map and ring_key in expand_board_map[layer_key]:
            return expand_board_map[layer_key][ring_key]
        else:
            return "NULL"

    # -------
    def tb_area():
        tb_areas_ = {}
        for key in board_map:
            initial_ring = board_map[key][0]
            for i in board_map[key][1:]:
                area = 0.0
                for j in range(initial_ring, initial_ring + int(i[1:])):
                    area += cell_geometries[j]["area"]
                initial_ring = initial_ring + int(i[1:])
                tb_areas_[i] = area
        return tb_areas_

    tileboards_area = tb_area()

    # --------
    def tb_bounds():
        tb_bounds_ = {}
        for key in board_map:
            initial_ring = board_map[key][0]
            for i in board_map[key][1:]:
                for j in range(initial_ring, initial_ring + int(i[1:])):
                    r1 = cell_geometries[initial_ring]["inner"]
                    r2 = cell_geometries[j]["outer"]
                initial_ring = initial_ring + int(i[1:])
                tb_bounds_[i] = (r1, r2)
        return tb_bounds_

    tileboards_bounds = tb_bounds()

    dframe = {"layer": [], "ring": [], "center (mm)": [], "area (cm2)": [], "mipsig": [], "sipm_noise": [], 
              "S/N": [], "power (mW)": [], "fluence": [], "dose (kRad)": [], "outer": [], "inner": [], 
              "sipm_area": [], "nring": [], "radiation_loss": [], "tileboard_name": [], "tileboard_area": [],
              "tileboard_rin": [], "tileboard_rout": []}
    
    total_sipms = 0
    big_sipms   = 0
    under       = 0

    irange = 9
    total_layers = 22

    for layer in range(irange, total_layers + 1):

        for iring in range(0, len(cell_geometries)):
            if (not ring_in_layer(layer, iring)): continue
            center = cell_geometries[iring]["center"]
            cell_w = cell_geometries[iring]["width"]
            cell_h = cell_geometries[iring]["height"]
            #if (center < 0): continue

            ring_sipms = 2 * 360 / dphi_degrees
            total_sipms += ring_sipms

            signal = cell_amplitude(iring) * radiation_loss(layer, center)
            edges  = cell_bounds(iring)
            if (sipm_area > 3.9):
                big_sipms = big_sipms + 2 * 360 / dphi_degrees

            ring = iring
            ringcode = ""
            
            SN_ratio = signal / sipm_noise(layer, iring)

            tileboard = tileboards_name(layer, iring)
            if tileboard == "NULL":
                print(ring, layer, SN_ratio)
                continue

            dframe["layer"         ].append(layer                                     )
            dframe["ring"          ].append(f"{ringcode}{ring:02d}"                   )
            dframe["center (mm)"   ].append(f"{center:.2f}"                           )
            dframe["area (cm2)"    ].append(f"{(cell_area(iring)/100):.3f}"           )
            dframe["mipsig"        ].append(f"{signal:.3f}"                           )
            dframe["sipm_noise"    ].append(f"{sipm_noise(layer, iring):.3f}"         )
            dframe["S/N"           ].append(f"{SN_ratio:.2f}"                         )
            dframe["power (mW)"    ].append(f"{(sipm_power(layer, iring) * 1000):.3f}")
            dframe["fluence"       ].append(fluence(layer, center) * lumi / 3000      )
            dframe["dose (kRad)"   ].append(dose(layer, center) * lumi / 3000 / 1000  )
            dframe["outer"         ].append(f"{edges[0]:.2f}"                         )
            dframe["inner"         ].append(f"{edges[1]:.2f}"                         )
            dframe["sipm_area"     ].append(sipm_area                                 )
            dframe["nring"         ].append(ring_sipms                                )
            dframe["radiation_loss"].append(radiation_loss(layer, center)             )
            dframe["tileboard_name"].append(tileboard                                 )
            dframe["tileboard_area"].append(f"{tileboards_area[tileboard]:.3f}"       )
            dframe["tileboard_rin" ].append(f"{tileboards_bounds[tileboard][0]:.3f}"  )
            dframe["tileboard_rout"].append(f"{tileboards_bounds[tileboard][1]:.3f}"  )

    return dframe


if __name__ == "__main__":
    dframe_test = run_sim(
        lumi=3000,
        radscen=3,
        sipmscen=5,
        mip_pe=48,
        pde_ov_base=40.0,
        pde_ov_corr=34.3,
        sipm_area=4
    )
    print(pd.DataFrame(dframe_test))

    out_dir = "csv_output"
    os.makedirs(out_dir, exist_ok=True)

    run_for = []
    # jun 19 testbeam result
    run_for.append({"name": "cast", "radscen": 3, "mip": 48, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 2.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 48, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 4.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 48, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 9.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 24, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 2.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 24, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 4.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 24, "pde_base": 40, "pde_corr": 34.5, "sipmscen": 5, "sipm_area": 9.0})
    # jan 20 testbeam result
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 2.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 4.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 9.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 2.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 4.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 5, "sipm_area": 9.0})
    # jan 20 testbeam result + updated Noise
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 2.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 4.0})
    run_for.append({"name": "cast", "radscen": 3, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 9.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 2.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 4.0})
    run_for.append({"name": "mold", "radscen": 3, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 9.0})
    # jan 20 testbeam result + updated Noise + updated Rad Damage
    run_for.append({"name": "cast", "radscen": 31, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 2.0})
    run_for.append({"name": "cast", "radscen": 31, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 4.0})
    run_for.append({"name": "cast", "radscen": 31, "mip": 35, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 9.0})
    run_for.append({"name": "mold", "radscen": 31, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 2.0})
    run_for.append({"name": "mold", "radscen": 31, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 4.0})
    run_for.append({"name": "mold", "radscen": 31, "mip": 25, "pde_base": 36, "pde_corr": 34.9, "sipmscen": 51, "sipm_area": 9.0})


    for i in run_for:
        name = i["name"]
        radscen = i["radscen"]
        mip = i["mip"]
        pde_base = i["pde_base"]
        pde_corr = i["pde_corr"]
        sipmscen = i["sipmscen"]
        sipm_area = i["sipm_area"]

        outFileName = f"{name}_mip_{mip}_pdeC_{pde_corr}_{pde_base}_sipmA_{sipm_area}_rad_{radscen}_sipmN_{sipmscen}.csv"
        print(outFileName)
        dframe = run_sim(
            lumi=3000,
            radscen=radscen,
            sipmscen=sipmscen,
            mip_pe=mip,
            pde_ov_base=pde_base,
            pde_ov_corr=pde_corr,
            sipm_area=sipm_area
        )
        df = pd.DataFrame(dframe)
        df = df[list(dframe.keys())]
        df.to_csv(f"{out_dir}/{outFileName}")
