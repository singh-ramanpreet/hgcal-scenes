#!/bin/python

from math import *

layer=13
padding=0.25 # mm
dimple_rad=0.244*25.4
dimple_offset=0.062*25.4
scint_thickness=3.0
pcb_thickness=1.0
pcb_padding=0.5
pcb_gap=0.25
pcb_offset=pcb_thickness+pcb_gap
pcb_phi_gap=0.05
connector_cutout_r=3.5
connector_cutout_x=12.8+8
sipm=(2.12,2.12,0.4)
m2clear=2.4/2

bh_pcb_ranges=(16,15+16,15+16+11,15+16+11+8)
bh_pcb_conns=(15,16+14,16+15+1,16+15+12)

f=open("layer_%02d.scad"%(layer),"w")

with open("macros.scad","r") as g:
    for line in g:
        f.write(line)
g.close()

def cosdeg(angledeg):
    return cos(angledeg*3.141592/180)

def sindeg(angledeg):
    return sin(angledeg*3.141592/180)

def rerotate(x,y,phi_center):
    return [x*cosdeg(phi_center)-y*sindeg(phi_center),y*cosdeg(phi_center)+x*sindeg(phi_center)];

class RingData:
    def __init__(self,rname,rin,rout):
        self.ringname=rname
        self.ringnum=int(self.ringname[1:])
        self.inner=rin
        self.outer=rout
        if (self.ringname[0]=='f'): self.dphi=1.0
        else: self.dphi=1.25

    def printMe(self):
        print("%s,%d,%d,%.2f"%(self.ringname,self.inner,self.outer,self.dphi))
        
    def basePoints(self,phi_center):
        pts=[]
        pts.append(rerotate(self.inner*cosdeg(-self.dphi/2)+padding,self.inner*sindeg(-self.dphi/2)+padding,phi_center))
        pts.append(rerotate(self.inner*cosdeg(+self.dphi/2)+padding,self.inner*sindeg(+self.dphi/2)-padding,phi_center))
        pts.append(rerotate(self.outer*cosdeg(+self.dphi/2)-padding,self.outer*sindeg(+self.dphi/2)-padding,phi_center))
        pts.append(rerotate(self.outer*cosdeg(-self.dphi/2)-padding,self.outer*sindeg(-self.dphi/2)+padding,phi_center))
        return pts

    def dimple_pos(self,phi_center):
        return ((self.inner+self.outer)/2*cosdeg(phi_center),
                (self.inner+self.outer)/2*sindeg(phi_center),
                scint_thickness-dimple_offset-dimple_rad)
    
    def connector_pos(self,phi_center):
        r=(self.inner+connector_cutout_r/2)
        return rerotate(r,0,phi_center)
    
inner_mosts=[]
outer_mosts=[]

    
def load_data(layer):
    global inner_mosts, outer_mosts
    scint_rings=[]
    lout=0
    lastlayer=-1
    lastring=-1
    with open("sipm_detail.txt") as f:
        for line in f:
            if line[0]=='#': continue
            bits=line.split()
            ilayer=int(bits[0])
            if bits[1][0]=="f": continue # can't handle FH yet

            if ilayer!=lastlayer and lastlayer!=-1 and not (lastring in outer_mosts):
                outer_mosts.append(lastring)
            lastring=int(bits[1][1:])
            if ilayer!=lastlayer and not (lastring in inner_mosts):
                inner_mosts.append(lastring)
            lastlayer=ilayer
                
            if ilayer!=layer: continue
            scint_rings.append(RingData(bits[1],int(bits[11]),int(bits[10])))
    return scint_rings

