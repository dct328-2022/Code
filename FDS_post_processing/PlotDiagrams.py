import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
exec(open("HSV2RGB.py").read())

# ============================= Contour Plot ==========================
#TimeSelected = 480
TimeSelected = 'max'
TemperatureGradient = [300, 290, 280, 270, 260, 250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 130, 120, 117, 110, 100, 90, 80]
Folder1 = "204-Fire1"
#TemperatureGradient = [50, 45, 40, 35, 30]
#TemperatureGradient = [300, 117]

# Wall3b Y-
#GroupBegin = 5927
#GroupEnd = 7076
#fn1 = open("%s/FDS Device locations Wall3bY-.txt"%Folder1)

# Wall3a Y-
#GroupBegin = 7077
#GroupEnd = 7329
#fn1 = open("%s/FDS Device locations Wall3aY-.txt"%Folder1)

# Wall3 Y+
#GroupBegin = 7330
#GroupEnd = 8732
#fn1 = open("%s/FDS Device locations Wall3Y+.txt"%Folder1)

# Ceiling1 Z-
#GroupBegin = 1657
#GroupEnd = 3791
#fn1 = open("%s/FDS Device locations Ceiling1Z-.txt"%Folder1)

# Ceiling1 Z+
#GroupBegin = 3792
#GroupEnd = 5926
#fn1 = open("%s/FDS Device locations Ceiling1Z+.txt"%Folder1)

# Wall4 X+
#GroupBegin = 8733
#GroupEnd = 9008
#fn1 = open("%s/FDS Device locations Wall4X+.txt"%Folder1)

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
GroupBegin = 1243
GroupEnd = 1656
fn1 = open("%s/FDS Device locations Wall1bY-.txt"%Folder1)

exec(open("PlotDiagramMainProgram.py").read())


