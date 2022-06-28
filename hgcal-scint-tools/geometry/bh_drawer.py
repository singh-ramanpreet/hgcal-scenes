#!/usr/bin/python3

from pyx import *
from math import sin,cos,sqrt,atan,atan2,acosh,asinh,sinh
from ec_dimensions import *
import sys

#sensor_size=164.1*2/sqrt(3) # effective diameter in mm
sensor_size=167.441*2/sqrt(3) # effective diameter in mm
scaling=0.01
sensor_size=sensor_size*scaling
set_scaling(scaling)
sensor_area=3*sqrt(3)/2*(sensor_size/2)*(sensor_size/2)
sixtydeg=3.14159/180*60

cassette_dphi=30
cell_rotation=3.14159/2
handed=0

cassette_angle=sixtydeg/2

#geomf=open("bh_counts.csv","w")

#radii_si=[1144,1076,1022,971,933,908,885,873,885,898,911,923]

mueta=24

radii_si=[1374, 1304, 1238, 1249,
#          1162,1074,922,922,
          1074,1074,922,922,          
          922,922,922,922,
          922,922,922,922]

# these may be slightly smaller than the si boundaries to cover sliver-edges
radii_sc=[1365, 1304, 1187, 1190,
          1062, 1062, 922,  922,
#          1147, 1062, 922,  922,          
          922,922,922,922,
          922,922,922,922] 

si_boundary=radii_sc
si_rot=0

vertex_list=[]

def setup_boundaries(layer,handed):
    global si_left, si_right, scint_left, scint_right, cassette_left, cassette_right, si_rot, cell_rotation

    hlayer=layer
    sshift=0
    if (hlayer==9): sshift=sixtydeg/60*1.95
    if (hlayer==10): sshift=sixtydeg/60*4.13
    if (hlayer==11): sshift=sixtydeg/60*2.20
    if (hlayer==12): sshift=sixtydeg/60*2.23
    if (hlayer==12+1): sshift=sixtydeg/60*4.71
    if (hlayer==12+2): sshift=sixtydeg/60*2.54
    if (hlayer>=12+3 and hlayer<=12+10): sshift=sixtydeg/60*3.00
    if (hlayer>=12+11 and hlayer<=12+12): sshift=sixtydeg/60*5.50

    si_rot=-sshift
    cell_rotation=3.14159/2-si_rot
    sshift=0

    if handed==0:
        cassette_left=-sixtydeg/2
        cassette_right=+0
        si_left=cassette_left
        si_right=cassette_right+sixtydeg/10
        scint_left=cassette_left+sshift
        scint_right=cassette_right+sshift
    else:
        cassette_left=0
        cassette_right=sixtydeg/2
        si_left=cassette_left
        si_right=cassette_right+1.5*sixtydeg/12
        scint_left=cassette_left+sshift
        scint_right=cassette_right+sshift
           

def r_outer_chop(layer):
    return r_outer(layer)*cos(10*3.14159/180)

def override(x,y,mode):
    global layer,handed
    if (mode<0):
#        if (handed==0 and layer == 28+9) and x==(-2) and y==(10): return True
#        if (handed==1 and layer == 28+9) and x==(2) and y==(10): return True
        if (handed==1 and layer == 28+9) and x==(0) and y in [9,7,5]: return True
        if (handed==0 and layer == 28+9) and x==(0) and y in [10]: return True
        if (handed==0 and layer == 28+10) and x==(0) and y in [9]: return True
        if (handed==0 and layer == 28+10) and x in [-2,-1] and y in [9]: return True
        if (handed==1 and layer == 28+10) and x==(0) and y in [7,5]: return True
        if (handed==1 and layer == 28+10) and x==(1) and y in [9]: return True
        if (handed==0 and layer < 28+12+8) and x==(0) and y==(4): return True         
        if (handed==0 and layer in [28+12+1,28+12+2,28+12+3,28+12+11,28+12+12]) and x==(0) and y==(6): return True
        if (handed==1 and layer <= 28+12+12) and x==(2) and y==4: return True
        if (handed==1 and layer < 28+12+1) and x==(1) and y==3: return True
