#!/usr/bin/env python3

import ROOT
import pandas as pd
from collections import OrderedDict

ROOT.gROOT.SetBatch(True)

csv_dir = "csv_output"
# extract geometry from any csv
temp_pd = pd.read_csv(f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5.csv")
tileboard_names = list(set(temp_pd["tileboard_name"]))
boards = temp_pd[["layer", "ring", "tileboard_name", "tileboard_rin", "tileboard_rout", "tileboard_area"]]


scene = OrderedDict()
scene["cast_4"] = {"name": "Cast", "sipm": 4.0, "device": "HDR15", "color": ROOT.kYellow + 1,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5.csv"}
scene["cast_2"] = {"name": "Cast", "sipm": 2.0, "device": "HDR15", "color": ROOT.kYellow,
                   "file": f"{csv_dir}/cast_mip_48_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5.csv"}
scene["mold_4"] = {"name": "Molded", "sipm": 4.0, "device": "HDR15", "color": ROOT.kBlue + 2,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_4.0_rad_3_sipmN_5.csv"}
scene["mold_2"] = {"name": "Molded", "sipm": 2.0, "device": "HDR15", "color": ROOT.kBlue,
                   "file": f"{csv_dir}/mold_mip_24_pdeC_34.5_40_sipmA_2.0_rad_3_sipmN_5.csv"}

def make_scene(scene=scene, sn_cut=5.0, out_name="scene"):
    for s in scene:
        df = pd.read_csv(scene[s]["file"], index_col=0)
        df["full_tb"] = False
        df["partial_tb"] = False
        for layer in range(9, 23):
            for tb in tileboard_names:
                location = (df["layer"] == layer) & (df["tileboard_name"] == tb)
                df.loc[location, "full_tb"] = all(df.loc[location]["S/N"] >= sn_cut)
                df.loc[location, "partial_tb"] = (df.loc[location]["S/N"] >= sn_cut)
        scene[s]["loaded_pd"] = df

    mipsig = []
    noise = []
    sn_ratio = []
    cell_rin = []
    cell_rout = []
    cell_area = []
    scint = []
    sipmA = []
    color = []
    full_tb = []
    partial_tb = []

    for layer, ring in zip(boards["layer"], boards["ring"]):
        for i, s in enumerate(scene):
            df = scene[s]["loaded_pd"]
            location = (df["layer"] == layer) & (df["ring"] == ring )

            mipsig_ = df.loc[location]["mipsig"].values[0]
            noise_ = df.loc[location]["sipm_noise"].values[0]
            sn_ratio_ = df.loc[location]["S/N"].values[0]
            cell_rin_ = df.loc[location]["inner"].values[0]
            cell_rout_ = df.loc[location]["outer"].values[0]
            cell_area_ = df.loc[location]["area (cm2)"].values[0]
            sipmA_ = df.loc[location]["sipm_area"].values[0]
            color_ = scene[s]["color"]
            full_tb_ = df.loc[location]["full_tb"].values[0]
            partial_tb_ = df.loc[location]["partial_tb"].values[0]

            if i == 0:
                mipsig.append(mipsig_)
                noise.append(noise_)
                sn_ratio.append(sn_ratio_)
                cell_rin.append(cell_rin_)
                cell_rout.append(cell_rout_)
                cell_area.append(cell_area_)
                sipmA.append(sipmA_)
                scint.append(s)
                color.append(color_)
                full_tb.append(full_tb_)
                partial_tb.append(partial_tb_)

            if i > 0 and full_tb_ and sn_ratio_ >= sn_cut:
                mipsig[-1] = mipsig_
                noise[-1] = noise_
                sn_ratio[-1] = sn_ratio_
                cell_rin[-1] = cell_rin_
                cell_rout[-1] = cell_rout_
                cell_area[-1] = cell_area_
                sipmA[-1] = sipmA_
                scint[-1] = s
                color[-1] = color_
                full_tb[-1] = full_tb_
                partial_tb[-1] = partial_tb_

    boards["mipsig"] = mipsig
    boards["noise"] = noise
    boards["sn_ratio"] = sn_ratio
    boards["cell_rin"] = cell_rin
    boards["cell_rout"] = cell_rout
    boards["cell_area"] = cell_area
    boards["sipmA"] = sipmA
    boards["scint"] = scint
    boards["color"] = color
    boards["full_tb"] = full_tb
    boards["partial_tb"] = partial_tb

    canvas = ROOT.TCanvas("", "", 800, 600)
    canvas.SetRightMargin(0.3)

    detector_frame = canvas.DrawFrame(8, 850, 23, 2720,  "; CEH - Layer; R (mm)")
    detector_frame.Draw()

    legend = ROOT.TLegend(0.71, 1 - len(scene) * 0.18, 0.97, 0.9)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)

    for s in scene:
        # total area in scene
        scene[s]["total_area"] = sum(boards.loc[boards["scint"] == s]["cell_area"].values) * 2 * 288 / 1e4
        scene[s]["sipms_count"] = len(boards.loc[(boards["sipmA"] == scene[s]["sipm"]) 
                                                 & (boards["scint"] == s)]["sipmA"].values) * 2 * 288 

        tt1 = f"#splitline{{Scint: {scene[s]['name']}}}{{Device: {scene[s]['device']} {scene[s]['sipm']}mm^{{2}}}}"
        tt2 = f"#splitline{{Scint Area: {scene[s]['total_area']:.2f}m^{{2}}}}{{SiPMs: {scene[s]['sipms_count']:d}}}"
        scene[s]["tbox"] = ROOT.TBox()
        scene[s]["tbox"].SetFillColor(scene[s]["color"])
        legend.AddEntry(scene[s]["tbox"], tt1, "f")
        legend.AddEntry("", tt2, "")


    border_tboxes = []
    full_tboxes = []
    partial_tboxes = []
    for layer in range(9, 23):
            for tb in tileboard_names:
                location = (boards["layer"] == layer) & (boards["tileboard_name"] == tb)
                if len(boards[location]) == 0: continue
                r1 = boards[location]["tileboard_rin"].values[0]
                r2 = boards[location]["tileboard_rout"].values[0]
                if boards[location]["full_tb"].values[0]:
                    color = boards[location]["color"].values[0]
                else:
                    color = ROOT.kRed
                full_tboxes.append(ROOT.TBox(layer - 0.5, r1, layer + 0.5, r2))
                full_tboxes[-1].SetFillColor(int(color))

                border_tboxes.append(ROOT.TBox(layer - 0.5, r1, layer + 0.5, r2))
                border_tboxes[-1].SetFillColor(0)
                border_tboxes[-1].SetFillStyle(0)

                for i in range(len(boards[location]["partial_tb"].values)):
                    if boards[location]["partial_tb"].values[i] and not boards[location]["full_tb"].values[0]:
                        r1 = boards[location]["cell_rin"].values[i]
                        r2 = boards[location]["cell_rout"].values[i]
                        color = boards[location]["color"].values[i]
                        partial_tboxes.append(ROOT.TBox(layer - 0.5, r1, layer + 0.5, r2))
                        partial_tboxes[-1].SetFillColor(int(color))


    for tbox in full_tboxes:
        tbox.Draw()

    for tbox in partial_tboxes:
        tbox.Draw()

    for tbox in border_tboxes:
        tbox.Draw("l")

    legend.Draw()    
    canvas.Draw()
    canvas.SaveAs(f"{out_name}.pdf")


if __name__ == "__main__":
    make_scene()
