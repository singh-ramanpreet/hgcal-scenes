#!/usr/bin/env python3

import ROOT
import numpy as np
import pandas as pd
import os
import copy
from pyroot_cms_scripts import CMS_style

ROOT.gROOT.SetBatch(True)


def make_plot(z_axis_param = "S/N", z_axis_title = "S/N at 3000 fb^{-1}",
              z_axis_min = 1, z_axis_max = 9,
              df=None, out_name="test", tpave_text="", out_dir="plot_zr"):

    os.makedirs(out_dir, exist_ok=True)

    canvas = ROOT.TCanvas()

    poly_h2 = ROOT.TH2Poly("hist_z_r_poly", f"; CEH - Layer; R (mm); {z_axis_title}", 8, 23, 960, 2640)

    for i in range(9,23):

        bin_r_outer = df.loc[df["layer"] == i]["outer"].values
        bin_r_inner = df.loc[df["layer"] == i]["inner"].values

        z_axis_vals = df.loc[df["layer"] == i][z_axis_param].values

        #if z_axis_param == "fluence":
        #    z_axis_vals = z_axis_vals / base_fluence

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

    if tpave_text != "":
        tp = ROOT.TPaveText(8.3, 2445, 13.3, 2600)
        tp.SetFillStyle(0)
        tp.SetBorderSize(1)
        tp.SetTextFont(42)
        tp.SetTextSize(0.03)
        tp.AddText(tpave_text)
        tp.Draw()
    canvas.Draw()
    canvas.SaveAs(f"{out_dir}/{out_name}_{z_axis_param.replace('/', '_')}.pdf")


if __name__ == "__main__":

    csv_dir = "csv_output"
    csv_files = os.listdir(csv_dir)

    for inputfile in csv_files:
        if not inputfile.endswith(".csv"): continue
        out_name = inputfile.rstrip(".csv")

        df = pd.read_csv(f"{csv_dir}/{inputfile}", index_col=0)
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
        CMS_style.SetTitleOffset(1.2, "Z")
        CMS_style.cd()

        make_plot(z_axis_param = "S/N", z_axis_title = "S/N at 3000 fb^{-1}",
                  z_axis_min = 1, z_axis_max = 9,
                  df=df, out_name=out_name, tpave_text="", out_dir="plot_zr")

        make_plot(z_axis_param = "mipsig", z_axis_title = "MIP (PE) at 3000 fb^{-1}",
                  z_axis_min = 0, z_axis_max = 70,
                  df=df, out_name=out_name, tpave_text="", out_dir="plot_zr")

        make_plot(z_axis_param = "sipm_noise", z_axis_title = "SIPM Noise (PE) at 3000 fb^{-1}",
                  z_axis_min = 0, z_axis_max = 15,
                  df=df, out_name=out_name, tpave_text="", out_dir="plot_zr")

        make_plot(z_axis_param = "fluence", z_axis_title = "Fluence at 3000 fb^{-1}",
                  z_axis_min = 0, z_axis_max = 5e13,
                  df=df, out_name=out_name, tpave_text="", out_dir="plot_zr")

        make_plot(z_axis_param = "radiation_loss", z_axis_title = "Radiation Damage at 3000 fb^{-1}",
                  z_axis_min = 0.5, z_axis_max = 1.0,
                  df=df, out_name=out_name, tpave_text="", out_dir="plot_zr")
