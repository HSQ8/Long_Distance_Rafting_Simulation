#simulation module
from scipy import spatial
import numpy as np
import math
import random

class simulation:
    def __init__(self,_filename):
        self.const_terminate_value = 10000000
        self.filename = _filename
        self.data = self.datafiletoarray(_filename)
        self.KDtree = spatial.cKDTree(self.data[:,0:2])
        self.directionData = self.data[:,5:7]
        self.pathRay = []
        self.distanceTraveled = 0
        self.dt = 1
        #default target zone, must be replaced by custom target
        self.tTotal = 0
        self.latmin = -50
        self.latmax = -10
        self.longtmin = 10
        self.longtmax = 110
        self.successSimulation = False
        self.m_debug = False
        self.const_knotstodegrees = 180 * 1.852 / 6371 / math.pi


    def initialize_position(self,lat,longt):
        position = lat,longt
        self.successSimulation = False
        del self.pathRay [:]
        self.pathRay.append(position)


    def datafiletoarray(self,_filename):
        data = np.loadtxt(_filename)
        return data

    def advance(self):
        pointlat,pointlongt = self.pathRay[-1]
        if self.m_debug:
            print('point lat: '+str(pointlat))
            print('point longt: '+str(pointlongt)+'\n')

        distance, index = self.KDtree.query([pointlat,pointlongt])
        if self.m_debug:
            print('distance: ' + str(distance))
            print('index: '+ str(index)+'\n')

        velocity,angle = self.directionData[index]
        if self.m_debug:
            print('velocity'+str(velocity))
            print('angle'+ str(angle)+'\n')

        pointlat += velocity * math.sin(angle /180 * math.pi) * self.dt * self.const_knotstodegrees
        pointlongt += velocity * math.cos(angle /180 * math.pi) * self.dt * self.const_knotstodegrees
        self.distanceTraveled += distance
        newpoint = pointlat,pointlongt
        self.pathRay.append(newpoint)
        self.tTotal += 1
        if self.m_debug:
            print("newpoint:" + str(newpoint))
            print('####################division###############')

    def exportData(self,trialNum):
        if self.successSimulation:
            np.savetxt("success_"+self.filename+"path_dat"+str(trialNum),np.asarray(self.pathRay),'%5.2f')
            #editfile = open(self.filename+'path_dat','a')
            #editfile.write("time elapsed:  "+ str(self.tTotal))
            #editfile.close()
            print('Target Reached')
        if False:
            np.savetxt("FAIL_"+self.filename+"path_dat"+str(trialNum),np.asarray(self.pathRay),'%5.2f')
            #editfile = open(self.filename+'path_dat','a')
            #editfile.write("time elapsed:  "+ str(self.tTotal))
            #editfile.close()
            print('Target Not Reached')

    def setTargetZone(self,_latmin,_latmax,_longtmin,_longtmax):
        self.latmin = _latmin
        self.latmax = _latmax
        self.longtmin = _longtmin
        self.longtmax = _longtmax

    def inTargetZone(self):
        #print(len(self.pathRay))
        #print((self.pathRay))
        #print((self.pathRay[len(self.pathRay) - 1]))
        lat,longt = self.pathRay[-1]
        return self.latmin < lat < self.latmax and self.longtmin < longt < self.longtmax

    def reachTerminateCondition(self):
        terminate = self.inTargetZone()
        if terminate:
            self.successSimulation = True
            return terminate

        terminate = len(self.pathRay) > self.const_terminate_value
        return terminate

    def generaterandomStartingPoint(self,_latmin,_latmax,_longtmin,_longtmax):
        return random.uniform(_latmin,_latmax), random.uniform(_longtmin,_longtmax)

print('initialize KDTree')
mysimulation = simulation('whole.dat')
mysimulation.setTargetZone(-37,-13,111,120)

for i in range(100000):
    print('initialize experiment: ' + str(i))
    initiallat,initiallongt = mysimulation.generaterandomStartingPoint(-32,-10,31,56)
    mysimulation.initialize_position(initiallat,initiallongt)

    while not mysimulation.reachTerminateCondition():
        mysimulation.advance()

    mysimulation.exportData(i)
