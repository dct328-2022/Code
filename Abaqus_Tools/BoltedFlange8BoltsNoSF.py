import numpy as np
import matplotlib.pyplot as plt

# ================================== Input File ===========================================
InpFile = "/media/chenting/OS/Temp/BoltedFlange8BoltsSF2o.inp"
NewInpFile = "/media/chenting/OS/Temp/BoltedFlange8BoltsSF2.inp"

#InpFile = "/media/chenting/OS/Temp/BoltedFlange4BoltsSF2o.inp"
#NewInpFile = "/media/chenting/OS/Temp/BoltedFlange4BoltsSF2.inp"


# ================================== Read File ===========================================
file = open(InpFile, 'r')
file2 = open(NewInpFile, 'w')

# =================================== Predefined functions ================================
def RotationMatrix(x1, y1, z1, x2, y2, z2, s):
    ux = float(x2 - x1)
    uy = float(y2 - y1)
    uz = float(z2 - z1)
    mu = (ux*ux + uy*uy + uz*uz)**0.5
    ux = ux/mu
    uy = uy/mu
    uz = uz/mu
    term1 = 1 - np.cos(s)
    return np.array([[np.cos(s) + ux*ux*term1, ux*uy*term1 - uz*np.sin(s), ux*uz*term1 + uy*np.sin(s)], [ux*uy*term1 + uz*np.sin(s), np.cos(s) + uy*uy*term1, uy*uz*term1 - ux*np.sin(s)], [ux*uz*term1 - uy*np.sin(s), uy*uz*term1 + ux*np.sin(s), np.cos(s) + uz*uz*term1]])

def NodeTranslation(Node, TranslationVector, s=0, RotationVector=0):
    x1 = Node[0] + TranslationVector[0]
    y1 = Node[1] + TranslationVector[1]
    z1 = Node[2] + TranslationVector[2]
    if RotationVector == 0:
        return [x1, y1, z1]
    else:
        OldNode = np.array([[Node[0]], [Node[1]], [Node[2]]])
        NewNode = RotationMatrix(RotationVector[0], RotationVector[1], RotationVector[2], RotationVector[3], RotationVector[4], RotationVector[5], s).dot(OldNode) + np.array([[TranslationVector[0]],[TranslationVector[1]], [TranslationVector[2]]])
        return [NewNode[0, 0], NewNode[1, 0], NewNode[2, 0]]

class Part:
    instances = []
    def __init__(self, name):
        self.name = name
        self.NodeSet = []
        Part.instances.append(self)

    def addnode(self, n, x, y, z):
        self.NodeSet.append([n, x, y, z])

    def name(self):
        return self.name

    def nodeset(self):
        return self.NodeSet

