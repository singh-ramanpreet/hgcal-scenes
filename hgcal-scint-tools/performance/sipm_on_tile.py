#!/usr/bin/python3

from ec_radiation import fluence;
from ec_radiation import dose;
from ec_dimensions import r_inner;
from ec_dimensions import r_outer, r_scint;
from math import pow, sqrt, exp,log, tan;
import sys;
import argparse;

parser=argparse.ArgumentParser(description="Determine performance for SiPM-on-tile technology")
parser.add_argument('--lumi',type=int,default=3000,help='Integrated luminosity in /fb (default: 3000)')
parser.add_argument('--radscen',type=int,default=10,help='Scintillator radiation damage scenario, see code for details (default: 10)')
parser.add_argument('--permm2',action='store_true',help='Use exactly 1mm2 SiPM everywhere to get signal per mm2 of SiPM')
parser.add_argument('--allceh',action='store_true',help='Determine values for whole of CE-H volume, not just the expected region for scintillator')
parser.add_argument('--unitysignal',action='store_true',help='Make signal just 1 PE')
#parser.add_argument('--allbig',action='store_true',help='Use 1.25 cells everywhere')
parser.add_argument('--sipmscen',type=int,default=8,help='SiPM noise scenario, see code for details (default:8)')
#parser.add_argument('--bhlayers',type=int,default=12,help='Number of thick-absorber layers (default: 12)')

#fixed_point=2000
#fixed_point=912
fixed_point=1554
fixed_ring=18
fluence_limit=5e13

r_outer_max=r_outer(21)
si_boundary_min=r_scint(21)

args=parser.parse_args()

lumi=args.lumi
radscen=args.radscen

def cell_30():
        return 24 # same delta-phi everywhere.

def deltaphi():
    return 30.0/cell_30()*3.1415926/180

def sipm_area(layer,center):
    if args.permm2: return 1
    if (layer<=13): return 4
    if (layer==9): return 4
    if (layer==10): return 4
    if (layer==11 and center<1700): return 4
    if (layer==12 and center<1700): return 4         
    if (layer<=8): return 4 # mm2
    if (layer==9 and center<1460): return 4 # mm2
    if (layer==10 and center<1410): return 4 # mm2
    if (layer==11 and center<1330): return 4 # mm2
    if (layer==12 and center<1270): return 4 # mm2
    if (layer==13 and center<1350): return 4 # mm2
    if (layer==14 and center<1350): return 4 # mm2
    return 2.0 # mm2


def si_boundary_layer(layer):
    if args.allceh: return r_inner(layer)
    return r_scint(layer)

def generate_cell_data():
    centers=[]
    # outbound
    center=fixed_point
    ring=fixed_ring
    hwidth=tan(deltaphi()/2)*center
#    while (center<r_outer(layer)):
    while (center+hwidth*0.5<float(r_outer_max)):
        centers.append(center)
        center=(1+tan(deltaphi()/2))*center/(1-tan(deltaphi()/2))
        hwidth=tan(deltaphi()/2)*center  
        ring=ring+1      
    # inbound 
    center=fixed_point
    ring=fixed_ring
    n30=cell_30()
    while (center>si_boundary_min):
        center=(1-tan(deltaphi()/2))*center/(1+tan(deltaphi()/2))
        hwidth=tan(deltaphi()/2)*center 
        ring=ring-1       
        if (center+hwidth*1.5>r_outer_max): continue
        if (center>si_boundary_min): 
           centers.append(center)
    centers=sorted(centers)
    cells=[]
    # now, we redo this by determining the average sizes in pairs
    for i in range(0,len(centers),2):
        nominal_even=tan(deltaphi()/2)*centers[i] # half width
        nominal_odd=tan(deltaphi()/2)*centers[i+1] # half width
        average_height=(nominal_even+nominal_odd) # average _height_ since no divide by two
        # we keep the inner bound at the nominal position (arbitrary)
        rinner_even=centers[i]-nominal_even
        new_center_even=rinner_even+average_height*0.5
        width=tan(deltaphi()/2)*new_center_even*2
        cell_even={'center' : new_center_even,
                   'ring' : i,
                   'inner' : rinner_even,
                   'outer' : rinner_even+average_height,
                   'width' : width,
                   'height' : average_height,
                   'area' : width*average_height
                   }
        new_center_odd=rinner_even+average_height*1.5
        cell_odd={'center' : new_center_odd,
                   'ring' : i+1,
                   'inner' : rinner_even+average_height,
                   'outer' : rinner_even+average_height*2,
                   'width' : width,
                   'height' : average_height,
                   'area' : width*average_height
                   }
        cells.append(cell_even)
        cells.append(cell_odd)
    return cells

