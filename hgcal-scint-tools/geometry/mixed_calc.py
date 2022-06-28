#!/usr/bin/python3

from math import sin,cos,sqrt,atan,atan2,acosh,asinh,sinh
from ec_dimensions import *
from sensor import *
import sys
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
from shapely.ops import cascaded_union
from shapely import affinity

from matplotlib import pyplot as plt
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString
from descartes import PolygonPatch

sixtydeg=3.14159/180*60

cassette_dphi=30
cell_rotation=3.14159/2

cassette_angle=sixtydeg/2

mueta=24
bounds=None

si_boundary=radii_sc

vertex_list=[]

def r_outer_chop(glayer):
    return r_outer(glayer)*cos(10*3.14159/180)

def override(x,y,mode,bounds):
    layer=bounds.hlayer
    handed=bounds.handed
    if (mode==0):
#        if (handed==0 and layer == 9) and x==(-2) and y==(10): return True
#        if (handed==1 and layer == 9) and x==(2) and y==(10): return True
        if (handed==1 and layer == 9) and x==(0) and y in [9,7,5]: return True
        if (handed==0 and layer == 9) and x==(0) and y in [10]: return True
        if (handed==0 and layer == 10) and x==(0) and y in [9]: return True
        if (handed==0 and layer == 10) and x in [-2,-1] and y in [9]: return True
        if (handed==1 and layer == 10) and x==(0) and y in [7,5]: return True
        if (handed==1 and layer == 10) and x==(1) and y in [9]: return True
        if (handed==0 and layer < 12+8) and x==(0) and y==(4): return True         
        if (handed==0 and layer in [12+1,12+2,12+3,12+11,12+12]) and x==(0) and y==(6): return True
        if (handed==1 and layer <= 12+12) and x==(2) and y==4: return True
        if (handed==1 and layer < 12+1) and x==(1) and y==3: return True
#        if (handed==0 and layer == 12+1) and x in [-1,0] and y==8: return True
        if (handed==1 and layer in [12+1,12+2]) and x in [1] and y==7: return True
        if (handed==0 and layer in [12+1, 12+2]) and x in [-2] and y==7: return True
        if (handed==1 and layer == 12+1) and x in [1] and y==8: return True
        if (handed==0 and layer in [12,12+2] and x==(0) and (y==5)): return True
        if (handed==1 and layer in [12+1] and x==(0) and (y==5)): return True
        if (handed==1 and layer in [12,12+1,12+2] and x==(0) and (y==7)): return True
        if (handed==1 and (layer >= 12+3 and layer <=12+12) and x==(0) and (y==5)): return True
        if (handed==0 and layer >= 12+11 and x in [0,-1] and (y==7)): return True
    if (mode==10 or mode==11):
        if (handed==1 and layer in [9,10,11,12] and x==(0) and (y==3)): return True
        if (handed==1 and layer >= 12+1 and layer <= 12+9) and x==(1) and y==3: return True
        if (handed==0 and layer >= 12+11 and layer <= 12+12) and x==(0) and y==4: return True

    if (mode==12 or mode==13):
        if (handed==0 and layer == 9 and x==(-1) and (y==10)): return True
        if (handed==0 and layer == 10 and x==(-3) and (y==9)): return True
        if (handed==1 and layer in [9] and x==(1) and (y==10)): return True
        if (handed==1 and layer >= 12+11 and layer <= 12+12) and x==(1) and y==7: return True
        if (handed==0 and layer >= 12+11 and layer <= 12+12) and x==(-2) and y==7: return True
#        if (handed==1 and layer == 12 and x==(4) and (y==8)): return True
#        if (handed==1 and layer == 12 and x==(-3) and (y==8)): return True
#    if (mode==100):
#    if (mode==200):
#         if (handed==0 and layer >= 12+8 and x==(0) and (y==4)): return True
#        if (handed==1 and layer == 12 and x==(3) and (y==8)): return True
#        return False
    return False   

def get_dropped_sensors(bounds,sides=6):
    layer=bounds.hlayer
    handed=bounds.handed

    if (layer==9):
        if (handed==0): return [[-4,8]]
        else: return [[0,10]]
    if (layer in [10]):
        if (handed==0): return [] #[-4,8],[0,9]]
        else: return [[0,9],[4,7]]
    if (layer in [11]):
        if (handed==0): return [[-4,7]] #[-4,8],[0,9]]
        else: return [[0,8]]
    if (layer in [12+1,12+1]):
        if (handed==0): return [[1,8]]
#        else: return [[5,8]]
    if (layer in [12+11,12+12]):
        if (handed==1): return [[0,7],[3,5]]
    if (layer>=12+3):
        if (handed==0): return [[-3,5]]
        else: return [[0,6]]
    if (layer==12):
        if (handed==0): return [[-4,7]]
        else: return [[0,8]]
    if (layer==12+2):
        if (handed==0): return [[-3,6],[0,7]]
    return []

