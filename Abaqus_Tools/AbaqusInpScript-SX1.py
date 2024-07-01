import numpy as np
import matplotlib.pyplot as plt

# ================================== Input File ===========================================
InpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SX1.inp"
NewInpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SX1g.inp"

# ================================== Read File ===========================================
file = open(InpFile, 'r')
file2 = open(NewInpFile, 'w')

# ================================== Elements to be find =================================
eles = [5453, 5561, 5554, 5560, 5559, 5558, 5557, 5556, 5555, 5452, 5468,5654, 5647, 5653, 5652, 5651, 5650, 5649, 5648, 5467]

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

class InterNodes:
    def __init__(self, itemname1, nodeset1, itemname2, nodeset2, condition, filename, dir, pairnum):
        self.masternodes = filter(condition, nodeset1)
        self.slavenodes = []
        pairnum1 = pairnum
        filename.write("** ======================= Spring Elements for %s and %s =======================\n" % (itemname1, itemname2))
        for i, obj in enumerate(self.masternodes):
            temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1,
                          nodeset2)
            if len(temp) == 1:
                temp1 = temp[0]
            if len(temp) == 0:
                temp = filter(
                    lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15,
                    nodeset2)
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



flag1 = 0
flag2 = 0
flag3 = 0
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

    # Find Specified Elements in SteelTubeV3
    if "SteelTubeV3" in line:
        flag1 = 1
    if "Element," in line and flag1 == 1:
        flag2 = 1
    if "End Part" in line and flag1 == 1 and flag2 == 1:
        flag1 = 0
        flag2 = 0
    if flag1 == 1 and flag2 == 1:
        for item in eles:
            itemn = str(item) + ','
            if line.startswith(itemn):
                flag3 = 1
                counter += 1

    # ====== Find Node Pairs ====================================================================
    if line.startswith("*End Assembly"):
        PairCounter = 0
        SteelRodSet = filter(lambda x: x.part.startswith("SteelRod"), Instance.instances)
        ConcreteCore = filter(lambda x: x.name == "ConcreteCore-1", Instance.instances)[0]
        # Define Spring in three directions
        file2.write("*Spring, elset=XSpring\n")
        file2.write("1, 1\n")
        file2.write("1e+07\n")
        file2.write("*Spring, elset=YSpring\n")
        file2.write("2, 2\n")
        file2.write("1e+07\n")
        file2.write("*Spring, elset=ZSpring\n")
        file2.write("3, 3\n")
        file2.write("1e+07\n")

        # Find SteelRods, SteelRod is an independent instance
        for item in SteelRodSet:
            # Processing SteelRod-1
            if item.name.startswith("SteelRod-1") and len(item.name) == 10:
                NodePairy = []
                NodePairz = []
                # Length of Node Set
                numnodes = len(item.nodeset())
                # Node Set after coordinate transformation
                tempnodeset = []
                # Coordinate Transformation
                for i in range(0, numnodes):
                    tempnodeset.append([int(item.nodeset()[i][0])] + NodeTranslation(item.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))

                for i in range(0, numnodes):
                    # Condition 1: Y=1592.5 and Z=133.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1592.5) < 0.3 and abs(tempnodeset[i][3] - 133.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 2: Y=1567.5 and Z=133.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1567.5) < 0.3 and abs(tempnodeset[i][3] - 133.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1580 and Z=120.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1580) < 0.3 and abs(tempnodeset[i][3] - 120.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1580 and Z=145.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1580) < 0.3 and abs(tempnodeset[i][3] - 145.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                # Write command to file
                file2.write("** ====================== Spring Elements for %s ====================\n" % item.name)
                for ci, obj in enumerate(NodePairy):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))
                for ci, obj in enumerate(NodePairz):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))

            # Processing SteelRod-1-lin-1-2
            if item.name == "SteelRod-1-lin-1-2":
                NodePairy = []
                NodePairz = []
                # Length of Node Set
                numnodes = len(item.nodeset())
                # Node Set after coordinate transformation
                tempnodeset = []
                # Coordinate Transformation
                for i in range(0, numnodes):
                    tempnodeset.append([int(item.nodeset()[i][0])] + NodeTranslation(item.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))

                for i in range(0, numnodes):
                    # Condition 1: Y=1122.5 and Z=133.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1122.5) < 0.3 and abs(tempnodeset[i][3] - 133.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 2: Y=1097.5 and Z=133.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1097.5) < 0.3 and abs(tempnodeset[i][3] - 133.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1110 and Z=120.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1110) < 0.3 and abs(tempnodeset[i][3] - 120.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1110 and Z=145.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1110) < 0.3 and abs(tempnodeset[i][3] - 145.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                # Write command to file
                file2.write("** ===================== Spring Elements for %s =============================\n" % item.name)
                for ci, obj in enumerate(NodePairy):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))
                for ci, obj in enumerate(NodePairz):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))

            # Processing SteelRod-1-lin-2-1
            if item.name == "SteelRod-1-lin-2-1":
                NodePairy = []
                NodePairz = []
                # Length of Node Set
                numnodes = len(item.nodeset())
                # Node Set after coordinate transformation
                tempnodeset = []
                # Coordinate Transformation
                for i in range(0, numnodes):
                    tempnodeset.append([int(item.nodeset()[i][0])] + NodeTranslation(item.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))

                for i in range(0, numnodes):
                    # Condition 1: Y=1592.5 and Z=47.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1592.5) < 0.3 and abs(tempnodeset[i][3] - 47.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 2: Y=1567.5 and Z=47.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1567.5) < 0.3 and abs(tempnodeset[i][3] - 47.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1580 and Z=34.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1580) < 0.3 and abs(tempnodeset[i][3] - 34.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1580 and Z=59.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1580) < 0.3 and abs(tempnodeset[i][3] - 59.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                # Write command to file
                file2.write("** ======================== Spring Elements for %s ==========================\n" % item.name)
                for ci, obj in enumerate(NodePairy):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))
                for ci, obj in enumerate(NodePairz):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))

            # Processing SteelRod-1-lin-2-2
            if item.name == "SteelRod-1-lin-2-2":
                NodePairy = []
                NodePairz = []
                # Length of Node Set
                numnodes = len(item.nodeset())
                # Node Set after coordinate transformation
                tempnodeset = []
                # Coordinate Transformation
                for i in range(0, numnodes):
                    tempnodeset.append([int(item.nodeset()[i][0])] + NodeTranslation(item.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))

                for i in range(0, numnodes):
                    # Condition 1: Y=1122.5 and Z=47.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1122.5) < 0.3 and abs(tempnodeset[i][3] - 47.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 2: Y=1097.5 and Z=47.0. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1097.5) < 0.3 and abs(tempnodeset[i][3] - 47.0) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairy.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1110 and Z=34.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1110) < 0.3 and abs(tempnodeset[i][3] - 34.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                    # Condition 3: Y=1110 and Z=59.5. Find All nodes conforming this condition
                    if abs(tempnodeset[i][2] - 1110) < 0.3 and abs(tempnodeset[i][3] - 59.5) < 0.3:
                        temp = filter(lambda x: abs(ConcreteCore.nodeset()[x][1] - tempnodeset[i][1]) < 0.3 and abs(ConcreteCore.nodeset()[x][2] - tempnodeset[i][2]) < 0.3 and abs(ConcreteCore.nodeset()[x][3] - tempnodeset[i][3]) < 0.3, range(0, len(ConcreteCore.nodeset())))
                        if len(temp) == 1:
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])
                        elif len(temp) > 1:
                            print("May be an error")
                            for obj in temp:
                                print(tempnodeset[i], ConcreteCore.nodeset()[obj])
                            NodePairz.append([tempnodeset[i][0], int(ConcreteCore.nodeset()[temp[0]][0])])

                # Write command to file
                file2.write("** ========================= Spring Elements for %s ===========================\n" % item.name)
                for ci, obj in enumerate(NodePairy):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))
                for ci, obj in enumerate(NodePairz):
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, ConcreteCore-1.%d\n" % (PairCounter, item.name, obj[0], obj[1]))

        # Bond Fillet Welds, FilletWeld is an dependent instance
        FilletWeldSet = filter(lambda x: x.part.startswith('''"FilletWeld v4'''), Instance.instances)
        ColumnTube = filter(lambda x: x.name == "SteelTubeV3-1", Instance.instances)[0]
        FilletWeldPart = filter(lambda x: x.name.startswith('''"FilletWeld v4'''), Part.instances)[0]
        SteelTubePart = filter(lambda x: x.name.startswith("SteelTubeV3"), Part.instances)[0]
        numnodes = len(FilletWeldPart.nodeset())
        for item in FilletWeldSet:
            if item.name == '''"FilletWeld v4-1"''':
                def BoundFunction(x):
                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1529.9 <= x[2] <= 1630.1
                    BoundZ = 174.9 <= x[3] <= 178.4 or 1.6 <= x[3] <= 5.1
                    condition1 = BoundX and BoundY and BoundZ

                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1629.9 <= x[2] <= 1633.4
                    BoundZ = 4.9 <= x[3] <= 175.1
                    condition2 = BoundX and BoundY and BoundZ

                    if condition1 or condition2:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    #tempnodeset.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                    tempnodeset.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], item.translation()))
                masternodes = filter(BoundFunction, tempnodeset)

                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''"FilletWeld v4-1-lin-1-2"''':
                def BoundFunction(x):
                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1059.9 <= x[2] <= 1160.1
                    BoundZ = 174.9 <= x[3] <= 178.4 or 1.6 <= x[3] <= 5.1
                    condition1 = BoundX and BoundY and BoundZ

                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1056.6 <= x[2] <= 1060.1
                    BoundZ = 4.9 <= x[3] <= 175.1
                    condition2 = BoundX and BoundY and BoundZ

                    if condition1 or condition2:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''"FilletWeld v4-2"''':
                def BoundFunction(x):
                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1529.9 <= x[2] <= 1630.1
                    BoundZ = 174.9 <= x[3] <= 178.4 or 1.6 <= x[3] <= 5.1
                    condition1 = BoundX and BoundY and BoundZ

                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1629.9 <= x[2] <= 1633.4
                    BoundZ = 4.9 <= x[3] <= 175.1
                    condition2 = BoundX and BoundY and BoundZ

                    if condition1 or condition2:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''"FilletWeld v4-2-lin-1-2"''':
                def BoundFunction(x):
                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1059.9 <= x[2] <= 1160.1
                    BoundZ = 174.9 <= x[3] <= 178.4 or 1.6 <= x[3] <= 5.1
                    condition1 = BoundX and BoundY and BoundZ

                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1056.6 <= x[2] <= 1060.1
                    BoundZ = 4.9 <= x[3] <= 175.1
                    condition2 = BoundX and BoundY and BoundZ

                    if condition1 or condition2:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

        # ========================= Add fillet weld for fin plate ============================================================
        FilletWeld2Set = filter(lambda x: x.part.startswith('''FilletWeldFinPlate'''), Instance.instances)
        FilletWeld2Part = filter(lambda x: x.name.startswith('''FilletWeldFinPlate'''), Part.instances)[0]
        numnodes = len(FilletWeld2Part.nodeset())
        for item in FilletWeld2Set:
            if item.name == '''FilletWeldFinPlate-2''':
                def BoundFunction(x):
                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1214.9 <= x[2] <= 1475.1
                    BoundZ = 102.9 <= x[3] <= 106.4
                    condition1 = BoundX and BoundY and BoundZ

                    if condition1:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeld2Part.nodeset()[i][0])] + NodeTranslation(FilletWeld2Part.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''FilletWeldFinPlate-1''':
                def BoundFunction(x):
                    BoundX = abs(x[1] + 410) < 0.1
                    BoundY = 1214.9 <= x[2] <= 1475.1
                    BoundZ = 89.6 <= x[3] <= 93.1
                    condition1 = BoundX and BoundY and BoundZ

                    if condition1:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeld2Part.nodeset()[i][0])] + NodeTranslation(FilletWeld2Part.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''FilletWeldFinPlate-3''':
                def BoundFunction(x):
                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1214.9 <= x[2] <= 1475.1
                    BoundZ = 89.6 <= x[3] <= 93.1
                    condition1 = BoundX and BoundY and BoundZ

                    if condition1:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeld2Part.nodeset()[i][0])] + NodeTranslation(FilletWeld2Part.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

            if item.name == '''FilletWeldFinPlate-4''':
                def BoundFunction(x):
                    BoundX = abs(x[1] - 30) < 0.1
                    BoundY = 1214.9 <= x[2] <= 1475.1
                    BoundZ = 102.9 <= x[3] <= 106.4
                    condition1 = BoundX and BoundY and BoundZ

                    if condition1:
                        return True
                    else:
                        return False

                tempnodeset = []
                for i in range(0, numnodes):
                    tempnodeset.append([int(FilletWeld2Part.nodeset()[i][0])] + NodeTranslation(FilletWeld2Part.nodeset()[i][1:], item.translation(), item.rotation()[-1]*np.pi/180, item.rotation()[0:-1]))
                masternodes = filter(BoundFunction, tempnodeset)
                slavenodes = []
                file2.write("** ======================= Spring Elements for %s =======================\n" % item.name)
                for i, obj in enumerate(masternodes):
                    temp = filter(lambda x: abs(x[1] - obj[1]) < 0.1 and abs(x[2] - obj[2]) < 0.1 and abs(x[3] - obj[3]) < 0.1, SteelTubePart.nodeset())
                    if len(temp) == 1:
                        temp1 = temp[0]
                    if len(temp) == 0:
                        temp = filter(lambda x: abs(x[1] - obj[1]) < 0.15 and abs(x[2] - obj[2]) < 0.15 and abs(x[3] - obj[3]) < 0.15, SteelTubePart.nodeset())
                        if len(temp) == 1:
                            temp1 = temp[0]
                        elif len(temp) == 0:
                            print("Node not found for (%d, %f, %f, %f)" % (obj[0], obj[1], obj[2], obj[3]))
                    if len(temp) > 1:
                        print("may be an error")
                        print("The master node is", obj)
                        print("The slave node is", temp)
                        temp1 = temp[0]
                    slavenodes.append(temp1)

                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=XSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpring\n")
                    file2.write("%d, %s.%d, SteelTubeV3-1.%d\n" % (PairCounter, item.name, obj[0], slavenodes[i][0]))

        # ======================================== Fillet Weld to Flange Cleat =========================================
        FlangeCleatPart = filter(lambda x: x.name.startswith("FlangeCleatV2"), Part.instances)[0]
        FlangeCleat2 = filter(lambda x: x.name.startswith("FlangeCleatV2-2"), Instance.instances)[0]
        FlangeCleat1 = filter(lambda x: x.name.startswith("FlangeCleatV2-1"), Instance.instances)[0]
        FlangeCleat3 = filter(lambda x: x.name.startswith("FlangeCleatV2-3"), Instance.instances)[0]
        FlangeCleat4 = filter(lambda x: x.name.startswith("FlangeCleatV2-4"), Instance.instances)[0]
        FilletWeldv41 = filter(lambda x: x.name.startswith('''"FilletWeld v4-1"'''), FilletWeldSet)[0]
        FilletWeldv42 = filter(lambda x: x.name.startswith('''"FilletWeld v4-2"'''), FilletWeldSet)[0]
        FilletWeldv41lin1 = filter(lambda x: x.name.startswith('''"FilletWeld v4-1-lin-1-2"'''), FilletWeldSet)[0]
        FilletWeldv42lin1 = filter(lambda x: x.name.startswith('''"FilletWeld v4-2-lin-1-2"'''), FilletWeldSet)[0]

        nodenum = len(FlangeCleatPart.nodeset())
        FlangeCleat2NodeSet = []
        FlangeCleat1NodeSet = FlangeCleatPart.nodeset()
        FlangeCleat3NodeSet = []
        FlangeCleat4NodeSet = []
        for i in range(0, nodenum):
            FlangeCleat2NodeSet.append([int(FlangeCleatPart.nodeset()[i][0])] + NodeTranslation(FlangeCleatPart.nodeset()[i][1:], FlangeCleat2.translation(), FlangeCleat2.rotation()[-1] * np.pi / 180, FlangeCleat2.rotation()[0:-1]))
            FlangeCleat3NodeSet.append([int(FlangeCleatPart.nodeset()[i][0])] + NodeTranslation(FlangeCleatPart.nodeset()[i][1:], FlangeCleat3.translation(), FlangeCleat3.rotation()[-1] * np.pi / 180, FlangeCleat3.rotation()[0:-1]))
            FlangeCleat4NodeSet.append([int(FlangeCleatPart.nodeset()[i][0])] + NodeTranslation(FlangeCleatPart.nodeset()[i][1:], FlangeCleat4.translation(), FlangeCleat4.rotation()[-1] * np.pi / 180, FlangeCleat4.rotation()[0:-1]))

        numnodes = len(FilletWeldPart.nodeset())
        FilletWeldv41NodeSet = []
        FilletWeldv42NodeSet = []
        FilletWeldv41lin1NodeSet = []
        FilletWeldv42lin1NodeSet = []

        for i in range(0, numnodes):
            FilletWeldv41NodeSet.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], FilletWeldv41.translation()))
            FilletWeldv42NodeSet.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], FilletWeldv42.translation(), FilletWeldv42.rotation()[-1] * np.pi / 180, FilletWeldv42.rotation()[0:-1]))
            FilletWeldv41lin1NodeSet.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], FilletWeldv41lin1.translation(), FilletWeldv41lin1.rotation()[-1] * np.pi / 180, FilletWeldv41lin1.rotation()[0:-1]))
            FilletWeldv42lin1NodeSet.append([int(FilletWeldPart.nodeset()[i][0])] + NodeTranslation(FilletWeldPart.nodeset()[i][1:], FilletWeldv42lin1.translation(), FilletWeldv42lin1.rotation()[-1] * np.pi / 180, FilletWeldv42lin1.rotation()[0:-1]))


        def BoundFunction(x):
            BoundX = 29.9 <= x[1] <= 33.4
            BoundY = 1519.8 <= x[2] <= 1630.1
            BoundZ = 174.9 <= x[3] <= 175.1 or 4.9 <= x[3] <= 5.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = 29.9 <= x[1] <= 33.4
            BoundY = 1629.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False
        FWv41FC2 = InterNodes(FilletWeldv41.name, FilletWeldv41NodeSet, FlangeCleat2.name, FlangeCleat2NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWv41FC2.pairnum
        FWv41FC2.showYZ()

        def BoundFunction(x):
            BoundX = -413.4 <= x[1] <= -409.9
            BoundY = 1519.8 <= x[2] <= 1630.1
            BoundZ = 174.9 <= x[3] <= 175.1 or 4.9 <= x[3] <= 5.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -413.4 <= x[1] <= -409.9
            BoundY = 1629.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False
        FWv42FC1 = InterNodes(FilletWeldv42.name, FilletWeldv42NodeSet, FlangeCleat1.name, FlangeCleat1NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWv42FC1.pairnum
        FWv42FC1.showYZ()

        def BoundFunction(x):
            BoundX = -413.4 <= x[1] <= -409.9
            BoundY = 1059.9 <= x[2] <= 1170.1
            BoundZ = 174.9 <= x[3] <= 175.1 or 4.9 <= x[3] <= 5.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -413.4 <= x[1] <= -409.9
            BoundY = 1059.9 <= x[2] <= 1060.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False
        FWv42linFC3 = InterNodes(FilletWeldv42lin1.name, FilletWeldv42lin1NodeSet, FlangeCleat3.name, FlangeCleat3NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWv42linFC3.pairnum
        FWv42linFC3.showYZ()

        def BoundFunction(x):
            BoundX = 29.9 <= x[1] <= 33.4
            BoundY = 1059.9 <= x[2] <= 1170.1
            BoundZ = 174.9 <= x[3] <= 175.1 or 4.9 <= x[3] <= 5.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = 29.9 <= x[1] <= 33.4
            BoundY = 1059.9 <= x[2] <= 1060.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False
        FWv41linFC4 = InterNodes(FilletWeldv41lin1.name, FilletWeldv41lin1NodeSet, FlangeCleat4.name, FlangeCleat4NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWv41linFC4.pairnum
        FWv41linFC4.showYZ()

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
for item in Part.instances:
    print(item.name)

print("==================================")
print(len(Instance.instances))
for item in Instance.instances:
    print(item.name)

newnode = NodeTranslation([7.34731579, 53, -10.1127129], [-345, 1110.0, 47], 2*np.pi/3, [-345, 1110.0, 47, -344.42265, 1109.42265, 47.57735])
print(newnode)