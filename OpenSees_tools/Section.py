class Fiber:
    Counter = 0
    instances = []
    nlist = []

    def __init__(self, n, PatchList):
        Fiber.Counter += 1
        self.PatchList = PatchList
        self.n = n
        if self.n in Fiber.nlist:
            Error("There's already an Fiber Section No.%d" % self.n)
        else:
            Fiber.nlist.append(n)
        self.name = 'fibers%d' % Fiber.Counter
        Fiber.instances.append(self)

        if Fiber.Counter == 1:
            commandp = "double locy;\ndouble locz;\ndouble AFiber;\nint tempno;\n"
        else:
            commandp = ''

        TotalFibers = 0
        for obj in PatchList:
            if obj.__class__.__name__ == "RectPatch":
                TotalFibers += obj.nh * obj.nv
            if obj.__class__.__name__ == "CircularPatch":
                TotalFibers += obj.ns * obj.nr
        Command1Line1 = "Fiber *%s[%d];\n" % (self.name, TotalFibers)
        self.TotalFibers = TotalFibers

        self.command = commandp + Command1Line1 + 'tempno = 0;\n'
        for obj in PatchList:
            self.command += obj.command1()
        self.command = self.command.replace('__FiberName__', self.name)

    def include(self):
        return ['Fiber.h', 'UniaxialFiber3d.h']
    def n(self):
        return self.n
    def PatchList(self):
        return self.PatchList
    def TotalFibers(self):
        return self.TotalFibers


class RectPatch:
    Counter = 0
    instances = []

    def __init__(self, mattag, nh, nv, yI, zI, yJ, zJ):
        self.mattag = mattag
        self.nv = nv
        self.nh = nh
        self.yI = yI
        self.zI = zI
        self.yJ = yJ
        self.zJ = zJ
        self.matcomp = filter(lambda x: x.n == self.mattag, uniaxialMaterial.instances)
        if len(self.matcomp) == 0:
            Error("In Fiber Section Patch, No Material Tagged %d" % self.mattag)
        else:
            self.matcomp = self.matcomp[0]

        self.SectionYLength = yJ - yI
        self.SectionZLength = zJ - zI
        if self.SectionYLength <= 0 or self.SectionZLength <= 0:
            Error("The 2 nodes of the rectangular patch in the fiber section are not correct")
        Command1Line1 = "for (i = 1; i <= %d; i++) {\n" % nh
        Command1Line2 = "   for (j = 1; j <= %d; j++) {\n" % nv
        Command1Line3 = "      locy = %f + %f / %d * 0.5 + (i - 1) * %f / %d;\n" % (yI, self.SectionYLength, nh, self.SectionYLength, nh)
        Command1Line4 = "      locz = %f + %f / %d * 0.5 + (j - 1) * %f / %d;\n" % (zI, self.SectionZLength, nv, self.SectionZLength, nv)
        Command1Line5 = "      AFiber = %f * %f / (%d * %d);\n" % (self.SectionYLength, self.SectionZLength, nh, nv)
        Command1Line6 = "      __FiberName__[tempno] = new UniaxialFiber3d(tempno + 1, *%s, AFiber, locy, locz);\n" % (self.matcomp.name)
        Command1Line7 = "      tempno = tempno + 1;\n"
        Command1Line8 = "   }\n"
        Command1Line9 = "}\n"
        self.Command1 = Command1Line1 + Command1Line2 + Command1Line3 + Command1Line4 + Command1Line5 + Command1Line6 + Command1Line7 + Command1Line8 + Command1Line9

    def matcomp(self):
        return self.matcomp

    def mattag(self):
        return self.mattag

    def yI(self):
        return self.yI

    def zI(self):
        return self.zI

    def yJ(self):
        return self.yJ

    def zJ(self):
        return self.zJ

    def SectionYLength(self):
        return self.SectionYLength

    def SectionZLength(self):
        return self.SectionZLength

    def command1(self):
        return self.Command1

