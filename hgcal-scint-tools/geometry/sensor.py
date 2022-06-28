#!/usr/bin/python3

from math import sin,cos,sqrt,atan,atan2,acosh,asinh,sinh
from ec_dimensions import *
from shapely.geometry.polygon import Polygon

class Sensor:
    
    # Rotation angle for the sensor plane
    si_rotation=0.0

    # modes
    # 0 --> standard full sensor
    # 10-->19 variations of half sensor
    
    def __init__(self,xmode,ix,iy):
        self.mode=xmode
        self.global_i=(ix,iy)
        self.center=(0,0)
        self.points=[]
        self.shapely=None
        if self.mode==0:
            self.constructStandard()
        if self.mode>=10 and self.mode<19:
            self.constructHalf()

    def printMe(self):
        if self.mode==0:
            print ("Full hexagon (%d,%d)"%self.global_i)
        if self.mode>=10 and self.mode<=19:
            print ("Half hexagon (%d,%d) type %d"%(self.global_i[0],self.global_i[1],self.mode))
        print ("  Center: %.3f,%.3f"%self.center)
        print ("  Points:")
        for point in self.points:
            print ("    [%.3f,%.3f]"%(point[0],point[1]))

    def constructStandard(self):
        cell_rotation=3.14159/2-self.si_rotation
        sixtydeg=3.14159/180*60
        
        local_pts=(sensor_size/2*cos(cell_rotation),sensor_size/2*sin(cell_rotation),
                   sensor_size/2*cos(sixtydeg+cell_rotation),sensor_size/2*sin(sixtydeg+cell_rotation),
                   sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                   sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                   sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                   sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))    
        
        xx=self.global_i[0]*sensor_size*sqrt(3)/4*2+(self.global_i[1]%2)*sensor_size*sqrt(3)/4
        yy=self.global_i[1]*sensor_size*3/4

        self.center=(cos(self.si_rotation)*xx+sin(self.si_rotation)*yy,cos(self.si_rotation)*yy-sin(self.si_rotation)*xx)
        
        for ipt in range(0,len(local_pts),2):
            self.points.append([local_pts[ipt]+self.center[0],local_pts[1+ipt]+self.center[1]])

    def constructHalf(self):
        cell_rotation=3.14159/2-self.si_rotation        
        sixtydeg=3.14159/180*60
        if self.mode==10:
            local_pts=(sensor_size/2*cos(0*sixtydeg+cell_rotation),sensor_size/2*sin(0*sixtydeg+cell_rotation),
                       sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                       sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                       sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        elif self.mode==11:
            local_pts=(sensor_size/2*cos(0+cell_rotation),sensor_size/2*sin(0+cell_rotation),
                       sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                       sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                       sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        elif self.mode==12:
            local_pts=(sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                       sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                       sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation),
                       sensor_size/2*cos(5*sixtydeg+cell_rotation),sensor_size/2*sin(5*sixtydeg+cell_rotation))
        elif self.mode==13:
            local_pts=(sensor_size/2*cos(1*sixtydeg+cell_rotation),sensor_size/2*sin(1*sixtydeg+cell_rotation),
                       sensor_size/2*cos(2*sixtydeg+cell_rotation),sensor_size/2*sin(2*sixtydeg+cell_rotation),
                       sensor_size/2*cos(3*sixtydeg+cell_rotation),sensor_size/2*sin(3*sixtydeg+cell_rotation),
                       sensor_size/2*cos(4*sixtydeg+cell_rotation),sensor_size/2*sin(4*sixtydeg+cell_rotation))

        xx=self.global_i[0]*sensor_size*sqrt(3)/4*2+(self.global_i[1]%2)*sensor_size*sqrt(3)/4
        yy=self.global_i[1]*sensor_size*3/4

        self.center=(cos(self.si_rotation)*xx+sin(self.si_rotation)*yy,cos(self.si_rotation)*yy-sin(self.si_rotation)*xx)
        
        for ipt in range(0,len(local_pts),2):
            self.points.append([local_pts[ipt]+self.center[0],local_pts[1+ipt]+self.center[1]])

    def getShape(self):
        if not self.shapely:
            self.shapely=Polygon(self.points)
        return self.shapely

#Sensor.si_rotation=0.1
#sensor=Sensor(0,1,3)
#sensor.printMe()
#sensor3=Sensor(13,1,4)
#sensor3.printMe()
