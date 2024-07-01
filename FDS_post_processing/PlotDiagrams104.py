import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
exec(open("HSV2RGB.py").read())

# ============================= Contour Plot ==========================
#TimeSelected = 480
TimeSelected = 'max'
TemperatureGradient = [300, 290, 280, 270, 260, 250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 130, 120, 117, 110, 100, 90, 80]
Folder1 = "104-Fire1"
#TemperatureGradient = [50, 45, 40, 35, 30]
#TemperatureGradient = [300, 117]

# Read xx_devc.csv file
path = "/home/chenting/CompiledFDS/fds-FDS6.7.7/Build/mpi_gnu_linux_64"
folder = "104FireNewLocation"
filename = "104FireNewLocation_devc.csv"

# Wall3b Y-
GroupBegin = 1
GroupEnd = 552
fn1 = open("%s/FDS Device locations Wall3bY-.txt"%Folder1)

# Wall3a Y-
#GroupBegin = 553
#GroupEnd = 805
#fn1 = open("%s/FDS Device locations Wall3aY-.txt"%Folder1)

# Wall3 Y+
#GroupBegin = 1358
#GroupEnd = 2185
#fn1 = open("%s/FDS Device locations Wall3Y+.txt"%Folder1)
#3.166000000000001,7.536000,1.8780000000000006

# Ceiling1 Z-
#GroupBegin = 3842
#GroupEnd = 5101
#fn1 = open("%s/FDS Device locations Ceiling1Z-.txt"%Folder1)

# Ceiling1 Z+
#GroupBegin = 5102
#GroupEnd = 6361
#fn1 = open("%s/FDS Device locations Ceiling1Z+.txt"%Folder1)

# Wall4 X+
#GroupBegin = 806
#GroupEnd = 1081
#fn1 = open("%s/FDS Device locations Wall4X+.txt"%Folder1)

# Wall4 X-
#GroupBegin = 1082
#GroupEnd = 1357
#fn1 = open("%s/FDS Device locations Wall4X-.txt"%Folder1)

# Wall1 Y+
#GroupBegin = 2186
#GroupEnd = 3013
#fn1 = open("%s/FDS Device locations Wall1Y+.txt"%Folder1)

# Wall1a Y-
#GroupBegin = 3014
#GroupEnd = 3427
#fn1 = open("%s/FDS Device locations Wall1aY-.txt"%Folder1)

# Wall1b Y-
#GroupBegin = 1243
#GroupEnd = 1656
#fn1 = open("%s/FDS Device locations Wall1bY-.txt"%Folder1)

exec(open("PlotDiagramMainProgram.py").read())