cell_geometries=generate_cell_data()

def ring_in_layer(layer,ring):
    if (cell_geometries[ring]['inner']<si_boundary_layer(layer)): return False
    if (cell_geometries[ring]['outer']>r_outer(layer)): return False
    return True
        
def cell_bounds(ring):
    return [cell_geometries[ring]['inner'],cell_geometries[ring]['outer']]

def cell_area(ring):
    return cell_geometries[ring]['area']

def cell_amplitude(layer,ring):
#    return 20*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area/1.0
#    return 18*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/1.0
    if args.unitysignal: return 1
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for HDR2-10um ratio at 2V OV
    if (args.sipmscen==4):
        return 13.0/40.0*35*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for HDR2-15um ratio at 2V OV
    if (args.sipmscen==5):
        return 30.0/40.0*35*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    # based on July 2019 J. Freeman result from testbeam of 59 PE/MIP for a 3x3 cm tile of EJ208 with "small hole" ESR foil, correct for HDR2-15um ratio at 2V OV
    if (args.sipmscen==7):
        return 30.0/40.0*59*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    # based on "averaged" July 2019 J. Freeman result from testbeam of 48 PE/MIP for a 3x3 cm tile of EJ208 with "reasonable hole" ESR foil, correct for HDR2-15um ratio at 2V OV
    if (args.sipmscen==8):
        return 30.0/40.0*48*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)

    # based on "averaged" July 2019 J. Freeman result from testbeam of 48 PE/MIP for a 3x3 cm tile of EJ208 with "reasonable hole" ESR foil, correct for W9_S ratio at 2V OV
    if (args.sipmscen==20):
        return 27.0/40.0*48*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)

    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for "overall PDE" ratio at 2V OV (30 agreed as reference PDE from J. Virdee)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for "overall PDE" ratio at 3V OV
    if (args.sipmscen==3):
        return 28.5/40.0*35*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for "overall PDE" ratio at 2V OV (30 agreed as reference PDE from J. Virdee)
    if (args.sipmscen==2):
        return 20.5/30.0*35*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil
    if (args.sipmscen==1):
        return 35*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
#    return 14*sqrt(30*30)/sqrt(cell_area(ring))*sipm_area(layer,ring)/(1.3*1.3)
    

    return 0

def radiation_loss(layer,cell_center):
    d=dose(layer,cell_center)*lumi/3000
    # in krad/hr
    drate=d/1000/16.7e3
    if radscen==0:
        # using fit of D=1.57 * R^0.538
        dose_constant=1.57*pow(drate,0.538)*1e6
        return exp(-d/dose_constant)
    if radscen==4:
        # using fit of D=4 * R^0.575
        dose_constant=4*pow(drate,0.575)*1e6
        return exp(-d/dose_constant)
    if radscen==5:
        # using fit of D=5 * R^0.675
        dose_constant=5*pow(drate,0.675)*1e6
        return exp(-d/dose_constant)
    if radscen==51: 
        # using fit of D=5 * R^0.675 and a bonus of 15% for SiPM-on-tile
        dose_constant=5*pow(drate,0.675)*1e6
        return exp(-d/dose_constant)    
    if radscen==3: 
        # using fit of D=3.6 * R^0.5 (HB Phase 2 TDR)
        dose_constant=3.6*pow(drate,0.5)*1e6
        return exp(-d/dose_constant)
    if radscen==6:
        # using fit of D=8.5 * R^0.78
        dose_constant=8.5*pow(drate,0.78)*1e6
        return exp(-d/dose_constant)
    if radscen==9:
        # using fit of D=6.0 * R^0.35
        dose_constant=6.0*pow(drate,0.35)*1e6
        return exp(-d/dose_constant)
    if radscen==10:
        # rough guess based on single cold point and sqrt(rate)
        dose_constant=6.0*pow(drate,0.5)*1e6
        return exp(-d/dose_constant)

    
def sipm_noise(layer,ring):
    cell_center=cell_geometries[ring]['center']
    shaping_time=15.0 # ns
    sipm_temp_constant=1.88 # per 10 degrees
    sipm_temperature=-30
    sipm_base_noise=0
    sipm_base_temp=23.5
    sipm_base_fluence=2e13
    sipm_base_area=(3.14159*1.4*1.4)
    if (args.sipmscen==2 or args.sipmscen==1):
        sipm_base_noise=15 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 2V OV
    if (args.sipmscen==3):
        sipm_base_noise=22 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 3V OV
    if (args.sipmscen==4):
        sipm_base_noise=sqrt(250e6*50e-9) # 10um 220 MHz at -30, 2mm2 device at 2.1e12, 2V OV
        sipm_base_temp=30 # -30
        sipm_base_fluence=2.1e12
        sipm_base_area=2
    if (args.sipmscen==5 or args.sipmscen==7 or args.sipmscen==8):
        sipm_base_noise=sqrt(350e6*50e-9) # 15um 270 MHz at -30, 2mm2 device at 2.1e12, 2V OV