class InterNodes:
    def __init__(self, itemname1, nodeset1, itemname2, nodeset2, condition, filename, dir, pairnum, tol=0.15):
        self.masternodes = filter(condition, nodeset1)
        self.slavenodes = []
        self.itemname1 = itemname1
        self.itemname2 = itemname2
        pairnum1 = pairnum
        tol = float(tol)
        filename.write("** ======================= Spring Elements for %s and %s =======================\n" % (itemname1, itemname2))
        for i, obj in enumerate(self.masternodes):
            temp = filter(lambda x: abs(x[1] - obj[1]) < tol/3*2 and abs(x[2] - obj[2]) < tol/3*2 and abs(x[3] - obj[3]) < tol/3*2, nodeset2)
            if len(temp) == 1:
                temp1 = temp[0]
            if len(temp) == 0:
                temp = filter(lambda x: abs(x[1] - obj[1]) < tol and abs(x[2] - obj[2]) < tol and abs(x[3] - obj[3]) < tol, nodeset2)
                if len(temp) == 1:
                    temp1 = temp[0]
                elif len(temp) == 0:
                    print("Node not found for (%d, %f, %f, %f) in pair %s and %s" % (obj[0], obj[1], obj[2], obj[3], itemname1, itemname2))
            if len(temp) > 1:
                print("may be an error")
                print("The master node is", obj)
                print("The slave node is", temp)
                temp1 = temp[0]
            self.slavenodes.append(temp1)

            if 1 in dir:
                pairnum1 += 1
                filename.write("*Element, type=Spring2, elset=XSpring\n")
                filename.write("%d, %s.%d, %s.%d\n" % (pairnum1, itemname1, obj[0], itemname2, self.slavenodes[i][0]))
            if 2 in dir:
                pairnum1 += 1
                filename.write("*Element, type=Spring2, elset=YSpring\n")
                filename.write("%d, %s.%d, %s.%d\n" % (pairnum1, itemname1, obj[0], itemname2, self.slavenodes[i][0]))
            if 3 in dir:
                pairnum1 += 1
                filename.write("*Element, type=Spring2, elset=ZSpring\n")
                filename.write("%d, %s.%d, %s.%d\n" % (pairnum1, itemname1, obj[0], itemname2, self.slavenodes[i][0]))
        self.pairnum = pairnum1

    def pairnum(self):
        return self.pairnum
    def masternodes(self):
        return self.masternodes
    def slavenodes(self):
        return self.slavenodes
    def showYZ(self):
        masternodesy = map(lambda x: x[2], self.masternodes)
        masternodesz = map(lambda x: x[3], self.masternodes)
        plt.plot(masternodesy, masternodesz, 'ro')
        plt.show()
    def showXY(self):
        masternodesx = map(lambda x: x[1], self.masternodes)
        masternodesy = map(lambda x: x[2], self.masternodes)
        plt.plot(masternodesx, masternodesy, 'ro')
        plt.show()
    def showXZ(self):
        masternodesx = map(lambda x: x[1], self.masternodes)
        masternodesz = map(lambda x: x[3], self.masternodes)
        plt.plot(masternodesx, masternodesz, 'ro')
        plt.show()
    def show(self):
        masternodesx = map(lambda x: x[1], self.masternodes)
        masternodesy = map(lambda x: x[2], self.masternodes)
        masternodesz = map(lambda x: x[3], self.masternodes)
        plt.figure(figsize=(11, 11))
        ax1 = plt.subplot(2, 2, 1)
        plt.plot(masternodesx, masternodesy, 'ro')
        plt.title("XY Plane - %s & %s" % (self.itemname1, self.itemname2))
        ax2 = plt.subplot(2, 2, 2)
        plt.plot(masternodesz, masternodesy, 'ro')
        plt.title("ZY Plane")
        ax3 = plt.subplot(2, 2, 3)
        plt.plot(masternodesx, masternodesz, 'ro')
        plt.title("XZ Plane")
        plt.show()


class Instance:
    instances = []
    def __init__(self, name, part):
        self.name = name
        self.NodeSet = []
        self.Translation = []
        self.Rotation = []
        self.part = part
        Instance.instances.append(self)

    def addnode(self, n, x, y, z):
        self.NodeSet.append([n, x, y, z])

    def definetranslation(self, x, y, z):
        self.Translation = [x, y, z]

    def definerotation(self, x1, y1, z1, x2, y2, z2, s):
        self.Rotation = [x1, y1, z1, x2, y2, z2, s]

    def translation(self):
        return self.Translation

    def rotation(self):
        return self.Rotation

    def name(self):
        return self.name

    def part(self):
        return self.part

    def nodeset(self):
        return self.NodeSet

    def transnodeset(self, partnodeset):
        if self.Translation == []:
            return partnodeset
        elif self.Rotation == []:
            return map(lambda x: [x[0]] + NodeTranslation(x[1:], self.Translation), partnodeset)
        else:
            return map(lambda x: [x[0]] + NodeTranslation(x[1:], self.Translation, self.Rotation[-1]*np.pi/180, self.Rotation[0:-1]), partnodeset)

#flag1 = 0
#flag2 = 0
flag3 = 0
#flag4 = 0
flagPart = 0
flagNode = 0
flagInstance = 0
flagPosition = 0
counter = 0

