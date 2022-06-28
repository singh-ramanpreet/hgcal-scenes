#!/usr/bin/python3

from ec_radiation import fluence;
from ec_radiation import dose;
from ec_dimensions import r_inner;
from ec_dimensions import r_outer;
from math import pow, sqrt, exp,log, tan;
import sys;
import argparse;

parser=argparse.ArgumentParser(description="Determine performance for SiPM-on-tile technology")
parser.add_argument('--lumi',type=int,default=3000,help='Integrated luminosity in /fb (default: 3000)')
parser.add_argument('--radscen',type=int,default=3,help='Scintillator radiation damage scenario, see code for details (default: 3)')
parser.add_argument('--permm2',action='store_true',help='Use exactly 1mm2 SiPM everywhere to get signal per mm2 of SiPM')
parser.add_argument('--allceh',action='store_true',help='Determine values for whole of CE-H volume, not just the expected region for scintillator')
parser.add_argument('--unitysignal',action='store_true',help='Make signal just 1 PE')
parser.add_argument('--sipmscen',type=int,default=1,help='SiPM noise scenario, dee code for details (default:1)')

#fixed_point=2000
fixed_point=912

#si_boundary=[
#    1500,1500,1500,1500,
#    1500,1500,1500,1500,
#    1374,1304,1195,1195,
#    1062,1062,922,922,
#    922,922,922,922,
#    922,922,922,922]

si_boundary=[
     1500,1500,1500,1500,
     1500,1500,1500,1500,
     1374,1304,1195,1195,
     1147,1051,902,902,
     902,902,902,902,
     902,902,902,902]


#si_boundary=[1224,1224,1224,1224,1224,
#             902,902,902,902,
#             902,902,902,902,
#             902,902,902,952]

args=parser.parse_args()

lumi=args.lumi
radscen=args.radscen

def cell_30(layer,center):
#    if (layer>=28+12 and center>1307):
#        return 12
    if (layer<=28+12): # FH
        return 30
    else: return 24

def deltaphi(layer,center):
    return 30.0/cell_30(layer,center)*3.141592/180

def sipm_area(layer,center):
    if args.permm2: return 1
    if (layer<=28+8): return 4 # mm2
    if (layer==28+9 and center<1460): return 4 # mm2
    if (layer==28+10 and center<1410): return 4 # mm2
    if (layer==28+11 and center<1330): return 4 # mm2
    if (layer==28+12 and center<1270): return 4 # mm2
    if (layer==40+1 and center<1270): return 4 # mm2
    if (layer==40+2 and center<1130): return 4 # mm2
    if (layer==40+3 and center<1010): return 4 # mm2
#    if (layer==40+4 and center<1110): return 4 # mm2
#    if (layer==40+5 and center<1110): return 4 # mm2
    #if (layer==40+6 and center<1030): return 4 # mm2    
    #if (layer<=28+12+2 and center<1500): return 1.4*1.4*3.14159 # mm2
    #if (layer<=28+12+5 and center<1300): return 1.4*1.4*3.14159 # mm2
    return 2.0 # mm2


def si_boundary_layer(layer):
    if args.allceh: return r_inner(layer)
    return si_boundary[layer-28-1]
    
def generate_cell_centers(layer):
    centers=[]
    # outbound
    center=fixed_point
    hwidth=tan(deltaphi(layer,center)/2)*center
    while (center<r_outer(layer)):
        if (center>si_boundary_layer(layer)): centers.append(center)
        else: centers.append(-1)
        center=(1+tan(deltaphi(layer,center)/2))*center/(1-tan(deltaphi(layer,center)/2))
        hwidth=tan(deltaphi(layer,center)/2)*center        
    # inbound (generally unused)
    center=fixed_point
    n30=cell_30(layer,center)
    while (center>si_boundary_layer(layer)):        
        acenter=(1-tan(deltaphi(layer,center)/2))*center/(1+tan(deltaphi(layer,center)/2))
        if (n30!=cell_30(layer,acenter)):
            hwidth=tan(deltaphi(layer,center)/2)*center
            hwidth=hwidth+tan(deltaphi(layer,acenter)/2)*acenter
            center=center-hwidth
            n30=cell_30(layer,acenter)
        else: center=acenter
        hwidth=tan(deltaphi(layer,center)/2)*center        
        if (center+hwidth*1.5>r_outer(layer)): continue
        if (center>si_boundary_layer(layer)): centers.append(center)
    return sorted(centers)

def cell_bounds(layer,center):
    rv=[]
    hwidth=tan(deltaphi(layer,center)/2)*center
    rv.append(center+hwidth)
    rv.append(center-hwidth)
    return rv