def check_point(x,y,bounds):
    global scaling,sensor_size
    layer=bounds.glayer
    handed=bounds.handed
    rsi=(radii_si[layer-28-12+4-1]*scaling+sensor_size/3)
    if (sqrt(x*x+y*y)<(r_inner(layer)+2*scaling)):
        return 0
    elif ((x*x+y*y)>r_outer_chop(layer)*r_outer_chop(layer)):
        return 0
    elif ((x*x+y*y)>rsi*rsi):
        return 0
    elif (atan2(x,y)<bounds.si_left*1.0001):
        return 0      
    elif (atan2(x,y)>bounds.si_right*1.0001):
        return 0
    else: return 1

def n_inside(points,bounds):
    nin=0
    for pt in points:
        nin=nin+check_point(pt[0],pt[1],bounds)
    return nin

def is_sensor_ok(sensor,bounds):
    if n_inside(sensor.points,bounds)==len(sensor.points) and check_point(sensor.center[0],sensor.center[1],bounds)==1: return True
    if override(sensor.global_i[0],sensor.global_i[1],sensor.mode,bounds): return True
    return False

def calc_cassette(bounds,sensorveto):
    layer=bounds.glayer
    handed=bounds.handed

    #find where the left boundary intersects the sensors
    leftls=LineString([[0,0],[r_outer_chop(layer)*sin(bounds.scint_left),r_outer_chop(layer)*cos(bounds.scint_left)]])
    leftend=[0,0]
#    for sensor in sensors:
    bigshape=sensorveto.buffer(1)
    if leftls.intersects(bigshape):
        inter=leftls.intersection(bigshape)
        if inter.bounds[3]>leftend[1]:
            leftend=[inter.bounds[0],inter.bounds[3]]

    rightend=[0,0]
    rightls=LineString([[0,0],[r_outer_chop(layer)*sin(bounds.scint_right),r_outer_chop(layer)*cos(bounds.scint_right)]])
#    for sensor in sensors:
    bigshape=sensorveto.buffer(1)
    if rightls.intersects(bigshape):
        inter=rightls.intersection(bigshape)
        if inter.bounds[3]>rightend[1]:
            rightend=[inter.bounds[2],inter.bounds[3]]
    
    pwedge=None
    if (handed==0):
        points=[leftend]
        points.append([r_outer_chop(layer)*sin(bounds.scint_left),r_outer_chop(layer)*cos(bounds.scint_left)])
        points.append([r_outer(layer)*sin(-sixtydeg/3),r_outer(layer)*cos(-sixtydeg/3)])
        points.append([0,r_outer(layer)])
        points.append(rightend)
        pwedge=Polygon(points)
    else:
        points=[leftend]
        points.append([r_outer(layer)*sin(bounds.scint_left),r_outer(layer)*cos(bounds.scint_left)])
        points.append([r_outer(layer)*sin(sixtydeg/3),r_outer(layer)*cos(sixtydeg/3)])
        points.append([r_outer_chop(layer)*sin(bounds.scint_right),r_outer_chop(layer)*cos(bounds.scint_right)])
        points.append(rightend)
        pwedge=Polygon(points)
    return pwedge
                    

def get_scint_radii(layer):
    scint_radii=[]
    lout=0
    with open("sipm_tdr.txt") as f:
        for line in f:
            if line[0]=='#': continue
            bits=line.split()
            if int(bits[0])!=layer-28: continue
            scint_radii.append(int(bits[11]))
            lout=int(bits[10])
    scint_radii.append(lout)
    return scint_radii

class Tileboard:
    nominal_radii=[]
    
    def __init__(self,bring,phicenter,supersensor,cassette):
        self.bring=bring
        self.phicenter=phicenter
        self.shape=None
        # ring sizes
        ringcounts=[16,8,8,8,6,6]

        if len(Tileboard.nominal_radii)==0:
            Tileboard.nominal_radii=get_scint_radii(28+12+12)

        ii=0
        for i in range(1,bring):
            ii=ii+ringcounts[i-1]        
        self.nominal_inner=Tileboard.nominal_radii[ii]
        self.inner_i=ii
        if ii+ringcounts[bring-1]>len(Tileboard.nominal_radii):
            self.nominal_outer=Tileboard.nominal_radii[len(Tileboard.nominal_radii)-1]
        else: self.nominal_outer=Tileboard.nominal_radii[ii+ringcounts[bring-1]]
        self.outer_i=ii+ringcounts[bring-1]
        self.makeShape(supersensor,cassette)
