import numpy as np
import matplotlib.pyplot as plt

# ================================== Input File ===========================================
InpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SY2To.inp"
NewInpFile = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/Specimen-SY2T.inp"

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

    if flagPosition >= 3:
        flagPosition = 0

    if flagPosition >= 1 and flagPosition < 3:
        flagPosition = flagPosition + 1

    # ====== Find Node Pairs ====================================================================
    if line.startswith("*End Assembly"):
        PairCounter = 0

        # Find Part and Instances
        InternalStiffenerPart = filter(lambda x: x.name.startswith("InternalStiffener"), Part.instances)[0]
        BeamSolidPart = filter(lambda x: x.name.startswith("BeamSolid"), Part.instances)[0]
        BeamFarPart = filter(lambda x: x.name.startswith("BeamFar"), Part.instances)[0]
        InternalStiffenerPart = filter(lambda x: x.name.startswith("InternalStiffener"), Part.instances)[0]
        SidePlatePart = filter(lambda x: x.name.startswith("SidePlate"), Part.instances)[0]
        FinPlatePart = filter(lambda x: x.name.startswith("FinPlate"), Part.instances)[0]
        SteelTubePart = filter(lambda x: x.name.startswith("SteelTubeV6"), Part.instances)[0]

        InternalStiffener1 = filter(lambda x: x.name.startswith("InternalStiffener-1"), Instance.instances)[0]
        InternalStiffener2 = filter(lambda x: x.name.startswith("InternalStiffener-2"), Instance.instances)[0]
        SidePlate1 = filter(lambda x: x.name.startswith("SidePlate-1"), Instance.instances)[0]
        SidePlate2 = filter(lambda x: x.name.startswith("SidePlate-2"), Instance.instances)[0]
        FinPlate2 = filter(lambda x: x.name.startswith("FinPlate-2"), Instance.instances)[0]
        SteelTube = filter(lambda x: x.name.startswith("SteelTubeV6-1"), Instance.instances)[0]
        BeamSolid = filter(lambda x: x.name.startswith("BeamSolid"), Instance.instances)[0]
        BeamFar = filter(lambda x: x.name.startswith("BeamFar"), Instance.instances)[0]

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

        # ======================================== Side Plate and Internal Stiffener ==================================

        nodenum = len(SidePlatePart.nodeset())
        SidePlate1NodeSet = SidePlate1.transnodeset(SidePlatePart.nodeset())
        SidePlate2NodeSet = SidePlate2.transnodeset(SidePlatePart.nodeset())
        InternalStiffener1NodeSet = InternalStiffener1.transnodeset(InternalStiffenerPart.nodeset())
        InternalStiffener2NodeSet = InternalStiffener2.transnodeset(InternalStiffenerPart.nodeset())
        SteelTubeNodeSet = SteelTube.transnodeset(SteelTubePart.nodeset())
        FinPlate2NodeSet = FinPlate2.transnodeset(FinPlatePart.nodeset())
        BeamSolidNodeSet = BeamSolid.transnodeset(BeamSolidPart.nodeset())
        BeamFarNodeSet = BeamFar.transnodeset(BeamFarPart.nodeset())

        # ============ Side Plate and Internal Stiffener ====================
        def BoundFunction(x):
            BoundX = -455.1 <= x[1] <= -299.9
            BoundY = 1529.9 <= x[2] <= 1530.1
            BoundZ = 104.9 <= x[3] <= 105.1 or 74.9 <= x[3] <= 75.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -455.1 <= x[1] <= -454.9
            BoundY = 1529.9 <= x[2] <= 1530.1
            BoundZ = 74.9 <= x[3] <= 105.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False

        FWSP1IS1 = InterNodes(SidePlate1.name, SidePlate1NodeSet, InternalStiffener1.name, InternalStiffener1NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWSP1IS1.pairnum

        def BoundFunction(x):
            BoundX = -455.1 <= x[1] <= -299.9
            BoundY = 1159.9 <= x[2] <= 1160.1
            BoundZ = 104.9 <= x[3] <= 105.1 or 74.9 <= x[3] <= 75.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -455.1 <= x[1] <= -454.9
            BoundY = 1159.9 <= x[2] <= 1160.1
            BoundZ = 74.9 <= x[3] <= 105.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False

        FWSP2IS2 = InterNodes(SidePlate2.name, SidePlate2NodeSet, InternalStiffener2.name, InternalStiffener2NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWSP2IS2.pairnum

        # =========================== Internal Stiffener and Steel Tube =============================
        def BoundFunction(x):
            BoundX = -300.1 <= x[1] <= -299.9 or -80.1 <= x[1] <= -79.9
            BoundY = 1529.9 <= x[2] <= 1630.1
            BoundZ = 104.9 <= x[3] <= 105.1 or 74.9 <= x[3] <= 75.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -300.1 <= x[1] <= -299.9 or -80.1 <= x[1] <= -79.9
            BoundY = 1629.9 <= x[2] <= 1630.1
            BoundZ = 74.9 <= x[3] <= 105.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWIS1C = InterNodes(SteelTube.name, SteelTubeNodeSet, InternalStiffener1.name, InternalStiffener1NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter, tol=0.5)
        PairCounter = FWIS1C.pairnum

        def BoundFunction(x):
            BoundX = -300.1 <= x[1] <= -299.9 or -80.1 <= x[1] <= -79.9
            BoundY = 1059.9 <= x[2] <= 1160.1
            BoundZ = 104.9 <= x[3] <= 105.1 or 74.9 <= x[3] <= 75.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -300.1 <= x[1] <= -299.9 or -80.1 <= x[1] <= -79.9
            BoundY = 1059.9 <= x[2] <= 1060.1
            BoundZ = 74.9 <= x[3] <= 105.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False

        FWIS2C = InterNodes(SteelTube.name, SteelTubeNodeSet, InternalStiffener2.name, InternalStiffener2NodeSet, BoundFunction, file2, [1, 2, 3], PairCounter, tol=0.5)
        PairCounter = FWIS2C.pairnum

        #=============================== Side Plate and Steel Tube =========================
        def BoundFunction(x):
            BoundX = -300.1 <= x[1] <= -299.9
            BoundY = 1529.9 <= x[2] <= 1530.1
            BoundZ = 4.9 <= x[3] <= 65.1 or 114.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -300.1 <= x[1] <= -299.9
            BoundY = 1519.9 <= x[2] <= 1520.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False

        FWSP1C = InterNodes(SidePlate1.name, SidePlate1NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWSP1C.pairnum


        def BoundFunction(x):
            BoundX = -300.1 <= x[1] <= -299.9
            BoundY = 1159.9 <= x[2] <= 1160.1
            BoundZ = 4.9 <= x[3] <= 65.1 or 114.9 <= x[3] <= 175.1
            condition1 = BoundX and BoundY and BoundZ

            BoundX = -300.1 <= x[1] <= -299.9
            BoundY = 1169.9 <= x[2] <= 1170.1
            BoundZ = 4.9 <= x[3] <= 175.1
            condition2 = BoundX and BoundY and BoundZ

            if condition1 or condition2:
                return True
            else:
                return False


        FWSP2C = InterNodes(SidePlate2.name, SidePlate2NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWSP2C.pairnum


        # ======================== Fin Plate and Steel Tube =================================

        def BoundFunction(x):
            BoundX = -300.1 <= x[1] <= -299.9
            BoundY = 1214.9 <= x[2] <= 1475.1
            BoundZ = 102.9 <= x[3] <= 103.1 or 92.9 <= x[3] <= 93.1
            condition1 = BoundX and BoundY and BoundZ
            if condition1:
                return True
            else:
                return False

        FWFP2C = InterNodes(FinPlate2.name, FinPlate2NodeSet, SteelTube.name, SteelTubeNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = FWFP2C.pairnum


        # ======================== BeamSolid and BeamFar =================================

        def BoundFunction(x):
            BoundX = -810.1 <= x[1] <= -809.9
            condition1 = BoundX
            if condition1:
                return True
            else:
                return False


        BSBF = InterNodes(BeamSolid.name, BeamSolidNodeSet, BeamFar.name, BeamFarNodeSet, BoundFunction, file2, [1, 2, 3], PairCounter)
        PairCounter = BSBF.pairnum

    file2.write(line)


file.close()
file2.close()
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


newnode = NodeTranslation([7.34731579, 53, -10.1127129], [-345, 1110.0, 47], 2*np.pi/3, [-345, 1110.0, 47, -344.42265, 1109.42265, 47.57735])
print(newnode)