class CircularPatch:
    Counter = 0
    instances = []

    def __init__(self, mattag, nr, ns, yI, zI, r):
        self.mattag = mattag
        self.nr = nr
        self.ns = ns
        self.yI = yI
        self.zI = zI
        self.r = r
        self.matcomp = filter(lambda x: x.n == self.mattag, uniaxialMaterial.instances)
        if len(self.matcomp) == 0:
            Error("In Fiber Section Patch, No Material Tagged %d" % self.mattag)
        else:
            self.matcomp = self.matcomp[0]

        Command1Line1 = "for (i = 1; i <= %d; i++) {\n" % self.ns
        Command1Line2 = "   for (j = 1; j <= %d; j++) {\n" % self.nr
        Command1Line3 = "      locy = %f + (%f/%f * (j - 0.5))*cos(2*3.1415926/%f*i);\n" % (self.yI, self.r, self.nr, self.ns)
        Command1Line4 = "      locz = %f + (%f/%f * (j - 0.5))*sin(2*3.1415926/%f*i);\n" % (self.zI, self.r, self.nr, self.ns)
        Command1Line5 = "      AFiber = 3.1415926*((j*%f/%d)*(j*%f/%d)-((j-1)*%f/%d)*((j-1)*%f/%d))/%d;\n" % (self.r, self.nr, self.r, self.nr, self.r, self.nr, self.r, self.nr, self.ns)
        Command1Line6 = "      __FiberName__[tempno] = new UniaxialFiber3d(tempno + 1, *%s, AFiber, locy, locz);\n" % (self.matcomp.name)
        Command1Line7 = "      tempno = tempno + 1;\n"
        Command1Line8 = "   }\n"
        Command1Line9 = "}\n"
        self.Command1 = Command1Line1 + Command1Line2 + Command1Line3 + Command1Line4 + Command1Line5 + Command1Line6 + Command1Line7 + Command1Line8 + Command1Line9

    def matcomp(self):
        return self.matcomp

    def mattag(self):
        return self.mattag

    def yI(self):
        return self.yI

    def zI(self):
        return self.zI

    def r(self):
        return self.r

    def command1(self):
        return self.Command1

class BeamIntegration:
    Counter = 0
    instances = []
    def __init__(self):
        BeamIntegration.Counter += 1

    class Lobatto:
        Counter = 0
        def __init__(self):
            BeamIntegration.Lobatto.Counter += 1
            self.name = "LobattoIntegration%d" % BeamIntegration.Lobatto.Counter
            self.command = "BeamIntegration *%s = new LobattoBeamIntegration();\n" % self.name
            BeamIntegration.instances.append(self)

        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["LobattoBeamIntegration.h"]

    class Legendre:
        Counter = 0
        def __init__(self):
            BeamIntegration.Legendre.Counter += 1
            self.name = "LegendreIntegration%d" % BeamIntegration.Legendre.Counter
            self.command = "BeamIntegration *%s = new LegendreBeamIntegration();\n" % self.name
            BeamIntegration.instances.append(self)

        def name(self):
            return self.name

        def command(self):
            return self.command

        def include(self):
            return ["LegendreBeamIntegration.h"]

    class FixedLocation:
        Counter = 0
        def __init__(self, number, LocationList='Even'):
            self.number = number
            BeamIntegration.FixedLocation.Counter += 1
            self.name = "FixedLocationIntegration%d" % BeamIntegration.FixedLocation.Counter
            self.command = "Vector VecLoc%d(%d);\n" % (BeamIntegration.FixedLocation.Counter, self.number)

            if LocationList == 'Even':
                self.command += "for (i = 0; i < %d; i++)\n" % self.number
                self.command += "VecLoc%d(i) = 1.0/%d*(double)i;\n" % (BeamIntegration.FixedLocation.Counter, self.number - 1)
            elif type(LocationList) == list:
                for i in range(0, self.number):
                    if LocationList[i] > 1:
                        Error("In FixedLocationIntegration, LocationList expected a number no greater than 1, but received %f" % LocationList[i])
                    else:
                        self.command += "VecLoc%d(%d) = %f;\n" % (BeamIntegration.FixedLocation.Counter, i, LocationList[i])
            else:
                Error('In Fixed Location Integration, LocationList expected a list of numbers')
            self.command += 'BeamIntegration *%s = new FixedLocationBeamIntegration(%d, VecLoc%d);\n' % (self.name, self.number, BeamIntegration.FixedLocation.Counter)
            BeamIntegration.instances.append(self)

        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ['FixedLocationBeamIntegration.h']

    class HingeRadau:
        Counter = 0
        def __init__(self, lpi, lpj):
            # lpi: plastic hinge length at end I, lpj: plastic hinge length at end J
            self.lpi = lpi
            self.lpj = lpj
            BeamIntegration.HingeRadau.Counter += 1
            self.name = "HingeRadauIntegration%d" % BeamIntegration.HingeRadau.Counter
            self.command = 'BeamIntegration *%s = new HingeRadauBeamIntegration(%f, %f);\n' % (self.name, self.lpi, self.lpj)
            BeamIntegration.instances.append(self)

        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["HingeRadauBeamIntegration.h"]
        def lpi(self):
            return self.lpi
        def lpj(self):
            return self.lpj



