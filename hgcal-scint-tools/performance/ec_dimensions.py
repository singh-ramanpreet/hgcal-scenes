#!/usr/bin/python3

#
# works only for the CEH!
#
from math import cosh
from math import tan

scaling=1

def set_scaling(sc):
    global scaling
    scaling=sc

def z_coord(layer):
    global scaling

    zloc=[
        3677.1, 3731.6, 3786.1, 3840.6,
	3895.1, 3949.6, 4004.1, 4058.6,
	4111.3, 4165.8, 4220.3, 4274.8,
	4360.3, 4445.8, 4531.3, 4616.8,
	4702.3, 4787.3, 4873.3, 4958.8,
	5044.3, 5129.8
        ]

    if (layer<1 or layer>22): return -1
    return zloc[layer-1]*scaling

def r_inner(layer):
    global scaling
    return z_coord(layer)/cosh(3.0)+3*scaling

def r_outer(layer):
    global scaling

    if (layer<1 or layer>22): return -1
    
#    r_outer_array=[1590.7, 1597.3, 1643.3, 1649.1,
#                   1649.1, 1718.5, 1806, 1864.5,
#		   1997, 2086, 2132, 2227,
#		   2326.6, 2430, # 13-14
#		   2539, 2594, 2594, 2494,  # 15-18
#		   2594, 2594, 2594, 2484]
    r_outer_array=[1662.3,1681.2,1700.1,1718.9,
     1737.8,1801.6,1873.3,1945.7,
     2017.8,2089.8,2161.9,2233.9,
     2346.9,2460.0,2573.0,2624.6,
     2624.6,2624.6,2624.6,2624.6,
     2624.6,2484.9]
    
    if (layer<1 or layer>22): return -1
    return r_outer_array[layer-1]*scaling

#for layer in range(29,28+12+12+1):
#    print "%d %d %d %d"%(layer,z_coord(layer),r_inner(layer),r_outer(layer))

#for layer in range(28+9,28+12+12+1):
#    print (z_coord(layer)+z_coord(layer-1))/2

def r_scint(layer):
    # mm from April 15, 2019 SG meeting
    global scaling

    if (layer<1 or layer>22): return -1
    r_scint_data = [-1, -1, -1, -1,
		    -1, -1, -1, -1,
		    1537, 1537, 1537, 1537,
		    1378, 1378,
		    1180, 1180, 1180, 1180,
		    1035, 1035, 1035, 1035]
    if (layer<1 or layer>22): return -1
    return r_scint_data[layer-1]*scaling
