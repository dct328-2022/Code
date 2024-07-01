import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class NodeTempr:
    instances = []
    def __init__(self, n, x, y, z):
        self.n = n
        self.x = x
        self.y = y
        self.z = z
        NodeTempr.instances.append(self)
    def changex(self, x):
        self.x = x
    def changey(self, y):
        self.y = y
    def changez(self, z):
        self.z = z
    def surfacedirection(self, di):
        self.di = di
        if di == 'x' or di == 'X':
            self.xp = self.y
            self.yp = self.z
        elif di == 'y' or di == 'Y':
            self.xp = self.x
            self.yp = self.z
        elif di == 'z' or di == 'Z':
            self.xp = self.x
            self.yp = self.y
    def addtempr(self, tempr):
        self.tempr = tempr

path = "/home/chenting/CompiledFDS/fds-FDS6.7.7/Build/mpi_gnu_linux_64"
folder = "204woGyp"
filename = "204woGyp-FL2_devc.csv"
Folder1 = "204-Fire1"
fn1 = open("%s/FDS Device locations Ceiling1Z-.txt"%Folder1)

for content in fn1:
    line = content.split()
    if len(line) == 5:
        NodeTempr(int(line[0]), float(line[1]), float(line[2]), float(line[3]))
        NodeTempr.instances[-1].surfacedirection(line[4])

fn1.close()
fn2 = open("%s/FDS Device locations Ceiling1Z+.txt"%Folder1)

for content in fn2:
    line = content.split()
    if len(line) == 5:
        NodeTempr(int(line[0]), float(line[1]), float(line[2]), float(line[3]))
        NodeTempr.instances[-1].surfacedirection(line[4])

fn2.close()

z2 = NodeTempr.instances[-1].z
z1 = NodeTempr.instances[0].z

existingpairs = list(range(1657, 2001, 1))
existingpairs += list(range(2001, 2279, 1))
existingpairs += list(range(2279, 2289, 1))
existingpairs += list(range(2289, 2300, 1))
existingpairs += list(range(3750, 3765, 1))
existingpairs += list(range(3765, 3786, 1))
existingpairs += list(range(3689, 3704, 1))
existingpairs += list(range(3704, 3725, 1))
existingpairs += list(range(3622, 3643, 1))

fn3 = open('NodePairs3-.txt','w')
for obj in NodeTempr.instances:
    xvalue = obj.x
    yvalue = obj.y
    zvalue = obj.z
    if obj.n not in existingpairs and zvalue == z1:
        theother = list(filter(lambda x: x.x == xvalue and x.y == yvalue and x.z== z2, NodeTempr.instances))
        if len(theother) == 1:
            fn3.write("%d %d\n"%(obj.n, theother[0].n))