#        print("%d,%.1f,%.1f"%(ii+ringcounts[bring-1],self.nominal_inner,self.nominal_outer))
    
    def makeShape(self,sensorarea,cassette):
        pts=[]
        for iphi in range(-4,5):
            angle=(self.phicenter+iphi*1.25)*3.14159/180
            pts.append([self.nominal_inner*sin(angle),self.nominal_inner*cos(angle)])
        for iphi in range(4,-5,-1):
            angle=(self.phicenter+iphi*1.25)*3.14159/180
            pts.append([self.nominal_outer*sin(angle),self.nominal_outer*cos(angle)])
        fullshape=Polygon(pts)
        wosensors=fullshape.difference(sensorarea)
        self.shape=wosensors.intersection(cassette)

    def countringdata(self,bounds):
        for ring in range(self.inner_i,self.outer_i):
            nring=0
            for iphi in range(-4,4):
                angle=(self.phicenter+iphi*1.25)*3.14159/180
                tilepts=[[Tileboard.nominal_radii[ring]*sin(angle),Tileboard.nominal_radii[ring]*cos(angle)],
                         [Tileboard.nominal_radii[ring+1]*sin(angle),Tileboard.nominal_radii[ring+1]*cos(angle)]]
                angle=(self.phicenter+(iphi+1)*1.25)*3.14159/180
                tilepts.append([Tileboard.nominal_radii[ring+1]*sin(angle),Tileboard.nominal_radii[ring+1]*cos(angle)])
                tilepts.append([Tileboard.nominal_radii[ring]*sin(angle),Tileboard.nominal_radii[ring]*cos(angle)])
                cell=Polygon(tilepts)
                overlap=cell.intersection(self.shape)
                if (cell.area<0.1): fraction=-1.0
                else: fraction=overlap.area/cell.area
                if fraction>0.55: nring=nring+1
#                print("%d,%d,%d,%d,%.3f,%.2f"%(self.bring,self.phicenter,ring,iphi,fraction,cell.area))
#            print("%d,%d,%d,%d,%d,%d"%(bounds.hlayer,bounds.handed,self.bring,self.phicenter,ring,nring))

                         
                
        
def calc_tileboards(supersensor,plate,bounds):
    handed=bounds.handed
    tileboards=[]

    for iring in range(1,6):
        for phicenter in range(-5+handed*30,-35+handed*30,-10):
            tileboards.append(Tileboard(iring,phicenter,supersensor,plate))
    for tileboard in tileboards:
        tileboard.countringdata(bounds)
    return tileboards

ifig=1

def calc_plane(bounds):
    global ifig
    sensors=[]
    sensorshapes=[]  

    for x in range(-10,12):
        for y in range(-1,29) :
            for mode in (0,10,11,12,13):
                sensor=Sensor(mode,x,y)
                if is_sensor_ok(sensor,bounds):
                    sensors.append(sensor)
                    sensorshapes.append(sensor.getShape().buffer(0.2))
                    break

    supersensor=cascaded_union(sensorshapes)
                
    vetos=get_dropped_sensors(bounds)
    for veto in vetos:
        vetosensor=Sensor(0,veto[0],veto[1])
        sensorshapes.append(vetosensor.getShape().buffer(0.2))                

    superveto=cascaded_union(sensorshapes)

    coolingplate=calc_cassette(bounds,superveto)

    tileboards=calc_tileboards(superveto,coolingplate,bounds)

    for tileboard in tileboards:
        print(tileboard.bring,tileboard.phicenter)
        ashape = affinity.rotate(tileboard.shape,tileboard.phicenter,origin=Point(0,0))
        print(ashape)
    
#    for sensor in sensors:
#        sensor.printMe()
#        sensor.getShape()

    aratio=(coolingplate.bounds[0]-100-coolingplate.bounds[2]-200)/(supersensor.bounds[1]-100-coolingplate.bounds[3]-100)

    fig = plt.figure(ifig, figsize=(5,5/aratio), dpi=90)
    ifig=ifig+1
    ax = fig.add_subplot(111)
    ax.set_xlim(coolingplate.bounds[0]-100,coolingplate.bounds[2]+200)
    ax.set_ylim(supersensor.bounds[1]-100,coolingplate.bounds[3]+100)
    ring_patch = PolygonPatch(coolingplate)
    ax.add_patch(ring_patch)

    apatch=PolygonPatch(supersensor, fc="#0099cc")
    ax.add_patch(apatch)

    for sensor in sensors:
        apatch=PolygonPatch(sensor.getShape(), fc="#6699cc")
        ax.add_patch(apatch)
                       
    for tileboard in tileboards:
        #print(tileboard.shape)
        try:
            apatch=PolygonPatch(tileboard.shape, fc="#22CCcc")
            ax.add_patch(apatch)
        except:
            print(tileboard.shape)
            pass

    stub="L"
    if bounds.handed==1: stub="R"
    
    plt.savefig('calc_%d%s.pdf'%(bounds.hlayer,stub), dpi=300)

layer=int(sys.argv[1])
handed=0
if len(sys.argv)>2:
    handed=int(sys.argv[2])
bounds=Bounds(layer,handed)
Sensor.si_rotation=bounds.si_rot
calc_plane(bounds)

#for ilayer in range(13,25):
#    for ihanded in range(0,2):
#        bounds=Bounds(ilayer,ihanded)
#        Sensor.si_rotation=bounds.si_rot
#        calc_plane(bounds)
        

#geomf.close()
