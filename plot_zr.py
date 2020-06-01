#!/usr/bin/env python3

import ROOT
import numpy as np
import pandas as pd
import copy
from pyroot_cms_scripts import CMS_style

set_defaults = """
csv_dir = "csv_output"
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"
z_axis_param = "S/N"
z_axis_title = "S/N at 3000 fb^{-1}"
z_axis_min = 1
z_axis_max = 9
base_fluence = 2.1e12
"""

plot = """
if sipm_device == "hdr15":
    pde_ratio="34.5_40.0"
    sipm_device_name = "HDR (15#mum)"
    
if scint_mip == 48:
    scint_type = "Cast (Individual)"

inputfile = f"{csv_dir}/mip_{scint_mip}_pde_ratio_{pde_ratio}_sipm_area_{sipm_area}.csv"

NRGBs = 7
NCont = 100
stops = np.array([0.00, 0.25, 0.35, 0.55, 0.63, 0.75, 1.00])
red   = np.array([0.51, 1.00, 0.87, 0.00, 0.00, 0.00, 0.00])
green = np.array([0.00, 0.20, 1.00, 1.00, 1.00, 1.00, 0.20])
blue  = np.array([0.00, 0.00, 0.12, 0.00, 0.60, 1.00, 0.51])
ROOT.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
ROOT.gStyle.SetNumberContours(NCont)

CMS_style.SetCanvasDefW(700)
CMS_style.SetPadRightMargin(0.14)
CMS_style.SetTitleSize(0.04, "XYZ")
CMS_style.SetLabelSize(0.04, "XYZ")
CMS_style.SetTitleOffset(1.7, "Y")
CMS_style.SetTitleOffset(1.2, "X")
CMS_style.cd()

canvas = ROOT.TCanvas()
    
poly_h2 = ROOT.TH2Poly("hist_z_r_poly", "; CEH - Layer; R (mm); %s" % z_axis_title, 8, 23, 960, 2640)
    
df = pd.read_csv(inputfile, index_col=0)

for i in range(9,23):

    bin_r_outer = df.loc[df["layer"] == i]["outer"].values
    bin_r_inner = df.loc[df["layer"] == i]["inner"].values

    z_axis_vals = df.loc[df["layer"] == i][z_axis_param].values

    if z_axis_param == "fluence":
        z_axis_vals = z_axis_vals / base_fluence

    for j in range(len(bin_r_outer)):

        rbin_a = bin_r_inner[j]
        rbin_b = bin_r_outer[j]
        z_val  = z_axis_vals[j]

        x = poly_h2.AddBin(i - 0.5, rbin_a, i + 0.5, rbin_b)
        poly_h2.SetBinContent(x , z_val)

poly_h2.SetStats(0)
poly_h2.SetMinimum(z_axis_min)
poly_h2.SetMaximum(z_axis_max)
poly_h2.Draw("colz")

tp = ROOT.TPaveText(8.3, 2445, 13.3, 2600)
tp.SetFillStyle(0)
tp.SetBorderSize(1)
tp.SetTextFont(42)
tp.SetTextSize(0.03)

tp.AddText(sipm_device_name + " - %smm^{2}" % sipm_area)
tp.AddText(scint_type)

tp.Draw()
canvas.Draw()
"""

exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"
exec(plot)
#canvas.Print(f"plot_output/sn_hdr15_2p0_mip48.pdf")


exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "4.0"
exec(plot)
#canvas.Print(f"plot_output/sn_hdr15_4p0_mip48.pdf")


exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"

z_axis_param = "radiation_loss"
z_axis_title = "Radiation Damage at 3000 fb^{-1}"
z_axis_min = 0.5
z_axis_max = 1.0

CMS_style.SetTitleOffset(1.2, "Z")
exec(plot.replace("tp.Draw()", "#tp.Draw()"))
#canvas.Print(f"plot_output/rad_loss.pdf")


exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"

z_axis_param = "fluence"
base_fluence = 2.1e12
z_axis_title = "fluence/base_fluence at 3000 fb^{-1}"
z_axis_min = 0
z_axis_max = 25

exec(plot.replace("tp.Draw()", "#tp.Draw()"))
tp.Clear()
tp.AddText("base_fluence = 2.1e12")
tp.Draw()
canvas.Draw()
#canvas.Print(f"plot_output/fluence_ratio.pdf")


exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"

z_axis_param = "sipm_noise"
z_axis_title = "SIPM Noise (PE) at 3000 fb^{-1}"
z_axis_min = 0
z_axis_max = 15

exec(plot.replace("tp.Draw()", "#tp.Draw()"))
#canvas.Print(f"plot_output/sipm_noise_ratio.pdf")


exec(set_defaults)
scint_mip = 48
sipm_device = "hdr15"
sipm_area = "2.0"

z_axis_param = "mipsig"
z_axis_title = "MIP (PE) at 3000 fb^{-1}"
z_axis_min = 0
z_axis_max = 70

exec(plot.replace("tp.Draw()", "#tp.Draw()"))
#canvas.Print(f"plot_output/mipsig_ratio.pdf")