#        sipm_base_noise=sqrt(270e6*50e-9) # 15um 270 MHz at -30, 2mm2 device at 2.1e12, 2V OV
        sipm_base_temp=30 # -30
        sipm_base_fluence=2.1e12
        sipm_base_area=2
    if (args.sipmscen==20):
        #W9C FBK at 2V OverVoltage
        sipm_base_noise=sqrt(2e10*50e-9) # 15um 270 MHz at -30, 2mm2 device at 2.1e12, 2V OV
#        sipm_base_noise=sqrt(270e6*50e-9) # 15um 270 MHz at -30, 2mm2 device at 2.1e12, 2V OV
        sipm_base_temp=30 # -30
        sipm_base_fluence=1e13
        sipm_base_area=9
            
    sipm_constant=sipm_base_noise*sqrt(shaping_time/50.0)*sqrt(sipm_area(layer,ring)/sipm_base_area)*sqrt(pow(1.88,(sipm_temperature+sipm_base_temp)/10))
    return sipm_constant*sqrt(fluence(layer,cell_center)/sipm_base_fluence*lumi/3000)

def sipm_power(layer,ring):
    cell_center=cell_geometries[ring]['center']
    sipm_base_current=200e-6
    sipm_voltage=62.0 # "HE"

    if (args.sipmscen==4): # 10um
        sipm_voltage=36
    if (args.sipmscen==5): # 15um
        sipm_voltage=36

    sipm_temp_constant=1.88 # per 10 degrees
    sipm_temperature=-30

    sipm_noise_current=sipm_base_current*fluence(layer,cell_center)/2e13*lumi/3000
    sipm_noise_current=sipm_noise_current*(sipm_area(layer,ring)/(3.14159*1.4*1.4))
    sipm_noise_current=sipm_noise_current*pow(sipm_temp_constant,(sipm_temperature+23.5)/10)
    return sipm_noise_current*sipm_voltage

total_sipms=0;
big_sipms=0;
under=0;
print("# ",args)
print("#layer,ring,center[mm],area[cm2],mipsig,sipm_noise,  S/N,power[mW],fluence,dose[kRad],outer,inner,sipm_area,nring,height,width(center)")
if args.allceh: irange=1
else: irange=9
for layer in range(irange,22+1):
    for iring in range(0,len(cell_geometries)):
        if (not ring_in_layer(layer,iring)): continue
        center=cell_geometries[iring]['center']
        cell_w=cell_geometries[iring]['width']
        cell_h=cell_geometries[iring]['height']
                
#        if (fluence(layer,center)>fluence_limit): continue
        ring_sipms=cell_30()*360/30*2
        total_sipms+=ring_sipms
        signal=cell_amplitude(layer,iring)*radiation_loss(layer,center)
        edges=cell_bounds(iring)
        if (sipm_area(layer,iring)>3.9): big_sipms=big_sipms+cell_30()*360/30*2
        ringcode=""
        if args.unitysignal:
            print("%2d,     %s%02d, %7.2f,  %5.2f,    %5.3f,  %5.1f,    %5.2f,  %5.2f,  %4.1e,  %5.1f,   %4.0f, %4.0f,  %5.1f, %5d, %5.2f, %5.2f"%(layer, ringcode, iring, center, cell_area(iring)/100, signal, sipm_noise(layer,iring),signal/sipm_noise(layer,iring),sipm_power(layer,iring)*1000,fluence(layer,center)*lumi/3000,dose(layer,center)*lumi/3000/1000,edges[0],edges[1],sipm_area(layer,center),ring_sipms,cell_w,cell_h))
        else:
            print("%2d,     %s%02d, %7.2f,  %5.2f,    %5.1f,  %5.1f,    %5.2f,  %5.2f,  %4.1e,  %5.1f,   %4.0f, %4.0f,  %5.1f, %5d, %5.2f, %5.2f"%(layer, ringcode, iring, center, cell_area(iring)/100, signal, sipm_noise(layer,iring),signal/sipm_noise(layer,iring),sipm_power(layer,iring)*1000,fluence(layer,center)*lumi/3000,dose(layer,center)*lumi/3000/1000,edges[0],edges[1],sipm_area(layer,center),ring_sipms,cell_w,cell_h))

print('# sipms=%d big-sipms=%d'%(total_sipms,big_sipms))