def draw_pcbs(minring,maxring,rings):
    global inner_mosts, outer_mosts
    iphirange=8 # need a better source for this?

    f.write("color(\"green\")\ntranslate([0,0,%.3f]) {\n"%(-pcb_offset));
    if (layer>12):
        iring=minring
        for pcb in range(0,4):
            pcbrings=[]
            for j in rings:
                if pcb==0 or j.ringnum>=bh_pcb_ranges[pcb-1]:
                    pcbrings.append(j)
                if j.ringnum==bh_pcb_ranges[pcb]-1:
                    oring=j
                    break
            if pcb>0 and maxring.ringnum<bh_pcb_ranges[pcb-1]:
                continue
            if oring.ringnum<iring.ringnum: oring=maxring
            f.write("difference() {")
            f.write("   linear_extrude(height=%.3f) { polygon(["%(pcb_thickness))
            #inner edge
            for iphi in range(0,9):
                if iphi==0: phiadj=pcb_phi_gap
                elif iphi==8: phiadj=-pcb_phi_gap
                else: phiadj=0
                f.write("[%.3f,%.3f],"%((iring.inner+pcb_padding)*cosdeg(iring.dphi*iphi-iring.dphi/2+phiadj),(iring.inner+pcb_padding)*sindeg(iring.dphi*iphi-iring.dphi/2+phiadj)))
            for iphi in range(8,-1,-1):
                if iphi==0: phiadj=pcb_phi_gap
                elif iphi==8: phiadj=-pcb_phi_gap
                else: phiadj=0
                f.write("[%.3f,%.3f]"%((oring.outer-pcb_padding)*cosdeg(oring.dphi*iphi-oring.dphi/2+phiadj),(oring.outer-pcb_padding)*sindeg(oring.dphi*iphi-oring.dphi/2+phiadj)))
                if iphi!=0: f.write(",")
                else: f.write("]);}\n")
            # holes for mounting
            for j in pcbrings:
                if j.ringnum in inner_mosts or j.ringnum in bh_pcb_ranges:
                    f.write(" translate([%.3f,%.3f,-50]) { cylinder(100,%.3f,%.3f); }\n"%((j.inner+m2clear*3)*cosdeg(-j.dphi/2+2*pcb_phi_gap),(j.inner+m2clear*3)*sindeg(-j.dphi/2+2*pcb_phi_gap),m2clear,m2clear))
                    f.write(" translate([%.3f,%.3f,-50]) { cylinder(100,%.3f,%.3f); }\n"%((j.inner+m2clear*3)*cosdeg(7.5*j.dphi-2*pcb_phi_gap),(j.inner+m2clear*3)*sindeg(7.5*j.dphi-2*pcb_phi_gap),m2clear,m2clear))
                if j.ringnum in outer_mosts or j.ringnum+1 in bh_pcb_ranges:
                    f.write(" translate([%.3f,%.3f,-50]) { cylinder(100,%.3f,%.3f); }\n"%((j.outer-m2clear*3)*cosdeg(-j.dphi/2+2*pcb_phi_gap),(j.outer-m2clear*3)*sindeg(-j.dphi/2+2*pcb_phi_gap),m2clear,m2clear))
                    f.write(" translate([%.3f,%.3f,-50]) { cylinder(100,%.3f,%.3f); }\n"%((j.outer-m2clear*3)*cosdeg(7.5*j.dphi)+3*m2clear*sindeg(7.5*j.dphi-2*pcb_phi_gap),(j.outer-m2clear*3)*sindeg(7.5*j.dphi-2*pcb_phi_gap),m2clear,m2clear))
            f.write("  }\n")
            for j in rings:
                if j.ringnum==bh_pcb_ranges[pcb]: iring=j
    
    f.write("}\n")

