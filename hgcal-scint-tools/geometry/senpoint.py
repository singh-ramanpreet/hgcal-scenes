#!/usr/bin/python3

from math import sin,cos,sqrt,atan,atan2,acosh,asinh,sinh
from ec_dimensions import *
import sys

sensor_size=164.1*2/sqrt(3) # effective diameter in mm
sixtydeg=3.14159/180*60

cassette_dphi=30
cell_rotation=3.14159/2
handed=0

cassette_angle=sixtydeg/2

x=int(sys.argv[1])
y=int(sys.argv[2])
i=int(sys.argv[3])

xx=x*sensor_size*sqrt(3)/4*2+(y%2)*sensor_size*sqrt(3)/4
yy=y*sensor_size*3/4

    
points=(sensor_size/2*cos(cell_rotation),sensor_size/2*sin(cell_rotation),
        sensor_size/2*cos(sixtydeg+cell_rotation),sensor_size/2*sin(sixtydeg+cell_rotation),
        sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
        sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
        sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
        sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))

xx=xx+points[i*2]
yy=yy+points[i*2+1]
ang=atan2(yy,xx)*180.0/3.14159


print("%d,%d (%d)-> %d,%d (%.2f) (%.2f) "%(x,y,i,xx,yy,sqrt(xx*xx+yy*yy),60-ang))