def cell_area(layer,center):
    width=tan(deltaphi(layer,center))*center        
    return width*width

def cell_amplitude(layer,cell_center):
#    return 20*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area/1.0
#    return 18*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/1.0
    if args.unitysignal: return 1
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for "overall PDE" ratio at 3V OV
    if (args.sipmscen==3):
        return 28.5/40.0*35*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/(1.3*1.3)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil, correct for "overall PDE" ratio at 2V OV (30 agreed as reference PDE from J. Virdee)
    if (args.sipmscen==2):
        return 20.5/30.0*35*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/(1.3*1.3)
    # based on J. Freeman result from testbeam of 35 PE/MIP for a 3x3 cm tile of EJ200 with ESR foil
    if (args.sipmscen==1):
        return 35*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/(1.3*1.3)
#    return 14*sqrt(30*30)/sqrt(cell_area(layer,cell_center))*sipm_area(layer,cell_center)/(1.3*1.3)
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

    
def sipm_noise(layer,cell_center):
    shaping_time=15.0 # ns
    sipm_temp_constant=1.88 # per 10 degrees
    sipm_temperature=-30
    sipm_base_noise=15 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 2V OV
    #sipm_base_noise=22 # PE/50 ns 2.8 mm circular device at 2e13, -23.5C, 3V OV
    
        
    sipm_constant=sipm_base_noise*sqrt(shaping_time/50.0)*sqrt(sipm_area(layer,cell_center)/(3.14159*1.4*1.4))*sqrt(pow(1.88,(sipm_temperature+23.5)/10))
    return sipm_constant*sqrt(fluence(layer,cell_center)/2e13*lumi/3000)

def sipm_power(layer,cell_center):
    sipm_base_current=200e-6
    sipm_voltage=56.0

    sipm_temp_constant=1.88 # per 10 degrees
    sipm_temperature=-30

    sipm_noise_current=sipm_base_current*fluence(layer,cell_center)/2e13*lumi/3000
    sipm_noise_current=sipm_noise_current*(sipm_area(layer,cell_center)/(3.14159*1.4*1.4))
    sipm_noise_current=sipm_noise_current*pow(sipm_temp_constant,(sipm_temperature+23.5)/10)
    return sipm_noise_current*sipm_voltage

total_sipms=0;
big_sipms=0;
under=0;
print("# ",args)
print("#layer,ring,center[mm],area[cm2],mipsig,sipm_noise,  S/N power[mW],fluence,dose[kRad],outer,inner,sipm_area,nring")
if args.allceh: irange=28+1
else: irange=28+9
for layer in range(irange,28+12+12+1):
    centers=generate_cell_centers(layer)
    i=-1
    for center in centers:
        i=i+1
        if (center<0): continue
        ring_sipms=cell_30(layer,center)*360/30*2
        total_sipms+=ring_sipms
        signal=cell_amplitude(layer,center)*radiation_loss(layer,center)
        edges=cell_bounds(layer,center)
        if (sipm_area(layer,center)>3.9): big_sipms=big_sipms+cell_30(layer,center)*360/30*2
        ring=i
        if (layer<=28+12):
            ringcode="f"
            ring=ring-16
        else: ringcode="b"
        if args.unitysignal:
            print("%2d,     %s%02d,  %6.0f,  %5.2f,    %5.3f,  %5.1f,    %5.2f,  %5.2f,  %4.1e,  %5.1f,   %4.0f, %4.0f,  %5.1f, %5d"%(layer-28, ringcode, ring, center, cell_area(layer,center)/100, signal, sipm_noise(layer,center),signal/sipm_noise(layer,center),sipm_power(layer,center)*1000,fluence(layer,center)*lumi/3000,dose(layer,center)*lumi/3000/1000,edges[0],edges[1],sipm_area(layer,center),ring_sipms))
        else:
            print("%2d,     %s%02d,  %6.0f,  %5.2f,    %5.1f,  %5.1f,    %5.2f,  %5.2f,  %4.1e,  %5.1f,   %4.0f, %4.0f,  %5.1f, %5d"%(layer-28, ringcode, ring, center, cell_area(layer,center)/100, signal, sipm_noise(layer,center),signal/sipm_noise(layer,center),sipm_power(layer,center)*1000,fluence(layer,center)*lumi/3000,dose(layer,center)*lumi/3000/1000,edges[0],edges[1],sipm_area(layer,center),ring_sipms))

print('# sipms=%d big-sipms=%d'%(total_sipms,big_sipms))

