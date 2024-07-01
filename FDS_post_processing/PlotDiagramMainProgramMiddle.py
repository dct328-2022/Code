import matplotlib.font_manager as fm
import matplotlib.lines as mlines
import matplotlib as mpl

legend_handles = []
legend_labels = []

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

df = pd.read_csv(path + '/' + folder + '/' + filename, header=1)
dataset2 = open(filename2, 'r')

TempreN = []
TempreT = []
TimeS = int(TimeSelected/60)
for line in dataset2:
    lines = line.split()
    if len(lines) > 0:
        temp1 = int(lines[0])
        temp2 = float(lines[TimeS+1])
        TempreN.append(temp1)
        TempreT.append(temp2)

DeviceNo = []
for i, obj in enumerate(df.keys()):
    if obj != 'Time':
        if i in TempreN:
            DeviceNo.append(int(obj))

print(DeviceNo)

Coordinates = []
Xp = []
Yp = []
for content in fn1:
    line = content.split()
    if len(line) == 5:
        if int(line[0]) in DeviceNo:
            NodeTempr(int(line[0]), float(line[1]), float(line[2]), float(line[3]))
            NodeTempr.instances[-1].surfacedirection(line[4])

fn1.close()
print("NodeTempr")
print(len(NodeTempr.instances))

# Assign temperature to node instances

for i, obj in enumerate(NodeTempr.instances):
    obj.addtempr(TempreT[i])

print("%d points in total" % len(NodeTempr.instances))

# Grouping and Ploting Diagrams

fontpath = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
fontprop = fm.FontProperties(family='Arial', fname=fontpath, size=16)
mpl.rcParams['font.family'] = ['serif']
mpl.rcParams['font.serif'] = ['Arial']
mpl.rcParams.update({'font.size': 16, 'font.family': 'Arial'})

plt.figure(figsize=(14, 7))

lens = len(TemperatureGradient)
maxtempr = 0
for j, item in enumerate(TemperatureGradient):
    if j == 0:
        NodeList = list(filter(lambda xx: xx.tempr>=item, NodeTempr.instances))
        Xplot = list(map(lambda xx: xx.xp, NodeList))
        Yplot = list(map(lambda xx: xx.yp, NodeList))

    else:
        NodeList = list(filter(lambda xx: xx.tempr>=item and xx.tempr<TemperatureGradient[j-1], NodeTempr.instances))
        Xplot = list(map(lambda xx: xx.xp, NodeList))
        Yplot = list(map(lambda xx: xx.yp, NodeList))

    colorused = 250.0/lens*j
    colorused = HSV2RGB(colorused, 1.0, 1.0)
    
    handle = mlines.Line2D([], [], color=colorused, marker='o', linestyle='None', markersize=10) # Adjust marker as needed
    legend_handles.append(handle)

    if j > 0:
        label = f"{TemperatureGradient[j-1]} - {item}°C"
    else:
        label = f"Above {item}°C"
    legend_labels.append(label)
    
    if item >= 300:
        plt.scatter(Xplot, Yplot, color=colorused, marker='P')
    elif item >= 117:
        plt.scatter(Xplot, Yplot, color=colorused, marker='^')
    else:
        plt.scatter(Xplot, Yplot, color=colorused, marker='o')
    lens2 = len(Xplot)
    if j>0:
        print("%d points between temperature %f and %f" % (lens2, TemperatureGradient[j-1], item))
    else:
        print("%d points above temperature %f" % (lens2, item))

NodeList = list(filter(lambda xx: xx.tempr<TemperatureGradient[-1], NodeTempr.instances))
Xplot = list(map(lambda xx: xx.xp, NodeList))
Yplot = list(map(lambda xx: xx.yp, NodeList))
colorused = HSV2RGB(250.0, 1.0, 1.0)
plt.scatter(Xplot, Yplot, color=colorused)
plt.gcf().set_size_inches(12, 4)
if part == 'ceiling':
    plt.xlim(0, 12.5)
    plt.ylim(3.8, 7.5)
    plt.xticks([0, 2, 4, 6, 8, 10, 12, 12.5], ['0', '2', '4', '6', '8', '10', '12', '12.5'], fontproperties=fontprop)
    plt.yticks([3.8, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5], fontproperties=fontprop)
elif part == 'wall3by-':
    plt.xlim(2.5, 12.5)
    plt.ylim(0, 2.5)
    plt.xticks([2.5, 4, 6, 8, 10, 12, 12.5], ['2.5', '4', '6', '8', '10', '12', '12.5'], fontproperties=fontprop)
    plt.yticks([0, 0.5, 1, 1.5, 2, 2.5], fontproperties=fontprop)
lens2 = len(Xplot) 
print("%d points below temperature %f" % (lens2, TemperatureGradient[-1]))

plt.legend(handles=legend_handles, labels=legend_labels, loc='upper left', bbox_to_anchor=(1.05, 1)) # You can change the location
plt.tight_layout()
plt.gca().set_aspect('equal')
plt.show()