#        if (handed==0 and layer == 28+12+1) and x in [-1,0] and y==8: return True
        if (handed==1 and layer in [28+12+1,28+12+2]) and x in [1] and y==7: return True
        if (handed==0 and layer in [28+12+1, 28+12+2]) and x in [-2] and y==7: return True
        if (handed==1 and layer == 28+12+1) and x in [1] and y==8: return True
        if (handed==0 and layer in [28+12,28+12+2] and x==(0) and (y==5)): return True
        if (handed==1 and layer in [28+12+1] and x==(0) and (y==5)): return True
        if (handed==1 and layer in [28+12,28+12+1,28+12+2] and x==(0) and (y==7)): return True
        if (handed==1 and (layer >= 28+12+3 and layer <=28+12+12) and x==(0) and (y==5)): return True
        if (handed==0 and layer >= 28+12+11 and x in [0,-1] and (y==7)): return True
    if (mode==0):
        if (handed==1 and layer in [28+9,28+10,28+11,28+12] and x==(0) and (y==3)): return True
        if (handed==1 and layer >= 28+12+1 and layer <= 28+12+9) and x==(1) and y==3: return True
        if (handed==0 and layer >= 28+12+11 and layer <= 28+12+12) and x==(0) and y==4: return True

    if (mode==1):
        if (handed==0 and layer == 28+9 and x==(-1) and (y==10)): return True
        if (handed==0 and layer == 28+10 and x==(-3) and (y==9)): return True
        if (handed==1 and layer in [28+9] and x==(1) and (y==10)): return True
        if (handed==1 and layer >= 28+12+11 and layer <= 28+12+12) and x==(1) and y==7: return True
        if (handed==0 and layer >= 28+12+11 and layer <= 28+12+12) and x==(-2) and y==7: return True
#        if (handed==1 and layer == 28+12 and x==(4) and (y==8)): return True
#        if (handed==1 and layer == 28+12 and x==(-3) and (y==8)): return True
#    if (mode==100):
#    if (mode==200):
#         if (handed==0 and layer >= 28+12+8 and x==(0) and (y==4)): return True
#        if (handed==1 and layer == 28+12 and x==(3) and (y==8)): return True
#        return False
    return False   

def get_dropped_sensors(layer,sides=6):
    global handed
    if (layer==28+9):
        if (handed==0): return [[-4,8]]
        else: return [[0,10]]
    if (layer in [28+10]):
        if (handed==0): return [] #[-4,8],[0,9]]
        else: return [[0,9],[4,7]]
    if (layer in [28+11]):
        if (handed==0): return [[-4,7]] #[-4,8],[0,9]]
        else: return [[0,8]]
    if (layer in [28+12+1,28+12+1]):
        if (handed==0): return [[1,8]]
#        else: return [[5,8]]
    if (layer in [28+12+11,28+12+12]):
        if (handed==1): return [[0,7],[3,5]]
    if (layer>=28+12+3):
        if (handed==0): return [[-3,5]]
        else: return [[0,6]]
    if (layer==28+12):
        if (handed==0): return [[-4,7]]
        else: return [[0,8]]
    if (layer==28+12+2):
        if (handed==0): return [[-3,6],[0,7]]
    return []

def get_extra_line(layer):
    global handed
    if (handed==1 and layer >=28+12+3 and layer < 28+12+11):
        return [0,6,5]
    if (handed==1 and layer == 28+9):
        return [0,10,5]
    if (handed==1 and layer == 28+10):
        return [0,9,5]
    if (handed==1 and layer in [28+11,28+12]):
        return [0,8,5]
    if (handed==0 and layer == 28+12+1):
        return [1,8,1]
    if (handed==0 and layer == 28+12+2):
        return [0,7,1]
    if (handed==1 and layer >= 28+12+11):
        return [0,7,5]
    return []


def draw_sensor(x,y,fillmode=0):
    global c,si_rot,cell_rotation,vertex_list
    xx=x*sensor_size*sqrt(3)/4*2+(y%2)*sensor_size*sqrt(3)/4
    yy=y*sensor_size*3/4
    
    points=(sensor_size/2*cos(cell_rotation),sensor_size/2*sin(cell_rotation),
            sensor_size/2*cos(sixtydeg+cell_rotation),sensor_size/2*sin(sixtydeg+cell_rotation),
            sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
            sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
            sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
            sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))    
    if fillmode==0 and n_inside(xx,yy,points)<6 and not override(x,y,-1): return False
    p = path.path(path.moveto(points[0],points[1]),
                  path.lineto(points[2],points[3]),
                  path.lineto(points[4],points[5]),
                  path.lineto(points[6],points[7]),
                  path.lineto(points[8],points[9]),
                  path.lineto(points[10],points[11]),
                  path.lineto(points[0],points[1]))
    rxx=cos(si_rot)*xx+sin(si_rot)*yy
    ryy=cos(si_rot)*yy-sin(si_rot)*xx    
    if fillmode==0:
        c.stroke(p,[trafo.translate(rxx,ryy),deco.filled([color.cmyk.SkyBlue])])
    else:
        c.stroke(p,[trafo.translate(rxx,ryy),style.linewidth.THIN,deco.stroked([color.cmyk.White]),deco.filled([color.cmyk.White])])
    for ipt in range(0,len(points),2):
        vertex_list.append([points[ipt]+rxx,points[1+ipt]+ryy])
    c.text(rxx,ryy,"%d,%d"%(x,y))

    return True

