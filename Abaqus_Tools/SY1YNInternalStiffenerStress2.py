execfile("/media/chenting/Work/ProgramCode/Tools/Interpolation.py")

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# ======== Output Destination

# for 120kN
#Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN1.txt'
#Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN2.txt'

# for 90kN
#Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN3.txt'
#Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN4.txt'

# for 60kN
#Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN5.txt'
Outfile = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY1ISSYN6.txt'

# 120kN -> 1.29918
# 90kN -> 1.17012
# 60kN -> 1.10256

# for 120kN
#stepselected = 1.283708
#stepselected = 1.301503

# for 90kN
#stepselected = 1.160886
#stepselected = 1.174052

# for 60kN
#stepselected = 1.099957
stepselected = 1.103611

XGrid = [-300.0, -294.0, -288.0]
for i in range(0, 18):
    XGrid.append(XGrid[-1] + 98.0/9)
XGrid = XGrid + [-86.0, -80.0]

YGrid = []
for i in range(0, 21):
    YGrid.append(1530.0 + 5*i)

ZGrid = [75.0, 85.0, 95.0, 105.0]

class Node:
    instances = []
    def __init__(self, x, y, z, upperbound = False):
        self.x = x
        self.y = y
        self.z = z
        self.upperbound = upperbound
        Node.instances.append(self)
    def x(self):
        return self.x
    def y(self):
        return self.y
    def z(self):
        return self.z
    def upperbound(self):
        return self.upperbound
    def adjnodes(self, nodelist):
        self.dis = 100000000.0
        nodelist1 = filter(lambda ii: abs(ii[3] - self.z) < 1.0, nodelist)
        for obj in nodelist:
            rule = lambda ii: ((self.x - ii[1])**2 + (self.y - ii[2])**2)**0.5
            nodelist2 = sorted(nodelist1, key=rule)
            self.adjnodesc = [nodelist2[0], nodelist2[1], nodelist2[2]]
            # Check if colinear
            if IfColinear(nodelist2[0][1], nodelist2[0][2], nodelist2[1][1], nodelist2[1][2], nodelist2[2][1], nodelist2[2][2]):
                self.adjnodesc = [nodelist2[0], nodelist2[1], nodelist2[3]]
            return self.adjnodesc
    def nodestress(self, stresslist):
        self.stress = LinearInterpolation3D(self.adjnodesc[0][1], self.adjnodesc[0][2], stresslist[0], self.adjnodesc[1][1], self.adjnodesc[1][2], stresslist[1], self.adjnodesc[2][1], self.adjnodesc[2][2], stresslist[2], self.x, self.y)
        return self.stress
    def finalstress(self):
        return self.stress
    def distance(self, node2):
        return ((self.x - node2.x)**2 + (self.y - node2.y)**2 + (self.z - node2.z)**2)**0.5
    def ydistance(self, node2):
        return -self.y + node2.y

filepath = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/Tplll.txt'
f1 = open(filepath)
linecounter = 0
stressnodelist = [[], []]
for line in f1:
    linecounter += 1
    if linecounter == 1:
        content = line.split()
        for obji in content[1:]:
            stressnodelist[0].append(int(obji))
    else:
        content = line.split()
        step = float(content[0])
        if step == stepselected:
            for obji in content[1:]:
                stressnodelist[1].append(float(obji))
f1.close()


prestartflag = 0
startflag = 0
endflag = 0
nodelist = []

filepath = '/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SY1.inp'
f1 = open(filepath, 'r')
for line in f1:
    if line.startswith('*Part, name=InternalStiffener'):
        prestartflag = 1
    if startflag == 1 and line.startswith("*Element"):
        break
    if startflag == 1:
        content = line.split(',')
        if int(content[0]) in stressnodelist[0]:
            nodelist.append([])
            for obj in content:
                nodelist[-1].append(float(obj))
    if prestartflag == 1:
        if line.startswith('*Node'):
            startflag = 1

