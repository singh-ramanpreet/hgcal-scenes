#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
sys.path.append("hgcal-scint-tools/performance")

from ec_radiation  import fluence
from ec_radiation  import dose
from ec_dimensions import r_inner
from ec_dimensions import r_outer, r_scint

import os
import math
import pandas as pd


# In[11]:


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

    fixed_point = 1049
    fluence_limit = 5e13

    si_boundary = [
        1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 
        1374, 1304, 1195, 1195, 1147, 1051,  902,  902,
        902,  902,  902,  902,  902,  902,  902,  902,
    ]

    # ---------
    def si_boundary_layer(layer):
        return r_scint(layer)

    # ----------
    def generate_cell_centers(layer):
        centers = []
        center  = fixed_point
        hwidth  = math.tan(dphi / 2) * center

        while (center < r_outer(layer)):
            if (center > si_boundary_layer(layer)):
                centers.append(center)
            else:
                centers.append(-1)
            center = (1 + math.tan(dphi / 2)) / (1 - math.tan(dphi / 2)) * center
            hwidth = math.tan(dphi / 2) * center

        return sorted(centers)

    # ----------
    def cell_area(cell_center):
        return (math.tan(dphi) * cell_center) ** 2
    
    # ----------
    def cell_perimeter(cell_center):
        return 4 * math.tan(dphi) * cell_center
    
    # ----------
    def cell_amplitude(cell_center):
        
        cell_area_      = cell_area(cell_center)
        cell_perimeter_ = cell_perimeter(cell_center)
    
        pde_correction = pde_ov_corr / pde_ov_base
        
        sipm_area_correction      = sipm_area   / (1.3*1.3)
        cell_area_correction      = math.sqrt(30*30) / math.sqrt(cell_area_)
        cell_perimeter_correction = math.sqrt( 4*30) / math.sqrt(cell_perimeter_)

        return pde_correction * mip_pe * cell_area_correction * sipm_area_correction
    
    # ----------
    def cell_bounds(cell_center):
        rv = []
        hwidth = math.tan(dphi / 2) * cell_center
        rv.append(cell_center + hwidth)
        rv.append(cell_center - hwidth)

        return rv

    # ----------
    def sipm_noise(layer, cell_center):
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
    def sipm_power(layer, cell_center):
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


    dframe = {"layer": [], "ring": [], "center (mm)": [], "area (cm2)": [], "mipsig": [], "sipm_noise": [], 
              "S/N": [], "power (mW)": [], "fluence": [], "dose (kRad)": [], "outer": [], "inner": [], 
              "sipm_area": [], "nring": [], "radiation_loss": []}
    
    total_sipms = 0
    big_sipms   = 0
    under       = 0

    irange = 9
    total_layers = 22

    for layer in range(irange, total_layers + 1):

        centers = generate_cell_centers(layer)
        i = -1

        for center in centers:
            i = i + 1
            if (center < 0): continue

            ring_sipms = 2 * 360 / dphi_degrees
            total_sipms += ring_sipms

            signal = cell_amplitude(center) * radiation_loss(layer, center)
            edges  = cell_bounds(center)
            if (sipm_area > 3.9):
                big_sipms = big_sipms + 2 * 360 / dphi_degrees

            ring = i
            ringcode = ""
            
            SN_ratio = signal / sipm_noise(layer, center)

            dframe["layer"         ].append(layer                                     )
            dframe["ring"          ].append(f"{ringcode}{ring:02d}"                   )
            dframe["center (mm)"   ].append(f"{center:.2f}"                           )
            dframe["area (cm2)"    ].append(f"{(cell_area(center)/100):.3f}"          )
            dframe["mipsig"        ].append(f"{signal:.3f}"                           )
            dframe["sipm_noise"    ].append(f"{sipm_noise(layer, center):.3f}"        )
            dframe["S/N"           ].append(f"{SN_ratio:.2f}"                         )
            dframe["power (mW)"    ].append(f"{(sipm_power(layer,center) * 1000):.3f}")
            dframe["fluence"       ].append(fluence(layer, center) * lumi / 3000      )
            dframe["dose (kRad)"   ].append(dose(layer, center) * lumi / 3000 / 1000  )
            dframe["outer"         ].append(f"{edges[0]:.2f}"                         )
            dframe["inner"         ].append(f"{edges[1]:.2f}"                         )
            dframe["sipm_area"     ].append(sipm_area                                 )
            dframe["nring"         ].append(ring_sipms                                )
            dframe["radiation_loss"].append(radiation_loss(layer, center)             )
    
    return dframe


# In[12]:


dframe = run_sim(
                lumi=3000,
                radscen=3,
                sipmscen=5,
                mip_pe=48,
                pde_ov_base=40.0,
                pde_ov_corr=34.5,
                sipm_area=4
            )
print(pd.DataFrame(dframe))


# In[4]:


#out_dir = "csv_output"
#os.makedirs(out_dir, exist_ok=True)

#radiation_scene = 3

#for mip in [48, 38, 24]:
#    
#    pde_base = 40.0
#        
#    for pde_corr in [14.4, 18.37, 34.5]:
#        
#        if pde_corr == 18.37:
#            sipmscen = 6 # HE
#            
#        if pde_corr == 14.4:
#            sipmscen = 4 # 10um
#            
#        if pde_corr == 34.5:
#            sipmscen = 5 # 15um
#        
#        for sipm_area in [2.0, 4.0, 9.0]:
#            
#            outFileName = f"mip_{mip}_pde_ratio_{pde_corr}_{pde_base}_sipm_area_{sipm_area}.csv"
#            print(outFileName)
#            dframe = run_sim(
#                lumi=3000,
#                radscen=radiation_scene,
#                sipmscen=sipmscen,
#                mip_pe=mip,
#                pde_ov_base=pde_base,
#                pde_ov_corr=pde_corr,
#                sipm_area=sipm_area
#            )
#            df = pd.DataFrame(dframe)
#            df = df[list(dframe.keys())]
#            df.to_csv(f"{out_dir}/{outFileName}")


# In[ ]:




