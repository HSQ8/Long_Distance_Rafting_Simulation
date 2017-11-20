#plot functions
from tkinter import *
import random
import numpy as np

class visulization:
    def __init__(self,_filename,_multiplier):
        self.multiplier = _multiplier
        self.data = self.datafiletoarray(_filename)
        self.coordData = self.data[:,0:2]
        print(self.coordData)
        self.latmin = int(np.amin(self.coordData[:,0:1]))
        self.latmax = int(np.amax(self.coordData[:,0:1]))
        self.longtmin = int(np.amin(self.coordData[:,1:2]))
        self.longtmax = int(np.amax(self.coordData[:,1:2]))
        
        self.latoffset = self.latmin
        self.longtoffset = self.longtmin
        
        _dimx = (self.longtmax - self.longtmin) * self.multiplier
        _dimy = (self.latmax - self.latmin) * self.multiplier

        self.dimx = _dimx
        self.dimy = _dimy
                
        self.root = Tk()
        self.root.geometry(str(self.dimx)+'x'+str(self.dimy))
        self.c = Canvas(self.root,width = self.dimx, height = self.dimy)
        self.filename = _filename

    def datafiletoarray(self,_filename):
        data = np.loadtxt(_filename)
        return data
        
    def plotpoints(self,lat,longt,color):
        
        lat -= self.latoffset
        longt -= self.longtoffset
        lat *= self.multiplier
        longt *= self.multiplier
        self.c.create_oval(longt,self.dimy - lat,longt,self.dimy - lat,width = 1, outline = color)

    def plotPath(self,lst):
        for i in range(len(lst)):
            lat,longt = lst[i]
            #print(lat)
            #print(longt)
            #self.plotpoints(lat,longt,'#ff0000')
            #self.drawCircle(lat,longt)
        for i in range(len(lst) - 1):
            lat1,longt1 = lst[i]
            lat2, longt2 = lst[1+i]

            lat1 -= self.latoffset
            longt1 -= self.longtoffset
            lat1 *= self.multiplier
            longt1 *= self.multiplier

            lat2 -= self.latoffset
            longt2 -= self.longtoffset
            lat2 *= self.multiplier
            longt2 *= self.multiplier

            point1 = (longt1, self.dimy - lat1)
            point2 = (longt2, self.dimy - lat2)

            self.drawline(point1,point2,"#ff0000")
    
    def drawline(self,pt1, pt2,color):
        '''draws a line given two points'''
        x1,y1 = pt1
        x2,y2 = pt2
        return self.c.create_line(x1, y1, x2 ,y2, fill = color,width = 2)

    def readpathdata(self,filename):
        file = open(filename,'r')
        lst = []
        for line in file:
            temparray = [float (n) for n in line.split()]
            tempcord = temparray[0],temparray[1]
            lst.append(tempcord)
        #print(lst)
        return lst
        
    def datafiletomemory(self,filename):
        datafile = open(filename,'r',)
        dataarray = []
        for line in datafile:
            temparray = [float (n) for n in line.split()]
            dataarray.append(temparray)
            self.plotpoints(temparray[0],temparray[1],'#000000')
        return dataarray

    def init_plot(self):
        
        self.c.pack()
        self.datafiletomemory(self.filename)
        self.root.bind('<q>', quit)
        #self.c.bind('<Button-1>', self.button_handler)
    def init_mainloop(self):
        self.root.mainloop()

    def drawCircle(self,lat,longt):
        randomradius = 2 #random.randint(5,25)

        lat -= self.latoffset
        longt -= self.longtoffset
        lat *= self.multiplier
        longt *= self.multiplier

        lat1 = lat - randomradius
        longt1 = longt - randomradius
        lat2 = lat + randomradius
        longt2 = longt + randomradius
        self.c.create_oval(longt1,self.dimy - lat1,longt2,self.dimy - lat2,width = 1, outline = "#ff0000", fill = "#ff0000")

        #return self.c.create_oval(x1, y1, x2, y2, outline = '#ff0000', fill = '#ff0000')

    def addpoint(self,lat,longt):
        self.plotpoints(lat,longt,'#ff0000')

    def button_handler(self,event):
        '''Handle left mouse button click events.'''
        x = event.x
        y = event.y
        self.drawCircle(x,y)
    def update(self):
        self.root.update()



if __name__ == '__main__':
    print('Constructing Fluid Matrix...')
    myplot = visulization('whole.dat',10)
    myplot.init_plot()
    myplot.plotPath(myplot.readpathdata('success_whole.datpath_dat6'))
    
    myplot.init_mainloop()


    
 