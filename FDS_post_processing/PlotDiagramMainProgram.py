import matplotlib.font_manager as fm
import matplotlib.lines as mlines
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt

# Do you want to write the plot data to file?
WriteData = True
wfn = open("DataExport.txt", 'w')

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

Coordinates = []
Xp = []
Yp = []

for content in fn1:
    line = content.split()
    if len(line) == 5:
        if int(line[0]) >= GroupBegin and int(line[0]) <= GroupEnd:
            NodeTempr(int(line[0]), float(line[1]), float(line[2]), float(line[3]))
            NodeTempr.instances[-1].surfacedirection(line[4])

fn1.close()
print("NodeTempr")
print(len(NodeTempr.instances))

# Create lists of xp and yp values
xp_values = []
yp_values = []
for node in NodeTempr.instances:
    xp_values.append(node.xp)
    yp_values.append(node.yp)

# Remove duplicates by converting to set and then back to list
xp_values = list(set(xp_values))
yp_values = list(set(yp_values))

# Sort the lists
xp_values.sort()
yp_values.sort()

# Keep every second value
xp_values = xp_values[::2]
yp_values = yp_values[::2]

# Continue with your original code
df = pd.read_csv(path + '/' + folder + '/' + filename, header=1)

for i, obj in enumerate(df.keys()):
    if not FireT:
        if obj != 'Time':
            if int(obj)== GroupBegin:
                BeginDeviceIndex = i
            if int(obj)== GroupEnd:
                EndDeviceIndex = i
    if FireT:
        if obj != 'Time' and obj != 'FireT':
            if int(obj)== GroupBegin:
                BeginDeviceIndex = i
            if int(obj)== GroupEnd:
                EndDeviceIndex = i

if type(TimeSelected) != str:
    TimeSelected2 = min(df['Time'], key=lambda x: abs(x-TimeSelected))
    print("The selected time is %f" % TimeSelected2)
    TimeIndex = df[df['Time']==TimeSelected2].index.values[0]
    Tempr = df[df['Time']==TimeSelected2].values[0][BeginDeviceIndex:(EndDeviceIndex+1)]
elif TimeSelected == 'max':
    Tempr = df.max()[BeginDeviceIndex:(EndDeviceIndex+1)].values

# Assign temperature to node instances

for i, obj in enumerate(NodeTempr.instances):
    obj.addtempr(Tempr[i])
    if WriteData:
        wfn.write("%f %f %f\n"%(obj.xp, obj.yp, Tempr[i]))

print("%d points in total" % len(NodeTempr.instances))

# Grouping and Ploting Diagrams
fontpath = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
fontprop = fm.FontProperties(family='Arial', fname=fontpath, size=16)
mpl.rcParams['font.family'] = ['serif']
mpl.rcParams['font.serif'] = ['Arial']
mpl.rcParams.update({'font.size': 16, 'font.family': 'Arial'})
plt.figure(figsize=(14, 7))

lens = len(TemperatureGradient)
countdecomp = 0
countglatrans = 0
legend_handles = []
legend_temperatures = list(range(300, 50, -50))

for j, item in enumerate(TemperatureGradient):
    if j == 0:
        NodeList = [node for node in NodeTempr.instances if node.tempr >= item and node.xp in xp_values and node.yp in yp_values]
        Xplot = list(map(lambda xx: xx.xp, NodeList))
        Yplot = list(map(lambda xx: xx.yp, NodeList))
    else:
        NodeList = [node for node in NodeTempr.instances if item <= node.tempr < TemperatureGradient[j-1] and node.xp in xp_values and node.yp in yp_values]
        Xplot = list(map(lambda xx: xx.xp, NodeList))
        Yplot = list(map(lambda xx: xx.yp, NodeList))
    colorused = 250.0/lens*j
    colorused = HSV2RGB(colorused, 1.0, 1.0)
    marker = 'o'
    marker = 'o'
    if item >= 300:
        marker = '+'
    elif item >= 117:
        marker = '^'

    if item in legend_temperatures:
        handle = mlines.Line2D([], [], color=colorused, marker=marker, linestyle='None', markersize=10, label=f'{item}°C', fillstyle='none')
        legend_handles.append(handle)
    if item >= 300:
        plt.scatter(Xplot, Yplot, color=colorused, marker=marker)
        countdecomp = len(Xplot)
    elif item >= 117:
        plt.scatter(Xplot, Yplot, edgecolors=colorused, marker=marker, facecolors='none')
        countglatrans = len(Xplot)
    else:
        plt.scatter(Xplot, Yplot, edgecolors=colorused, marker=marker, facecolors='none')
    lens2 = len(Xplot)
    if j>0:
        print("%d points between temperature %f and %f" % (lens2, TemperatureGradient[j-1], item))
    else:
        print("%d points above temperature %f" % (lens2, item))

max_tempr = max(instance.tempr for instance in NodeTempr.instances)
print("Max temperature", max_tempr)

plt.legend(handles=legend_handles, loc='center left', bbox_to_anchor=(1, 0.5))
NodeList = [node for node in NodeTempr.instances if node.tempr < TemperatureGradient[-1] and node.xp in xp_values and node.yp in yp_values]
Xplot = list(map(lambda xx: xx.xp, NodeList))
Yplot = list(map(lambda xx: xx.yp, NodeList))
colorused = HSV2RGB(250.0, 1.0, 1.0)
plt.scatter(Xplot, Yplot, edgecolors=colorused, facecolors='none')
plt.gcf().set_size_inches(12, 4)
if part == 'ceiling':
    plt.xlim(0, 12.5)
    plt.ylim(3.8, 7.5)
    xtickslist = [0, 2, 4, 6, 8, 10, 12.5]
    xmarklist = [str(round(xnum - xdrift, 2)) for xnum in xtickslist]
    plt.xticks(xtickslist, xmarklist, fontproperties=fontprop)
    ytickslist = [3.8, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5]
    ymarklist = [str(round(ynum - ydrift, 2)) for ynum in ytickslist]
    plt.yticks(ytickslist, ymarklist, fontproperties=fontprop)
elif part == 'wall3by-':
    plt.xlim(2.5, 12.5)
    plt.ylim(0, 2.5)
    plt.xticks([2.5, 4, 6, 8, 10, 12, 12.5], ['2.5', '4', '6', '8', '10', '12', '12.5'], fontproperties=fontprop)
    plt.yticks([0, 0.5, 1, 1.5, 2, 2.5], fontproperties=fontprop)

lens2 = len(Xplot) 
print("%d points below temperature %f" % (lens2, TemperatureGradient[-1]))
print('===================================')
print('%d nodes > 300'%countdecomp)
print('%d nodes > 117'%countglatrans)
plt.gca().set_aspect('equal')
plt.subplots_adjust(right=0.7)  # Adjust the right margin
plt.show()