for line in file:
    # Record Parts
    if line.startswith("*Part, name="):
        name = line[12:-1]
        Part(name)
        flagPart = 1
    if flagPart == 1 and line.startswith("*Node"):
        flagNode = 1
    if flagPart == 1 and flagNode == 1:
        content = line.split(',')
        if len(content) == 4:
            Part.instances[-1].addnode(float(content[0]), float(content[1]), float(content[2]), float(content[3]))
        elif flagPart == 1 and line.startswith("*Node"):
            flagNode = 1
        else:
            flagNode = 0
    if line.startswith("*End Part"):
        flagPart = 0
        flagNode = 0

    # Record Instances
    if line.startswith("*Instance, name="):
        start = "*Instance, name="
        end = ", part="
        name = line[line.find(start)+len(start):line.rfind(end)]
        part = line[line.find(end)+len(end):-1]
        Instance(name, part)
        flagInstance = 1
        flagPosition = 1
    if flagInstance == 1 and flagPosition == 2:
        content = line.split(',')
        if len(content) == 3:
            Instance.instances[-1].definetranslation(float(content[0]), float(content[1]), float(content[2]))
        else:
            flagPosition = 0

    if flagInstance == 1 and flagPosition == 3:
        content = line.split(',')
        if len(content) == 7:
            Instance.instances[-1].definerotation(float(content[0]), float(content[1]), float(content[2]), float(content[3]), float(content[4]), float(content[5]), float(content[6]))
        else:
            flagPosition = 0

    if flagInstance == 1 and line.startswith("*Node"):
        flagNode = 1
    if flagInstance == 1 and flagNode == 1:
        content = line.split(',')
        if len(content) == 4:
            Instance.instances[-1].addnode(float(content[0]), float(content[1]), float(content[2]), float(content[3]))
        elif flagInstance == 1 and line.startswith("*Node"):
            flagNode = 1
        else:
            flagNode = 0

    if line.startswith("*End Instance"):
        flagInstance = 0
        flagNode = 0

    # ====== Find Node Pairs ====================================================================
    if line.startswith("*End Assembly"):
        # Print parts and instances
        print("Parts:\n")
        for item in Part.instances:
            print(item.name)

        print("==================================")
        print("Instances:\n")
        print(len(Instance.instances))
        for item in Instance.instances:
            if item.translation() == []:
                print(item.name, "No", "No")
            elif item.rotation() == []:
                print(item.name, "Yes", "No")
            else:
                print(item.name, "Yes", "Yes")

        # Begin to find nodes
        PairCounter = 0

        # Find Part and instances
        SteelPlatePart = filter(lambda x: x.name.startswith("Bolt8NoSF"), Part.instances)[0]
        SteelPlate1 = filter(lambda x: x.name == "Bolt8NoSF-1", Instance.instances)[0]
        SteelPlate2 = filter(lambda x: x.name == "Bolt8NoSF-2", Instance.instances)[0]
        SteelPlate1NodeSet = SteelPlate1.transnodeset(SteelPlatePart.nodeset())
        SteelPlate2NodeSet = SteelPlate2.transnodeset(SteelPlatePart.nodeset())

        # Define Spring in three directions
        file2.write("*Spring, Nonlinear, elset=ZSpring\n")
        file2.write("3, 3\n")
        file2.write("-0.1, -10.0\n")
        file2.write("-0.05, -5.0\n")
        file2.write("-0.02, -2.0\n")
        file2.write("-0.01, -1.0\n")
        file2.write("0, 0.0\n")
        file2.write("1000.0, 1.0\n")
        file2.write("5000.0, 5.0\n")

        # ========================= Processing Steel Plates ===========================================
        file2.write("** ================================ Springs ==============================\n")
        for i, obji in enumerate(SteelPlate1NodeSet):
            for j, objj in enumerate(SteelPlate2NodeSet):
                if abs(obji[1] - objj[1]) < 0.1 and abs(obji[2] - objj[2]) < 0.1 and 5.8 < obji[3] - objj[3] < 6.1 and (obji[1] - 68)**2 + (obji[2] - 25)**2 > 6.1**2 and (obji[1] - 25)**2 + (obji[2] - 68)**2 > 6.1**2:
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelPlate2.name, objj[0], SteelPlate1.name, obji[0]))

    if flag3 == 0:
        file2.write(line)

    if flagPosition >= 3:
        flagPosition = 0

    if flagPosition >= 1 and flagPosition < 3:
        flagPosition = flagPosition + 1

    # end of each line
    flag3 = 0


file.close()
file2.close()


newnode = NodeTranslation([7.34731579, 53, -10.1127129], [-345, 1110.0, 47], 2*np.pi/3, [-345, 1110.0, 47, -344.42265, 1109.42265, 47.57735])
print(newnode)