f1.close()

circlecounter = 0

for obji in XGrid:
    for objj in YGrid:
        for objk in ZGrid:
            if (obji + 147)**2 + (objj - 1578)**2 >= 14.5**2 and (obji + 233)**2 + (objj - 1578)**2 >= 14.5**2:
                Node(obji, objj, objk)
            else:
                circlecounter += 1

print("A total of %d points inside the circle\n" % circlecounter)

for obji in ZGrid:
    Node(-244.44444444, 1586.9036, obji, True)
    Node(-244.44444444, 1569.0964, obji)

    Node(-233.55555556, 1592.4894, obji, True)
    Node(-233.55555556, 1563.5106, obji)

    Node(-222.66666667, 1588.1721, obji, True)
    Node(-222.66666667, 1567.8279, obji)

    Node(-157.33333333, 1588.1721, obji, True)
    Node(-157.33333333, 1567.8279, obji)

    Node(-146.44444444, 1592.4894, obji, True)
    Node(-146.44444444, 1563.5106, obji)

    Node(-135.55555556, 1586.9036, obji, True)
    Node(-135.55555556, 1569.0964, obji)



for obj in Node.instances:
    adjnodes = obj.adjnodes(nodelist)
    stresslist = []
    for obji in adjnodes:
        temp = filter(lambda ii: stressnodelist[0][ii] == int(obji[0]), range(0, len(stressnodelist[0])))[0]
        stresslist.append(stressnodelist[1][temp])
    obj.nodestress(stresslist)

FxSet = []
MzSet = []

for obji in XGrid:
    y0 = 1630.0
    z0 = 75.0
    Fx = 0
    Mz = 0

    while True:
        node1 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0) < 0.1, Node.instances)[0]
        node2 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 10) < 0.1, Node.instances)[0]
        node3 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 20) < 0.1, Node.instances)[0]
        node4 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 30) < 0.1, Node.instances)[0]

        filterednodes = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.z - z0) < 0.1 and ii.y < y0, Node.instances)
        if len(filterednodes) == 0:
            break
        filterednodessorted = sorted(filterednodes, key=lambda ii: ii.ydistance(node1))
        node5 = filterednodessorted[0]
        y0 = node5.y
        node6 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 10) < 0.1, Node.instances)[0]
        node7 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 20) < 0.1, Node.instances)[0]
        node8 = filter(lambda ii: abs(ii.x - obji) < 0.1 and abs(ii.y - y0) < 0.1 and abs(ii.z - z0 - 30) < 0.1, Node.instances)[0]
        ydis = abs(node1.y - node5.y)
        yc = 0.5*(node1.y + node5.y) - 1580.0
        if node1.upperbound:
            Area = 0
        else:
            Area = ydis*10
        stress1 = 0.25*(node1.finalstress() + node2.finalstress() + node5.finalstress() + node6.finalstress())
        stress2 = 0.25*(node2.finalstress() + node3.finalstress() + node6.finalstress() + node7.finalstress())
        stress3 = 0.25*(node3.finalstress() + node4.finalstress() + node7.finalstress() + node8.finalstress())
        Fx += (stress1 + stress2 + stress3)*Area
        Mz += (stress1 + stress2 + stress3)*Area*yc
    FxSet.append(Fx)
    MzSet.append(-Mz)

ofile = open(Outfile, 'w')
for i, obj in enumerate(XGrid):
    ofile.write("%d " % obj)
ofile.write('\n')
for obj in FxSet:
    ofile.write("%f " % obj)
ofile.write('\n')
for obj in MzSet:
    ofile.write("%f " % obj)
ofile.close()

#print(len(XGrid), len(FxSet))
plt.subplot(1, 2, 1)
plt.plot(XGrid, FxSet, 'ro')
plt.subplot(1, 2, 2)
plt.plot(XGrid, MzSet, 'ro')
plt.show()
