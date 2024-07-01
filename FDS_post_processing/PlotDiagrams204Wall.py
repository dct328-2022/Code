import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
exec(open("HSV2RGB.py").read())

# ============================= Contour Plot ==========================
TimeSelected = 60*40
#TimeSelected = 'max' 
#TemperatureGradient = range(120, 20, -20)
Folder1 = "204-Fire1"
#TemperatureGradient = [50, 45, 40, 35, 30]
TemperatureGradient = [300, 117]

# Read xx_devc.csv file
path = "/home/chenting/CompiledFDS/fds-FDS6.7.7/Build/mpi_gnu_linux_64"
folder = "204woNoGyp"
filename = "204woNoGyp_devc.csv"

# Wall3b Y-
GroupBegin = 5927
GroupEnd = 7076
fn1 = open("%s/FDS Device locations Wall3bY-.txt"%Folder1)
part = 'wall3by-'

# Wall3a Y-
#GroupBegin = 7077
#GroupEnd = 7329
#fn1 = open("%s/FDS Device locations Wall3aY-.txt"%Folder1)

# Wall3 Y+
#GroupBegin = 7330
#GroupEnd = 8732
#fn1 = open("%s/FDS Device locations Wall3Y+.txt"%Folder1)
#part = 'wall3y+'

# Ceiling1 Z-
#GroupBegin = 1657
#GroupEnd = 3791
#fn1 = open("%s/FDS Device locations Ceiling1Z-.txt"%Folder1)
#part = 'ceiling'

# Ceiling1 Z+
#GroupBegin = 3792
#GroupEnd = 5926
#fn1 = open("%s/FDS Device locations Ceiling1Z+.txt"%Folder1)
#part = 'ceiling'

# Wall4 X+
#GroupBegin = 8733
#GroupEnd = 9008
#fn1 = open("%s/FDS Device locations Wall4X+.txt"%Folder1)
#part = 'wall4x+'

# Wall4 X-
#GroupBegin = 9009
#GroupEnd = 9284
#fn1 = open("%s/FDS Device locations Wall4X-.txt"%Folder1)

# Wall1 Y+
#GroupBegin = 1
#GroupEnd = 828
#fn1 = open("%s/FDS Device locations Wall1Y+.txt"%Folder1)

# Wall1a Y-
#GroupBegin = 829
#GroupEnd = 1242
#fn1 = open("%s/FDS Device locations Wall1aY-.txt"%Folder1)

# Wall1b Y-
#GroupBegin = 1243
#GroupEnd = 1656
#fn1 = open("%s/FDS Device locations Wall1bY-.txt"%Folder1)

exec(open("PlotDiagramMainProgram.py").read())


