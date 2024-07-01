import numpy as np
import matplotlib.pyplot as plt

# ================================== Input File ===========================================
InpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SX2-2o.inp"
NewInpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SX2-2.inp"

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


# ============================== Main Program begins here ==================================
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
    # Find Specified Elements in SteelTubeV3
    '''if "SteelTubeV3" in line:
        flag1 = 1
    if "Element," in line and flag1 == 1:
        flag2 = 1
    if "End Part" in line and flag1 == 1 and flag2 == 1:
        flag1 = 0
        flag2 = 0
    if flag4 == 1:
        flag3 = 1
        flag4 = 0
    if flag1 == 1 and flag2 == 1:
        for item in eles:
            itemn = str(item) + ','
            telength = len(line.split(","))
            if line.startswith(itemn) and telength > 12:
                flag3 = 1
                counter += 1
                flag4 = 1'''

    # ====== Find Node Pairs ====================================================================
    if line.startswith("*End Assembly"):
        # Print parts and instances
        for item in Part.instances:
            print(item.name)

        print("==================================")
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
        SteelRodPart = filter(lambda x: x.name.startswith("SteelRodBody"), Part.instances)[0]
        SteelRod1 = filter(lambda x: x.name == "SteelRodBody-1", Instance.instances)[0]
        SteelRod2 = filter(lambda x: x.name == "SteelRodBody-1-lin-1-2", Instance.instances)[0]
        SteelRod3 = filter(lambda x: x.name == "SteelRodBody-1-lin-2-1", Instance.instances)[0]
        SteelRod4 = filter(lambda x: x.name == "SteelRodBody-1-lin-2-2", Instance.instances)[0]
        SteelRod1NodeSet = SteelRod1.transnodeset(SteelRodPart.nodeset())
        SteelRod2NodeSet = SteelRod2.transnodeset(SteelRodPart.nodeset())
        SteelRod3NodeSet = SteelRod3.transnodeset(SteelRodPart.nodeset())
        SteelRod4NodeSet = SteelRod4.transnodeset(SteelRodPart.nodeset())

        ConcreteCore = filter(lambda x: x.name == "ConcreteCore-1", Instance.instances)[0]
        ConcreteCorePart = filter(lambda x: x.name.startswith("ConcreteCore"), Part.instances)[0]
        ConcreteCoreNodeSet = ConcreteCore.transnodeset(ConcreteCorePart.nodeset())

        FinPlatePart = filter(lambda x: x.name.startswith('''"Column1 v144-186"'''), Part.instances)[0]
        FinPlate1 = filter(lambda x: x.name == '''"Column1 v144-186-1"''', Instance.instances)[0]
        FinPlate2 = filter(lambda x: x.name == '''"Column1 v144-186-2"''', Instance.instances)[0]
        FinPlate1NodeSet = FinPlate1.transnodeset(FinPlatePart.nodeset())
        FinPlate2NodeSet = FinPlate2.transnodeset(FinPlatePart.nodeset())

        SteelTubePart = filter(lambda x: x.name.startswith("SteelTubeV3"), Part.instances)[0]
        SteelTube = filter(lambda x: x.name == "SteelTubeV3-1", Instance.instances)[0]
        SteelTubeNodeSet = SteelTube.transnodeset(SteelTubePart.nodeset())

        FlangeCleatPart = filter(lambda x: x.name.startswith("FlangeCleatV2"), Part.instances)[0]
        FlangeCleat1 = filter(lambda x: x.name == "FlangeCleatV2-1", Instance.instances)[0]
        FlangeCleat2 = filter(lambda x: x.name == "FlangeCleatV2-2", Instance.instances)[0]
        FlangeCleat3 = filter(lambda x: x.name == "FlangeCleatV2-3", Instance.instances)[0]
        FlangeCleat4 = filter(lambda x: x.name == "FlangeCleatV2-4", Instance.instances)[0]
        FlangeCleat1NodeSet = FlangeCleat1.transnodeset(FlangeCleatPart.nodeset())
        FlangeCleat2NodeSet = FlangeCleat2.transnodeset(FlangeCleatPart.nodeset())
        FlangeCleat3NodeSet = FlangeCleat3.transnodeset(FlangeCleatPart.nodeset())
        FlangeCleat4NodeSet = FlangeCleat4.transnodeset(FlangeCleatPart.nodeset())

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
        #file2.write("*Spring, elset=YSpringForRods\n")
        #file2.write("2, 2\n")
        #file2.write("1e+06\n")
        #file2.write("*Spring, elset=ZSpringForRods\n")
        #file2.write("3, 3\n")
        #file2.write("1e+06\n")
        file2.write("*Spring, NonLinear, elset=YSpringForRods\n")
        file2.write("2, 2\n")
        file2.write("-0.001, -10\n")
        file2.write("0, 0\n")
        file2.write("1e+06, 1\n")
        file2.write("*Spring, NonLinear, elset=ZSpringForRods\n")
        file2.write("3, 3\n")
        file2.write("-0.001, -10\n")
        file2.write("0, 0\n")
        file2.write("1e+06, 1\n")

        # ========================= Processing Steel Rods ===========================================
        file2.write("** ================================ SteelRod 1 ==============================\n")
        for i, obji in enumerate(ConcreteCoreNodeSet):
            for j, objj in enumerate(SteelRod1NodeSet):
                if 12.4 < ((obji[1] - objj[1])**2 + (obji[2] - objj[2])**2 + (obji[3] - objj[3])**2)**0.5 < 12.6:
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpringForRods\n")
                    if objj[2] <= obji[2]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod1.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod1.name, objj[0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpringForRods\n")
                    if objj[3] <= obji[3]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod1.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod1.name, objj[0]))

        file2.write("** ================================ SteelRod 2 ==============================\n")
        for i, obji in enumerate(ConcreteCoreNodeSet):
            for j, objj in enumerate(SteelRod2NodeSet):
                if 12.4 < ((obji[1] - objj[1])**2 + (obji[2] - objj[2])**2 + (obji[3] - objj[3])**2)**0.5 < 12.6:
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpringForRods\n")
                    if objj[2] <= obji[2]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod2.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod2.name, objj[0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpringForRods\n")
                    if objj[3] <= obji[3]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod2.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod2.name, objj[0]))

        file2.write("** ================================ SteelRod 3 ==============================\n")
        for i, obji in enumerate(ConcreteCoreNodeSet):
            for j, objj in enumerate(SteelRod3NodeSet):
                if 12.4 < ((obji[1] - objj[1])**2 + (obji[2] - objj[2])**2 + (obji[3] - objj[3])**2)**0.5 < 12.6:
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpringForRods\n")
                    if objj[2] <= obji[2]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod3.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod3.name, objj[0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpringForRods\n")
                    if objj[3] <= obji[3]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod3.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod3.name, objj[0]))

        file2.write("** ================================ SteelRod 4 ==============================\n")
        for i, obji in enumerate(ConcreteCoreNodeSet):
            for j, objj in enumerate(SteelRod4NodeSet):
                if 12.4 < ((obji[1] - objj[1])**2 + (obji[2] - objj[2])**2 + (obji[3] - objj[3])**2)**0.5 < 12.6:
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=YSpringForRods\n")
                    if objj[2] <= obji[2]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod4.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod4.name, objj[0]))
                    PairCounter += 1
                    file2.write("*Element, type=Spring2, elset=ZSpringForRods\n")
                    if objj[3] <= obji[3]:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, SteelRod4.name, objj[0], ConcreteCore.name, obji[0]))
                    else:
                        file2.write("%d, %s.%d, %s.%d\n" % (PairCounter, ConcreteCore.name, obji[0], SteelRod4.name, objj[0]))

        # ====================================== Fin Plates ==========================================
        def BoundFunction(x):
            BoundX = -410.1 <= x[1] <= -409.9
            BoundY = 1214.9 <= x[2] <= 1475.1
            BoundZ = 92.9 <= x[3] <= 93.1 or 102.9 <= x[3] <= 103.1
            condition1 = BoundX and BoundY and BoundZ

            if condition1:
                return True
            else:
                return False


        FWFP1C = InterNodes(FinPlate1.name, FinPlate1NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFP1C.pairnum

        def BoundFunction(x):
            BoundX = 29.9 <= x[1] <= 30.1
            BoundY = 1214.9 <= x[2] <= 1475.1
            BoundZ = 92.9 <= x[3] <= 93.1 or 102.9 <= x[3] <= 103.1
            condition1 = BoundX and BoundY and BoundZ

            if condition1:
                return True
            else:
                return False


        FWFP2C = InterNodes(FinPlate2.name, FinPlate2NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFP2C.pairnum

        # ========================================= Flange Cleats =========================================
        def BoundFunction(x):
            BoundX = -410.1 <= x[1] <= -409.9
            BoundY = 1529.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 5.1 or 174.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -410.1 <= x[1] <= -409.9
            BoundY = 1629.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWFC1C = InterNodes(FlangeCleat1.name, FlangeCleat1NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFC1C.pairnum

        def BoundFunction(x):
            BoundX = 29.9 <= x[1] <= 30.1
            BoundY = 1529.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 5.1 or 174.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = 29.9 <= x[1] <= 30.1
            BoundY = 1629.9 <= x[2] <= 1630.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWFC2C = InterNodes(FlangeCleat2.name, FlangeCleat2NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFC2C.pairnum

        def BoundFunction(x):
            BoundX = -410.1 <= x[1] <= -409.9
            BoundY = 1059.9 <= x[2] <= 1160.1
            BoundZ = 4.9 <= x[3] <= 5.1 or 174.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -410.1 <= x[1] <= -409.9
            BoundY = 1059.9 <= x[2] <= 1060.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWFC3C = InterNodes(FlangeCleat3.name, FlangeCleat3NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFC3C.pairnum

        def BoundFunction(x):
            BoundX = 29.9 <= x[1] <= 30.1
            BoundY = 1059.9 <= x[2] <= 1160.1
            BoundZ = 4.9 <= x[3] <= 5.1 or 174.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = 29.9 <= x[1] <= 30.1
            BoundY = 1059.9 <= x[2] <= 1060.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWFC4C = InterNodes(FlangeCleat4.name, FlangeCleat4NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFC4C.pairnum

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
