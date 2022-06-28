#!/usr/bin/python3

#
# assumes 28 layers of EE, 12 layers of FH, 12 layer of BH
#
from math import cosh
from math import tan,sqrt

#sensor_size=164.1*2/sqrt(3) # effective diameter in mm
sensor_size=167.441*2/sqrt(3) # effective diameter in mm
sensor_area=3*sqrt(3)/2*(sensor_size/2)*(sensor_size/2)

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

si_left=0
si_right=0
scint_left=0
scint_right=0
cassette_left=0
cassette_right=0

scaling=1

class Bounds:
    def __init__(self,layer,handed):
        sixtydegrad=3.14159/180*60

        self.hlayer=layer
        sshift=0
        if (self.hlayer==9): sshift=sixtydegrad/60*1.95
        if (self.hlayer==10): sshift=sixtydegrad/60*4.13
        if (self.hlayer==11): sshift=sixtydegrad/60*2.20
        if (self.hlayer==12): sshift=sixtydegrad/60*2.23
        if (self.hlayer==12+1): sshift=sixtydegrad/60*4.71
        if (self.hlayer==12+2): sshift=sixtydegrad/60*2.54
        if (self.hlayer>=12+3 and self.hlayer<=12+10): sshift=sixtydegrad/60*3.00
        if (self.hlayer>=12+11 and self.hlayer<=12+12): sshift=sixtydegrad/60*5.50
        self.glayer=self.hlayer+28
        
        self.si_rot=-sshift
        self.cell_rotation=3.14159/2-self.si_rot
        self.handed=handed

        if handed==0:
            self.cassette_left=-sixtydegrad/2
            self.cassette_right=+0
            self.si_left=self.cassette_left
            self.si_right=self.cassette_right+sixtydegrad/10
            self.scint_left=self.cassette_left
            self.scint_right=self.cassette_right
        else:
            print("YOYOYO")
            self.cassette_left=0
            self.cassette_right=sixtydegrad/2
            self.si_left=self.cassette_left
            self.si_right=self.cassette_right+1.5*sixtydegrad/12
            self.scint_left=self.cassette_left
            self.scint_right=self.cassette_right


def set_scaling(sc):
    global scaling
    scaling=sc

def z_coord(layer):
    global scaling
    if (layer<=28):
        return (3500-(28-layer)*10)*scaling
    elif (layer<=(28+12)):
        return (3558.8+4+(layer-28-1)*47.8)*scaling
    else:
        return (4097.4+74+4+(layer-28-12-1)*86.8)*scaling

def r_inner(layer):
    global scaling
    if (layer<=28):    
        return z_coord(layer)/cosh(3.0)+3*scaling
    else:
        r_inner_surkov=[356.3, 361.1, 365.9, 370.7, 375.5, 380.3, 385.1, 389.9, 
394.7, 399.5, 404.3, 409.1,  417.3, 426.1, 434.8, 443.6, 452.3, 461.0, 469.8, 478.5, 487.2, 496.0, 504.7, 513.4]
        return r_inner_surkov[layer-28-1]*scaling        


def r_outer(layer):
    global scaling
    if (layer<=28):
        return r_outer(28+8)-(z_coord(28+8)-z_coord(layer))*tan(18*3.14159/180)*scaling
    #((1700.0-1600.0)/(z_coord(28)-z_coord(1))*(z_coord(layer)-z_coord(1))+1600)*scaling    
    else:
        r_outer_surkov=[1696.9, 1713.5, 1730.1, 1746.7, 1763.3, 1779.9, 1796.4, 1844.2, 1907.6, 1971.0, 2034.5, 2097.9, 2184.6, 2299.8, 2415.0, 2530.2, 2645.3, 2664., 2664., 2664., 2664., 2664.,2664.,2664]        
        return r_outer_surkov[layer-28-1]*scaling


#if __name__ == "__main__":
#    for layer in range(29,28+12+12+1):
#        print "%d %d %d %d"%(layer,z_coord(layer),r_inner(layer),r_outer(layer))
