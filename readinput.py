import math
import os
import sys
# latmin,latmax,longtmin,longtmax
whole = -63.3, 26.5, 22.6, 150
belowequator = -63.3, 0, 22.6, 150
bottom = -39,-25, 44, 113
madagascarstraight =-25.5 ,-13.2,31.75,47
def printdataarray(lst):
    for i in lst:
        print(i)

def datafiletomemory(filename):
    datafile = open(filename,'r',)
    dataarray = []
    for line in datafile:
        temparray = [float (n) for n in line.split()]
        dataarray.append(temparray)
        return dataarray

def datafiletofile(filename,latmin,latmax,longtmin,longtmax):
    outfile = open(filename + '.dat','w')
    for i in range(1,36):
        num = (str(i).zfill(2))        
        datafile = open("SFCSD"+ num +".DAT",'r')               
        for line in datafile:
            temparray = [float (n) for n in line.split()]
            if checkifinBoundingbox(temparray[0], temparray[1],latmin,latmax,longtmin,longtmax) and not temparray[5] == 0.0 and len(temparray) == 8:
                outfile.write(line)        
        datafile.close()
    outfile.close()

def checkifinBoundingbox(lat,longt,latmin,latmax,longtmin,longtmax):
    return latmin < lat < latmax and longtmin < longt < longtmax

def computenetvector(filename,latmin,latmax,longtmin,longtmax):
    datafile = open(filename,'r',)
    dx = 0
    dy = 0
    for line in datafile:
        temparray = [float (n) for n in line.split()]
        if checkifinBoundingbox(temparray[0], temparray[1] ,latmin,latmax,longtmin,longtmax):
            dx += temparray[5]*math.sin(temparray[6]/180 * math.pi)
            dy += temparray[5]*math.cos(temparray[6]/180 * math.pi)
    dxy = (dx * dx + dy * dy) ** (1.0 / 2.0)
    theta = math.atan(dx/dy) * 180 / math.pi

    outfile = open((filename +'_netdirection.dat'),'w')
    outfile.write("dx  " + str(dx)+"\n")
    outfile.write("dy  " + str(dy)+"\n")
    outfile.write("dxy  " + str(dxy)+"\n")
    outfile.write("theta from true north  " + str(theta)+"\n")
    outfile.close()
    datafile.close()



latmin,latmax,longtmin,longtmax = belowequator

datafiletofile('belowequator',latmin,latmax,longtmin,longtmax)
computenetvector("belowequator.dat",latmin,latmax,longtmin,longtmax)