def draw_cables(arange, rings):
    global f
    f.write("module cables() {\n")
    for iphi in range(0,8):
        for ring in rings:
            if ring.ringnum in bh_pcb_conns:
                ipcb=bh_pcb_conns.index(ring.ringnum)
                if (iphi==3 and ipcb==0) or (iphi==2 and ipcb==1) or (iphi==4 and ipcb==3) or (iphi==5 and ipcb==2):
                    cpos=ring.connector_pos(ring.dphi*iphi)
                    #local calcuation
                    perfectx=(iphi-3.5)*36+maxring.outer*sindeg(4.5)
                    currentx=(maxring.outer-ring.inner)*sindeg(iphi*ring.dphi)+cpos[1]
                    perfectangle=-atan2(currentx-perfectx,maxring.outer-ring.inner)*180/3.14156
                    print(iphi,perfectx,cpos[1],currentx,perfectangle)
                    f.write("  translate([%.3f,%.3f,0]) rotate(%.3f) {twinaxAndConnector(%f,%f);}\n"%(cpos[0],cpos[1],iphi*ring.dphi,maxring.outer-ring.inner,perfectangle))
                    if arange>1:
                        # upper
                        cposlcl=rerotate(cpos[0],cpos[1],10)
                        remapu=(0,1,2.1,3.5)
                        perfectx=(remapu[ipcb]+6-3.5)*36+maxring.outer*sindeg(4.5)
                        currentx=(maxring.outer-ring.inner)*sindeg(iphi*ring.dphi)+cposlcl[1]
                        perfectangle=-atan2(currentx-perfectx,maxring.outer-ring.inner)*180/3.14156-10
                        print(ipcb+6,perfectx,cpos[1],currentx,perfectangle)
                        f.write("  translate([%.3f,%.3f,0]) rotate(%.3f) {twinaxAndConnector(%f,%f);}\n"%(cposlcl[0],cposlcl[1],(iphi+8)*ring.dphi,maxring.outer-ring.inner,perfectangle))
                        # lower
                        cposlcl=rerotate(cpos[0],cpos[1],-10)
                        remapd=(3,0.8,2,-0.5)                        
                        perfectx=(remapd[ipcb]-2-3.5)*36+maxring.outer*sindeg(4.5)
                        currentx=(maxring.outer-ring.inner)*sindeg(iphi*ring.dphi)+cposlcl[1]
                        perfectangle=-atan2(currentx-perfectx,maxring.outer-ring.inner)*180/3.14156+10
                        print(ipcb-4,perfectx,cpos[1],currentx,perfectangle)
                        f.write("  translate([%.3f,%.3f,0]) rotate(%.3f) {twinaxAndConnector(%f,%f);}\n"%(cposlcl[0],cposlcl[1],(iphi-8)*ring.dphi,maxring.outer-ring.inner,perfectangle))
    f.write("}\n")


    
rings=load_data(layer)
minring=rings[0]
maxring=rings[0]
f.write("module scints() {\n")
for ring in rings:
    if (maxring.ringnum<ring.ringnum): maxring=ring
    if (minring.ringnum>ring.ringnum): minring=ring
for iphi in range(0,8):
    for ring in rings:        
        points=ring.basePoints(ring.dphi*iphi)
        f.write("difference() {\n")
        f.write("  linear_extrude(height=%.3f) {polygon([[%.3f,%.3f],[%.3f,%.3f],[%.3f,%.3f],[%.3f,%.3f]]);};\n"%(scint_thickness,points[0][0],points[0][1],points[1][0],points[1][1],points[2][0],points[2][1],points[3][0],points[3][1]))
        spoints=ring.dimple_pos(ring.dphi*iphi)
        f.write("  translate([%.3f,%.3f,%.3f]) {sphere(%f);}\n"%(spoints[0],spoints[1],spoints[2],dimple_rad))
        # adjust this to have cutouts shift with radius.
        if ring.ringnum in bh_pcb_conns:
            ipcb=bh_pcb_conns.index(ring.ringnum)
            if (iphi==3 and ipcb==0) or (iphi==2 and ipcb==1) or (iphi==4 and ipcb==3) or (iphi==5 and ipcb==2):
                cpos=ring.connector_pos(ring.dphi*iphi)
                f.write("  translate([%.3f,%.3f,0]) rotate(%.3f) {cube([%.3f,%.3f,10],true);}\n"%(cpos[0],cpos[1],iphi*ring.dphi,connector_cutout_r,connector_cutout_x))
        f.write("}\n")
f.write("}\n")
f.write("module pcbs(global_angle=0) {\n")
# add the sipm
for iphi in range(0,8):
    for ring in rings:        
        spoints=ring.dimple_pos(ring.dphi*iphi)
        f.write("color(\"DeepSkyBlue\") translate([%.3f,%.3f,%.3f]) rotate(%.3f) { cube([%.3f,%3.f,%.3f],true); }\n"%(spoints[0],spoints[1],sipm[2]/2-pcb_gap,ring.dphi*iphi,sipm[0],sipm[1],sipm[2]))

draw_pcbs(minring,maxring,rings)

f.write("}\n")
draw_cables(3,rings);

f.write("scints(); pcbs();\n");
f.write("rotate(10) { scints(); pcbs(); }\n");
f.write("rotate(-10) { scints(); pcbs(); }\n");
f.write("cables();\n");

f.close()
    