def draw_blank(x,y,md):
    if (md==0): return draw_sensor(x,y,1)
    if (md==100): return draw_five_sensor(x,y,1,1)

def draw_half_sensor(x,y,mode):
    global c,si_rot,cell_rotation,vertex_list

    xx=x*sensor_size*sqrt(3)/4*2+(y%2)*sensor_size*sqrt(3)/4
    yy=y*sensor_size*3/4

    if (mode==0):
        if (xx>0):
            points=(sensor_size/2*cos(0*sixtydeg+cell_rotation),sensor_size/2*sin(0*sixtydeg+cell_rotation),
                    sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                    sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                    sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        else:
            points=(sensor_size/2*cos(0+cell_rotation),sensor_size/2*sin(0+cell_rotation),
                    sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                    sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                    sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
    elif (mode==1):
        if (xx<0):
            points=(sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                    sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                    sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                    sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        else:
            points=(sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                    sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                    sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                    sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation))
    elif (mode==2):
        points=(sensor_size/2*cos(cell_rotation),sensor_size/2*sin(cell_rotation),
                sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
    elif (mode==3):
        points=(sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                0,sensor_size/2*sin(4*sixtydeg+cell_rotation),
                0,sensor_size/2*sin(2*sixtydeg+cell_rotation),
                sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation))
    elif (mode==4):
        points=(sensor_size/2,0,
                sensor_size/2*cos(sixtydeg+cell_rotation),sensor_size/2*sin(sixtydeg+cell_rotation),
                sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        
    if n_inside(xx,yy,points)<len(points)/2 and not override(x,y,mode): return False
    if len(points)==8:
        p = path.path(path.moveto(points[0],points[1]),
                      path.lineto(points[2],points[3]),
                      path.lineto(points[4],points[5]),
                      path.lineto(points[6],points[7]),
                      path.lineto(points[0],points[1]))
    else:
        p = path.path(path.moveto(points[0],points[1]),
                      path.lineto(points[2],points[3]),
                      path.lineto(points[4],points[5]),
                      path.lineto(points[6],points[7]),
                      path.lineto(points[8],points[9]),
                      path.lineto(points[0],points[1]))
#    c.stroke(p,[trafo.translate(xx,yy),deco.filled([color.cmyk.PineGreen])])
    rxx=cos(si_rot)*xx+sin(si_rot)*yy
    ryy=cos(si_rot)*yy-sin(si_rot)*xx    
    c.stroke(p,[trafo.translate(rxx,ryy),deco.filled([color.cmyk.SkyBlue])])
    for ipt in range(0,len(points),2):
        vertex_list.append([points[ipt]+rxx,points[1+ipt]+ryy])
    return True

def draw_five_sensor(x,y,mode,fillmode=0):
    global c,si_rot

    xx=x*sensor_size*sqrt(3)/4*2+(y%2)*sensor_size*sqrt(3)/4
    yy=y*sensor_size*3/4

    if (mode==1):
        points=(sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
    if (mode==2):                                                         
        points=(sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation),
                sensor_size/2*cos(0*sixtydeg+cell_rotation),sensor_size/2*sin(0*sixtydeg+cell_rotation))
        
    if fillmode==0 and (n_inside(xx,yy,points)<(len(points)/2) and not override(x,y,100*mode)): return False
    if len(points)==8:
        p = path.path(path.moveto(points[0],points[1]),
                      path.lineto(points[2],points[3]),
                      path.lineto(points[4],points[5]),
                      path.lineto(points[6],points[7]),
                      path.lineto(points[0],points[1]))
    else:
        p = path.path(path.moveto(points[0],points[1]),
                      path.lineto(points[2],points[3]),
                      path.lineto(points[4],points[5]),
                      path.lineto(points[6],points[7]),
                      path.lineto(points[8],points[9]),
                      path.lineto(points[0],points[1]))
    rxx=cos(si_rot)*xx+sin(si_rot)*yy
    ryy=cos(si_rot)*yy-sin(si_rot)*xx    
    for ipt in range(0,len(points),2):
        vertex_list.append([points[ipt]+rxx,points[1+ipt]+ryy])
    if fillmode==0:
        c.stroke(p,[trafo.translate(rxx,ryy),deco.filled([color.cmyk.SkyBlue])])
    else:
        c.stroke(p,[trafo.translate(rxx,ryy),style.linewidth.THIN,deco.stroked([color.cmyk.White]),deco.filled([color.cmyk.White])])
    return True


def draw_extra_line(cx, cy, pt):
    global c,si_rot,cell_rotation
    xx=cx*sensor_size*sqrt(3)/4*2+(cy%2)*sensor_size*sqrt(3)/4
    yy=cy*sensor_size*3/4
    
    points=(sensor_size/2*cos(cell_rotation),sensor_size/2*sin(cell_rotation),
            sensor_size/2*cos(sixtydeg+cell_rotation),sensor_size/2*sin(sixtydeg+cell_rotation),
            sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
            sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
            sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
            sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))

    rxx=cos(si_rot)*xx+sin(si_rot)*yy+points[pt*2]
    ryy=cos(si_rot)*yy-sin(si_rot)*xx+points[pt*2+1]
    rx0=cos(si_rot)*xx+sin(si_rot)*yy+points[0]
    ry0=cos(si_rot)*yy-sin(si_rot)*xx+points[1]
    
    yint=-rx0*(ryy-ry0)/(rxx-rx0)+ry0
        
    p=path.path(path.moveto(rxx,ryy),
                path.lineto(0,yint),
                path.lineto(0,yint+10))
    c.stroke(p)

def interpol(x,x0,y0,x1,y1):
    return y0+(y1-y0)/(x1-x0)*(x-x0)

def check_point(x,y):
    global layer, radii_si, sensor_size
    rsi=(radii_si[layer-28-12+4-1]*scaling+sensor_size/3)
    if (sqrt(x*x+y*y)<(r_inner(layer)+2*scaling)): return 0
    elif ((x*x+y*y)>r_outer_chop(layer)*r_outer_chop(layer)): return 0
    elif ((x*x+y*y)>rsi*rsi): return 0
    elif (atan2(x,y)<si_left*1.0001):        return 0         
    elif (atan2(x,y)>si_right*1.0001):        return 0
    else: return 1

def n_inside(xx,yy,points):
    nin=0
    for j in range(0,len(points),2):
        nin=nin+check_point(xx+points[j],yy+points[j+1])
    if not check_point(xx,yy): return nin-1
    return nin

def draw_cassette():
    global layer,c,handed
    rsi=(radii_sc[layer-28-12+4-1])*scaling
    if (handed==0):
        p = path.path(path.arc(0,0,rsi,90-scint_right/3.14159*180,90-scint_left/3.14159*180),
                    path.lineto(r_outer_chop(layer)*sin(scint_left),r_outer_chop(layer)*cos(scint_left)),
#                  path.arcn(0,0,r_outer_chop(layer),90+30,90-30),
                  path.lineto(r_outer(layer)*sin(-sixtydeg/3),r_outer(layer)*cos(-sixtydeg/3)),
                      path.lineto(0,r_outer(layer)),
                  path.lineto(r_outer_chop(layer)*sin(scint_right),r_outer_chop(layer)*cos(scint_right)),
                  path.lineto(rsi*sin(scint_right),rsi*cos(scint_right))
        )
    else:
        p = path.path(path.arc(0,0,rsi,90-scint_right/3.14159*180,90-scint_left/3.14159*180),
                      path.lineto(r_outer_chop(layer)*sin(scint_left),r_outer_chop(layer)*cos(scint_left)),
                      path.lineto(r_outer(layer)*sin(sixtydeg/3),r_outer(layer)*cos(sixtydeg/3)),
                      path.lineto(r_outer_chop(layer)*sin(scint_right),r_outer_chop(layer)*cos(scint_right)),
                      path.lineto(rsi*sin(scint_right),rsi*cos(scint_right))
        )
    c.stroke(p,[deco.filled([color.cmyk.RedOrange])])

def get_scint_radii(layer):
    scint_radii=[]
    lout=0
    with open("sipm_detail.txt") as f:
        for line in f:
            if line[0]=='#': continue
            bits=line.split()
            if int(bits[0])!=layer-28: continue
            scint_radii.append(int(bits[11]))
            lout=int(bits[10])
    scint_radii.append(lout)
    return scint_radii


def draw_tileboards():
    global layer,c
    if (layer>28+12):
        boundaries=[1307,1556,1853,2207,2515,2685]
        r_innerX=si_boundary[layer-28-12+4-1]*scaling
        for boundary in boundaries:
            radius=boundary*scaling
            if radius>r_innerX and radius<r_outer(layer):
                p = path.path(path.arc(0,0,radius,90-scint_right/3.14159*180,90-scint_left/3.14159*180))
                c.stroke(p,[style.linestyle.solid,deco.stroked,color.rgb.blue])
        for bdi in range(0,4):
            angle=(10*bdi)*3.14159/180+scint_left
            r_outerX=r_outer(layer)
            if bdi==2: r_outerX=r_outer_chop(layer) 
            p = path.path(path.moveto(r_innerX*sin(angle),r_innerX*cos(angle)),
                          path.lineto(r_outerX*sin(angle),r_outerX*cos(angle)))
            
            c.stroke(p,[style.linestyle.solid,deco.stroked,color.rgb.blue])
            
    

def draw_megatiles():
    global layer,c
    rsi=(radii_sc[layer-28-12+4-1])*scaling

    if (handed==0):
        p = path.path(path.arc(0,0,rsi,90-scint_right/3.14159*180,90-scint_left/3.14159*180),
                    path.lineto(r_outer_chop(layer)*sin(scint_left),r_outer_chop(layer)*cos(scint_left)),
#                  path.arcn(0,0,r_outer_chop(layer),90+30,90-30),
                  path.lineto(r_outer(layer)*sin(-sixtydeg/3),r_outer(layer)*cos(-sixtydeg/3)),
                      path.lineto(0,r_outer(layer)),
                  path.lineto(r_outer_chop(layer)*sin(scint_right),r_outer_chop(layer)*cos(scint_right)),
                  path.lineto(rsi*sin(scint_right),rsi*cos(scint_right))
        )
    else:
        p = path.path(path.arc(0,0,rsi,90-scint_right/3.14159*180,90-scint_left/3.14159*180),
                      path.lineto(r_outer_chop(layer)*sin(scint_left),r_outer_chop(layer)*cos(scint_left)),
                      path.lineto(r_outer(layer)*sin(sixtydeg/3),r_outer(layer)*cos(sixtydeg/3)),
                      path.lineto(r_outer_chop(layer)*sin(scint_right),r_outer_chop(layer)*cos(scint_right)),
                      path.lineto(rsi*sin(scint_right),rsi*cos(scint_right))
        )
    c.stroke(p,[deco.filled([color.cmyk.Yellow])])


    r_edges=get_scint_radii(layer)

    ieta=0
    rin=r_edges[0]*scaling

    rout=0
    for edge in r_edges:
        tile_r=edge*scaling
        p = path.path(path.arc(0,0,tile_r,90-scint_right/3.14159*180,90-scint_left/3.14159*180))
        c.stroke(p,[style.linestyle.dotted,deco.stroked,color.rgb.red])
        ieta=ieta+1

        if (layer<=12+28): cells_per_30=30
        else:    cells_per_30=24
        for iphi in range(1,int(cassette_dphi/30*cells_per_30)):
            tile_edge=scint_left+iphi*30/cells_per_30*3.14159/180
            p = path.path(path.moveto(rin*sin(tile_edge),rin*cos(tile_edge)),
                          path.lineto(tile_r*sin(tile_edge),tile_r*cos(tile_edge)))
            c.stroke(p,[style.linestyle.dotted,deco.stroked,color.rgb.red])
 
def draw_plane(ilayer,dphi):
    global layer,c,vertex_list
    layer=ilayer
    c = canvas.canvas()
    nwhole = 0
    nhalf = 0
    nq = 0
    vertex_list= []
    
    draw_cassette()

    draw_megatiles()

    drops=get_dropped_sensors(ilayer)
    for drop in drops:
        if len(drop)>2:
            draw_blank(drop[0],drop[1],drop[2])
        else: draw_blank(drop[0],drop[1],0)

    extraline=get_extra_line(ilayer)
    if len(extraline)>1:
        draw_extra_line(extraline[0],extraline[1],extraline[2])
    
    
    for x in range(-10,12):
        for y in range(-1,29) :
            if draw_sensor(x,y):
                nwhole=nwhole + 1                
#            elif draw_five_sensor(x,y,1):
#                nhalf=nhalf+1
#            elif draw_five_sensor(x,y,2):
#                nhalf=nhalf+1
            elif draw_half_sensor(x,y,0):
                nhalf=nhalf+1
            elif draw_half_sensor(x,y,1):
                nhalf=nhalf+1

    draw_tileboards()
                
    etavalues=[3.0,2.9,2.7,2.4,2.2,2.0,1.8,1.6,1.479,1.4]
    for eta in etavalues:
        if eta<1.45 and (layer<=28+12+1 or layer==28+12+12): continue
        radius=(z_coord(layer))/sinh(eta)
        p = path.path(path.arc(0,0,radius,90-scint_right/3.14159*180,90-scint_left/3.14159*180))
#        p = path.path(path.arc(0,0,10,90+scint_left/3.14159*180,90+scint_right/3.14159*180))
#        c.stroke(p,[style.linestyle.dashed,deco.stroked,color.rgb.black])
        if (eta==1.479):
            c.text(0.2,radius-0.2,"$\\eta$=%.2f"%(eta))
        else: c.text(0.2,radius-0.2,"$\\eta$=%.1f"%(eta))

        
    if handed==0:
        handed_text="L"
    else:
        handed_text="R"

    p = path.path(path.arc(0,0,si_boundary[layer-28-12+4-1]*scaling,90-scint_right/3.14159*180,90-scint_left/3.14159*180))
    c.stroke(p,[style.linestyle.dashed,deco.stroked,color.rgb.blue])
    p = path.path(path.arc(0,0,r_inner(layer),90-scint_right/3.14159*180,90-scint_left/3.14159*180))
    c.stroke(p,[style.linestyle.dashed,deco.stroked,color.rgb.blue])
    p = path.path(path.arc(0,0,r_outer(layer),90-scint_right/3.14159*180,90-scint_left/3.14159*180))
    c.stroke(p,[style.linestyle.dashed,deco.stroked,color.rgb.blue])

        
        
    if layer<= 28+12:
        c.text(-9.2+15*handed,5,"FH Layer %d%s"%(layer-28,handed_text),[text.size(sizename="Huge")])
    else:
        c.text(-9.2+15*handed,5,"BH Layer %d%s"%(layer-28-12,handed_text),[text.size(sizename="Huge")])

        
    
    c.text(-9.1+15*handed,4.5,"Whole modules : %d"%(nwhole),[text.size(sizename="large")])
    c.text(-9.1+15*handed,4.1,"Odd modules : %d"%(nhalf),[text.size(sizename="large")])
    
    print ("Number of whole modules: ",nwhole)
    print ("Number of odd modules: ",nhalf)
    print (z_coord(layer))
    print (vertex_list)
    exterior_vert=[]
    for vert in vertex_list:
        nmatch=0
        for vert2 in vertex_list:
            if (pow(vert[0]-vert2[0],2)+pow(vert[1]-vert2[1],2)<0.01): nmatch=nmatch+1
        if nmatch==1:
            exterior_vert.append(vert)
        if nmatch==2:
            ne=0
            for vert2 in exterior_vert:
                if (pow(vert[0]-vert2[0],2)+pow(vert[1]-vert2[1],2)<0.01): ne=ne+1
            if ne==0: exterior_vert.append(vert)
    for vert in exterior_vert:
        print ("%.5f,%.5f"%(vert[0],vert[1]))

    if layer<= 28+12:
        c.writePDFfile("fh_layer_%d%s.pdf"%(layer-28,handed_text))
    else:
        c.writePDFfile("bh_layer_%d%s.pdf"%(layer-28-12,handed_text))

    outer_area=nq/4.0
        
#    geomf.write("%d,%d,%d,%.2f,%.2f\n"%(layer-28,nwhole,nhalf,inner_area,outer_area))
        

for ihanded in range(0,2):
    handed=ihanded
    for ilayer in range(9,13+12):
#    for ilayer in range(12+3,13+3):        
        setup_boundaries(ilayer,handed)
        draw_plane(ilayer+28,cassette_dphi)

#geomf.close()