class Section:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        Section.Counter += 1

    class Elastic:
        # section Elastic $secTag $E $A $Iz $Iy $G $J
        Counter = 0
        def __init__(self, n, E, A, Iz, Iy, G, J, numSec):
            Section.Elastic.Counter += 1
            self.n = n
            self.E = E
            self.A = A
            self.Iz = Iz
            self.Iy = Iy
            self.G = G
            self.J = J
            self.numSec = numSec
            self.name = 'ElasticSection%d' % Section.Elastic.Counter
            if self.n in Section.nlist:
                Error("There's already an Section No.%d" % self.n)
            else:
                Section.nlist.append(n)
            self.command = "SectionForceDeformation *%s[%d];\n" % (self.name, self.numSec)
            self.command += "for (i = 0; i < %d; i++)\n" % self.numSec
            self.command += "%s[i] = new ElasticSection3d(%d, %f, %f, %f, %f, %f, %f);\n" % (self.name, self.n, self.E, self.A, self.Iz, self.Iy, self.G, self.J)
            Section.instances.append(self)

        def n(self):
            return self.n
        def E(self):
            return self.E
        def A(self):
            return self.A
        def Iz(self):
            return self.Iz
        def Iy(self):
            return self.Iy
        def G(self):
            return self.G
        def J(self):
            return self.J
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ['ElasticSection3d.h']

    class Fiber:
        Counter = 0
        def __init__(self, n, fiberslist, nips=10):
            Section.Fiber.Counter += 1
            self.n = n
            self.nips = nips

            if type(fiberslist) == list:
                self.fiberslist = fiberslist
            else:
                self.fiberslist = []
                for i in range(1, nips+1):
                    self.fiberslist.append(fiberslist)

            self.name = 'FiberSection%d' % Section.Fiber.Counter

            if self.n in Section.nlist:
                Error("There's already an Section No.%d" % self.n)
            else:
                Section.nlist.append(n)

            Fibernumbers = []
            Fibernames = []
            self.command = "SectionForceDeformation *%s[%d];\n" % (self.name, self.nips)
            Section.instances.append(self)
            for i in range(0, nips):
                Fibernumbers.append(self.fiberslist[i].TotalFibers)
                Fibernames.append(self.fiberslist[i].name)
                self.command += "%s[%d] = new FiberSection3d(%d, %d, %s);\n" % (self.name, i, i + 1, Fibernumbers[i], Fibernames[i])

        def n(self):
            return self.n

        def nips(self):
            return self.nips

        def name(self):
            return self.name

        def command(self):
            return self.command

        def include(self):
            return ['FiberSection3d.h']

    class SectionAggregator:
        Counter = 0
        def __init__(self, n, MatTagList, DofList, PSectionTag=0, numSec = 10, ReinforcedSecNumList = 'All'):
            self.n = n
            Section.SectionAggregator.Counter += 1
            self.PSectionTag = PSectionTag
            self.MatTagList = MatTagList
            self.DofList = DofList
            self.numSec = numSec

            if self.n in Section.nlist:
                Error("There's already an Section No.%d" % self.n)
            else:
                Section.nlist.append(n)

            if ReinforcedSecNumList == 'All':
                self.ReinforcedSecNumList = []
                for i in range(0, self.numSec):
                    self.ReinforcedSecNumList.append(i)
            else:
                self.ReinforcedSecNumList = ReinforcedSecNumList

            if PSectionTag == 0:
                self.PSection = 0
            else:
                PSection = filter(lambda x: x.n == self.PSectionTag, Section.instances)

                if len(PSection) == 0:
                    Error("In Section Aggregator, no section specified")
                else:
                    self.PSection = PSection[0]

            if len(MatTagList) != len(DofList):
                Error("In Section Aggregator, the length of MatTagList is not equal to the length of DofList")
            else:
                self.numMat = len(MatTagList)

            MatList = []
            for i in range(0, self.numMat):
                Mat1 = filter(lambda x: x.n == self.MatTagList[i], uniaxialMaterial.instances)
                if len(Mat1) == 0:
                    Error("In Section Aggregator, No Material tagged %d" % self.MatTagList[i])
                else:
                    MatList.append(Mat1[0])

            self.MatList = MatList
            self.DofList = DofList
            self.name = 'AggregatedSections%d' % Section.SectionAggregator.Counter
            self.command = 'UniaxialMaterial *MatCombinedForSA%d[%d];\n' % (Section.SectionAggregator.Counter, self.numMat)

            for i in range(0, self.numMat):
                self.command += "MatCombinedForSA%d[%d] = %s;\n" % (Section.SectionAggregator.Counter, i, self.MatList[i].name)

            self.command += "ID DofsForSA%d(%d);\n" % (Section.SectionAggregator.Counter, self.numMat)

            for i in range(0, self.numMat):
                if self.DofList[i] == 'P':
                    rank = 2
                elif self.DofList[i] == 'Mz':
                    rank = 1
                elif self.DofList[i] == 'Vy':
                    rank = 3
                elif self.DofList[i] == 'My':
                    rank = 4
                elif self.DofList[i] == 'Vz':
                    rank = 5
                elif self.DofList[i] == 'T':
                    rank = 6

                self.command += "DofsForSA%d(%d) = %d;\n" % (Section.SectionAggregator.Counter, i, rank)

            if self.PSection == 0:
                self.command += "SectionForceDeformation *AggregatedSection%d = new SectionAggregator(%d, %d, &MatCombinedForSA%d[0], DofsForSA%d);\n" % (Section.SectionAggregator.Counter, self.n, self.numMat, Section.SectionAggregator.Counter, Section.SectionAggregator.Counter)
                self.command += "SectionForceDeformation *AggregatedSections%d[%d];\n" % (Section.SectionAggregator.Counter, self.numSec)
                for obj in self.ReinforcedSecNumList:
                    self.command += "AggregatedSections%d[%d] = AggregatedSection%d;\n" % (Section.SectionAggregator.Counter, obj, Section.SectionAggregator.Counter)
            else:
                self.command += "SectionForceDeformation *AggregatedSection%d = new SectionAggregator(%d, *%s[0], %d, &MatCombinedForSA%d[0], DofsForSA%d);\n" % (Section.SectionAggregator.Counter, self.n, self.PSection.name, self.numMat, Section.SectionAggregator.Counter, Section.SectionAggregator.Counter)
                self.command += "SectionForceDeformation *AggregatedSections%d[%d];\n" % (Section.SectionAggregator.Counter, self.numSec)
                for i in range(0, self.numSec):
                    if i in self.ReinforcedSecNumList:
                        self.command += "AggregatedSections%d[%d] = AggregatedSection%d;\n" % (Section.SectionAggregator.Counter, i, Section.SectionAggregator.Counter)
                    else:
                        self.command += "AggregatedSections%d[%d] = %s[0];\n" % (Section.SectionAggregator.Counter, i, self.PSection.name)

            Section.instances.append(self)

        def n(self):
            return self.n
        def PSectionTag(self):
            return self.PSectionTag
        def PSection(self):
            return self.PSection
        def MatTagList(self):
            return self.MatTagList
        def MatList(self):
            return self.MatList
        def numMat(self):
            return self.numMat
        def DofList(self):
            return self.DofList
        def numSec(self):
            return self.numSec
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["SectionAggregator.h"]

    class PlateFiber:
        #section PlateFiber $secTag $matTag $h
        Counter = 0
        def __init__(self, n, MatTag, h):
            self.n = n
            self.MatTag = MatTag
            self.h = h

            if self.n in Section.nlist:
                Error("There's already an Section No.%d" % self.n)
            else:
                Section.nlist.append(n)

            Section.PlateFiber.Counter += 1
            self.name = "PlateFiberSection%d" % Section.PlateFiber.Counter

            Mat1 = filter(lambda x: x.n == self.MatTag, NDMaterial.instances)
            if len(Mat1) == 0:
                Error("No NDMaterial Tagged %d" % self.MatTag)
            else:
                self.Mat = Mat1[0]

            self.command = 'SectionForceDeformation *%s = new MembranePlateFiberSection(%d, %f, *%s);\n' % (self.name, self.n, self.h, self.Mat.name)

            Section.instances.append(self)

        def n(self):
            return self.n
        def MatTag(self):
            return self.MatTag
        def Mat(self):
            return self.Mat
        def h(self):
            return self.h
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["MembranePlateFiberSection.h"]



