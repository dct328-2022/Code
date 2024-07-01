class LineElement:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        LineElement.Counter += 1


    class Truss:
        Counter = 0
        def __init__(self, n, iNode, jNode, A, mat, rho=0, cMass=0, doRayleigh=0):
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.A = A
            self.mat = mat
            self.rho = rho
            self.cMass = cMass
            self.doRayleigh = doRayleigh
            LineElement.Truss.Counter += 1
            self.name = 'Truss%d' % LineElement.Truss.Counter
            self.command = 'Truss *%s = new Truss(%d, 3, %d, %d, *%s, %f, %f, %d, %d);\n' % (self.name, self.n, self.iNode, self.jNode, self.mat.name, self.A, self.rho, self.doRayleigh, self.cMass)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)
            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def n(self):
            return self.n
        def iNode(self):
            return self.iNode
        def jNode(self):
            return self.jNode
        def A(self):
            return self.A
        def mat(self):
            return self.mat
        def rho(self):
            return self.rho
        def cMass(self):
            return self.cMass
        def doRayleigh(self):
            return self.doRayleigh
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ['Truss.h']

    class MaterialList:
        Counter = 0
        def __init__(self, MatList):
            LineElement.MaterialList.Counter += 1
            self.n = LineElement.MaterialList.Counter
            self.dim = len(MatList)
            self.MatList = MatList
            self.name = "theMats%d" % self.n
            LineElement.instances.append(self)
            self.command = 'UniaxialMaterial *theMats%d[%d];\n' % (self.n, self.dim)
            for i in range(0, self.dim):
                self.command += 'theMats%d[%d] = %s;\n' % (self.n, i, self.MatList[i].name)

        def n(self):
            return self.n
        def dim(self):
            return self.dim
        def MatList(self):
            return self.MatList
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return []

    class DirectionList:
        Counter = 0
        def __init__(self, DirList):
            LineElement.DirectionList.Counter += 1
            self.n = LineElement.DirectionList.Counter
            self.dim = len(DirList)
            self.DirList = DirList
            self.name = "theDirs%d" % self.n
            LineElement.instances.append(self)
            self.command = "ID theDirs%d(%d);\n" % (self.n, self.dim)
            for i in range(0, self.dim):
                self.command += 'theDirs%d(%d) = %d;\n' % (self.n, i, self.DirList[i])

        def n(self):
            return self.n
        def dim(self):
            return self.dim
        def MatList(self):
            return self.MatList
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return []

    class ZeroLength:
        Counter = 0
        def __init__(self, n, iNode, jNode, MatList, DirList, XVec=0, YpVec=0, doRayleigh=0):
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.MatList = MatList
            self.DirList = DirList
            self.XVec = XVec
            self.YpVec = YpVec
            self.n1dMat = self.MatList.dim
            self.doRayleigh = doRayleigh
            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)
            LineElement.ZeroLength.Counter += 1
            LineElement.instances.append(self)
            self.name = 'ZeroLength%d' % LineElement.ZeroLength.Counter
            self.command = "ZeroLength *%s = new ZeroLength(%d, 3, %d, %d, %s, %s, %d, %s, %s, %d);\n" % (self.name, self.n, self.iNode, self.jNode, self.XVec.name, self.YpVec.name, self.n1dMat, self.MatList.name, self.DirList.name, self.doRayleigh)
            self.command += "theDomain->addElement(%s);\n" % self.name
        def n(self):
            return self.n
        def iNode(self):
            return self.iNode
        def jNode(self):
            return self.jNode
        def MatList(self):
            return self.MatList
        def DirList(self):
            return self.DirList
        def XVec(self):
            return self.XVec
        def YpVec(self):
            return self.YpVec
        def n1dMat(self):
            return self.n1dMat
        def doRayleigh(self):
            return self.doRayleigh
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ['ZeroLength.h']



    class ElasticBeamColumn:
        # element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag <-mass $massDens> <-cMass>
        Counter = 0
        def __init__(self, n, iNode, jNode, A, E, G, J, Iy, Iz, transfTag, massDens=0, cMass=False):
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.A = A
            self.E = E
            self.G = G
            self.J = J
            self.Iy = Iy
            self.Iz = Iz
            self.transfTag = transfTag
            self.massDens = massDens
            self.cMass = cMass
            LineElement.ElasticBeamColumn.Counter += 1
            self.name = 'ElasticBeamColumn%d' % LineElement.ElasticBeamColumn.Counter
            GTList = filter(lambda x: x.n == self.transfTag, GeometricTransformation.instances)
            if len(GTList) == 0:
                Error("No Geometric Transformation Tagged %d" % self.transfTag)
            else:
                self.GTName = GTList[0].name
            if self.massDens == 0 and self.cMass == False:
                self.command = 'ElasticBeam3d *%s = new ElasticBeam3d(%d, %f, %f, %f, %f, %f, %f, %d, %d, *%s);\n' % (self.name, self.n, self.A, self.E, self.G, self.J, self.Iy, self.Iz, self.iNode, self.jNode, self.GTName)
            else:
                self.command = 'ElasticBeam3d *%s = new ElasticBeam3d(%d, %f, %f, %f, %f, %f, %f, %d, %d, *%s, %f);\n' % (self.name, self.n, self.A, self.E, self.G, self.J, self.Iy, self.Iz, self.iNode, self.jNode,self.GTName, self.massDens)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)
            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def A(self):
            return self.A

        def G(self):
            return self.G

        def J(self):
            return self.J

        def Iy(self):
            return self.Iy

        def Iz(self):
            return self.Iz

        def iNode(self):
            return self.iNode

        def jNode(self):
            return self.jNode

        def transfTag(self):
            return self.transfTag

        def GTName(self):
            return self.GTName

        def massDens(self):
            return self.massDens

        def cMass(self):
            return self.cMass

        def include(self):
            return ["ElasticBeam3d.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class flatSliderBearing:
        # element elasticBeamColumn $eleTag $iNode $jNode $A $E $G $J $Iy $Iz $transfTag <-mass $massDens> <-cMass>
        Counter = 0
        def __init__(self, n, iNode, jNode, frnmdl, kInit, MaterialList, VecX, VecY, shearDist = 0, mass = 0, iter = 25, tol=1e-8):
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.frnmdl = frnmdl
            self.kInit = kInit
            self.MaterialList = MaterialList
            self.VecX = VecX
            self.VecY = VecY
            self.mass = mass
            self.shearDist = shearDist
            self.iter = iter
            self.tol = str(tol)
            LineElement.flatSliderBearing.Counter += 1
            self.name = 'flatSliderBearing%d' % LineElement.flatSliderBearing.Counter

            self.frnmdli = filter(lambda x: x.n == self.frnmdl, Friction.instances)[0]

            self.command = 'FlatSliderSimple3d *%s = new FlatSliderSimple3d(%d, %d, %d, *%s, %f, %s, %s, %s, %f, 0, %f, %d, %s);\n' % (self.name, self.n, self.iNode, self.jNode, self.frnmdli.name, self.kInit, self.MaterialList.name, self.VecY.name, self.VecX.name, self.shearDist, self.mass, self.iter, self.tol)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)
            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)

        def n(self):
            return self.n

        def iNode(self):
            return self.iNode

        def jNode(self):
            return self.jNode

        def mass(self):
            return self.mass

        def frnmdl(self):
            return self.frnmdl

        def kInit(self):
            return self.kInit

        def include(self):
            return ["FlatSliderSimple3d.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class ElasticTimoshenkoBeamColumn:
        # element ElasticTimoshenkoBeam $eleTag $iNode $jNode $E $G $A $Jx $Iy $Iz $Avy $Avz $transfTag <-mass $massDens> <-cMass>
        Counter = 0
        def __init__(self, n, iNode, jNode, E, G, A, J, Iy, Iz, Avy, Avz, transfTag, massDens=0, cMass=False):
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.A = A
            self.E = E
            self.G = G
            self.J = J
            self.Iy = Iy
            self.Iz = Iz
            self.Avy = Avy
            self.Avz = Avz
            self.transfTag = transfTag
            self.massDens = massDens
            self.cMass = cMass
            LineElement.ElasticTimoshenkoBeamColumn.Counter += 1
            self.name = 'ElasticTimoshenkoBeam%d' % LineElement.ElasticTimoshenkoBeamColumn.Counter
            GTList = filter(lambda x: x.n == self.transfTag, GeometricTransformation.instances)
            if len(GTList) == 0:
                Error("No Geometric Transformation Tagged %d" % self.transfTag)
            else:
                self.GTName = GTList[0].name
            if self.massDens == 0 and self.cMass == False:
                self.command = 'ElasticTimoshenkoBeam3d *%s = new ElasticTimoshenkoBeam3d(%d, %d, %d, %f, %f, %f, %f, %f, %f, %f, %f, *%s);\n' % (self.name, self.n, self.iNode, self.jNode, self.E, self.G, self.A, self.J, self.Iy, self.Iz, self.Avy, self.Avz, self.GTName)
            else:
                self.command = 'ElasticTimoshenkoBeam3d *%s = new ElasticTimoshenkoBeam3d(%d, %d, %d, %f, %f, %f, %f, %f, %f, %f, %f, *%s, %f);\n' % (self.name, self.n, self.iNode, self.jNode, self.E, self.G, self.A, self.J, self.Iy, self.Iz, self.Avy, self.Avz, self.GTName, self.massDens)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)
            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def A(self):
            return self.A

        def G(self):
            return self.G

        def J(self):
            return self.J

        def Iy(self):
            return self.Iy

        def Iz(self):
            return self.Iz

        def Avy(self):
            return self.Avy

        def Avz(self):
            return self.Avz

        def iNode(self):
            return self.iNode

        def jNode(self):
            return self.jNode

        def transfTag(self):
            return self.transfTag

        def GTName(self):
            return self.GTName

        def massDens(self):
            return self.massDens

        def cMass(self):
            return self.cMass

        def include(self):
            return ["ElasticTimoshenkoBeam3d.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class ForceBeamColumn:
        # element forceBeamColumn $eleTag $iNode $jNode $transfTag "IntegrationType arg1 arg2 ..." <-mass $massDens> <-iter $maxIters $tol>
        Counter = 0
        def __init__(self, n, iNode, jNode, transfTag, numipts, BeamIntegration, SectionCombined, massDens=0, maxIters=15, tol=1e-12):
            self.n = n
            LineElement.ForceBeamColumn.Counter += 1

            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)

            self.iNode = iNode
            self.jNode = jNode
            self.transfTag = transfTag
            self.numipts = numipts

            GTList = filter(lambda x: x.n == self.transfTag, GeometricTransformation.instances)
            if len(GTList) == 0:
                Error("No Geometric Transformation Tagged %d" % self.transfTag)
            else:
                self.GTName = GTList[0].name

            self.BeamIntegration = BeamIntegration
            self.SectionCombined = SectionCombined
            self.massDens = massDens
            self.maxIters = maxIters
            self.tol = str(tol)
            self.name = "ForceBeamColumn%d" % LineElement.ForceBeamColumn.Counter
            self.command = "ForceBeamColumn3d *%s = new ForceBeamColumn3d(%d, %d, %d, %d, %s, *%s, *%s, %f, %d, %s);\n" % (self.name, self.n, self.iNode, self.jNode, self.numipts, self.SectionCombined.name, self.BeamIntegration.name, self.GTName, self.massDens, self.maxIters, self.tol)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)

        def n(self):
            return self.n
        def iNode(self):
            return self.iNode
        def jNode(self):
            return self.jNode
        def transfTag(self):
            return self.transfTag
        def GTName(self):
            return self.GTName
        def numipts(self):
            return self.numipts
        def BeamIntegration(self):
            return self.BeamIntegration
        def SectionCombined(self):
            return self.SectionCombined
        def massDens(self):
            return self.massDens
        def maxIter(self):
            return self.maxIters
        def tol(self):
            return self.tol
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["ForceBeamColumn3d.h"]

    class DispBeamColumn:
        # element forceBeamColumn $eleTag $iNode $jNode $transfTag "IntegrationType arg1 arg2 ..." <-mass $massDens> <-iter $maxIters $tol>
        Counter = 0
        def __init__(self, n, iNode, jNode, transfTag, numipts, BeamIntegration, SectionCombined, massDens=0, cMass=0):
            self.n = n
            LineElement.DispBeamColumn.Counter += 1

            if self.n in LineElement.nlist:
                Error("There's already an Element No.%d" % self.n)
            else:
                LineElement.nlist.append(n)

            self.iNode = iNode
            self.jNode = jNode
            self.transfTag = transfTag
            self.numipts = numipts

            GTList = filter(lambda x: x.n == self.transfTag, GeometricTransformation.instances)
            if len(GTList) == 0:
                Error("No Geometric Transformation Tagged %d" % self.transfTag)
            else:
                self.GTName = GTList[0].name

            self.BeamIntegration = BeamIntegration
            self.SectionCombined = SectionCombined
            self.massDens = massDens
            self.cMass = cMass
            self.name = "DispBeamColumn%d" % LineElement.DispBeamColumn.Counter
            self.command = "DispBeamColumn3d *%s = new DispBeamColumn3d(%d, %d, %d, %d, %s, *%s, *%s, %f, %d);\n" % (self.name, self.n, self.iNode, self.jNode, self.numipts, self.SectionCombined.name, self.BeamIntegration.name, self.GTName, self.massDens, self.cMass)
            self.command += "theDomain->addElement(%s);\n" % self.name
            LineElement.instances.append(self)

        def n(self):
            return self.n
        def iNode(self):
            return self.iNode
        def jNode(self):
            return self.jNode
        def transfTag(self):
            return self.transfTag
        def GTName(self):
            return self.GTName
        def numipts(self):
            return self.numipts
        def BeamIntegration(self):
            return self.BeamIntegration
        def SectionCombined(self):
            return self.SectionCombined
        def massDens(self):
            return self.massDens
        def cMass(self):
            return self.cMass
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["DispBeamColumn3d.h"]

    class DispBeamColumnMeshed:
        Counter = 0
        def __init__(self, n, iNode, jNode, transfTag, numipts, BeamIntegration, SectionCombined, divn, IfCombineSameNode, NodeStart, massDens=0, cMass=0):
            tolerance = 1e-3
            self.n = n
            self.iNode = iNode
            self.jNode = jNode
            self.transfTag = transfTag
            self.numipts = numipts
            self.BeamIntegration = BeamIntegration
            self.SectionCombined = SectionCombined
            self.divn = divn
            self.IfCombineSameNode = IfCombineSameNode
            self.NodeSart = NodeStart
            self.massDen = massDens
            self.cMass = cMass

            node1 = filter(lambda x: x.n == iNode, Node.instances)[0]
            node2 = filter(lambda x: x.n == jNode, Node.instances)[0]

            self.NodeList = [node1]

            if not(self.IfCombineSameNode):
                for i in range(1, divn):
                    temp = Node(NodeStart, node1.x + (node2.x - node1.x)*i/divn, node1.y + (node2.y - node1.y)*i/divn, node1.z + (node2.z - node1.z)*i/divn)
                    self.NodeList.append(temp)
                    NodeStart += 1

            else:
                for i in range(1, divn):
                    tempx = node1.x + (node2.x - node1.x)*i/divn
                    tempy = node1.y + (node2.y - node1.y)*i/divn
                    tempz = node1.z + (node2.z - node1.z)*i/divn
                    checknodes = filter(lambda xx: abs(xx.x - tempx) < tolerance and abs(xx.y - tempy) < tolerance and abs(xx.z - tempz) < tolerance, Node.instances)
                    if len(checknodes) == 0:
                        temp = Node(NodeStart, tempx, tempy, tempz)
                        self.NodeList.append(temp)
                        NodeStart += 1
                    elif len(checknodes) == 1:
                        self.NodeList.append(checknodes[0])
                    else:
                        self.NodeList.append(checknodes[0])
                        _Warning("In DispBeamColumnMeshed, IfCombineSameNode is True, but there are more than one node at the same position")


            self.NodeList.append(node2)

            EleStart = n
            self.EleStart = n
            for i in range(0, divn):
                LineElement.DispBeamColumn(EleStart, self.NodeList[i].n, self.NodeList[i + 1].n, self.transfTag, self.numipts, self.BeamIntegration, self.SectionCombined)
                EleStart += 1

class ShellElement:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        ShellElement.Counter += 1

    class ShellMITC9:
        Counter = 0
        def __init__(self, n, node1, node2, node3, node4, node5, node6, node7, node8, node9, secTag):
            self.n = n
            self.node1 = node1
            self.node2 = node2
            self.node3 = node3
            self.node4 = node4
            self.node5 = node5
            self.node6 = node6
            self.node7 = node7
            self.node8 = node8
            self.node9 = node9
            self.secTag = secTag

            secIns = filter(lambda x: x.n == self.secTag, Section.instances)
            if len(secIns) == 0:
                Error("In ShellMITC9, no secion tagged %d" % secTag)
            else:
                self.secName = secIns[0].name

            ShellElement.ShellMITC9.Counter += 1
            ShellElement.instances.append(self)

            self.name = "ShellMITC9%d" % ShellElement.ShellMITC9.Counter

            self.command = "ShellMITC9 *ShellMITC9%d = new ShellMITC9(%d, %d, %d, %d, %d, %d, %d, %d, %d, %d, *%s);" % (ShellElement.ShellMITC9.Counter, self.n, self.node1, self.node2, self.node3, self.node4, self.node5, self.node6, self.node7, self.node8, self.node9, self.secName)
            self.command += "theDomain->addElement(%s);\n" % self.name

        def n(self):
            return self.n
        def node1(self):
            return self.node1
        def node2(self):
            return self.node2
        def node3(self):
            return self.node3
        def node4(self):
            return self.node4
        def node5(self):
            return self.node5
        def node6(self):
            return self.node6
        def node7(self):
            return self.node7
        def node8(self):
            return self.node8
        def node9(self):
            return self.node9
        def secTag(self):
            return self.secTag
        def name(self):
            return self.name
        def secName(self):
            return self.secName
        def include(self):
            return ['ShellMITC9.h']
        def command(self):
            return self.command

    class ShellNLDKGT:
        Counter = 0
        def __init__(self, n, node1, node2, node3, secTag):
            self.n = n
            self.node1 = node1
            self.node2 = node2
            self.node3 = node3
            self.secTag = secTag

            secIns = filter(lambda x: x.n == self.secTag, Section.instances)
            if len(secIns) == 0:
                Error("In ShellNLDKGT, no secion tagged %d" % secTag)
            else:
                self.secName = secIns[0].name

            ShellElement.ShellNLDKGT.Counter += 1
            ShellElement.instances.append(self)

            self.name = "ShellNLDKGT%d" % ShellElement.ShellNLDKGT.Counter

            self.command = "ShellNLDKGT *ShellNLDKGT%d = new ShellNLDKGT(%d, %d, %d, %d, *%s);\n" % (ShellElement.ShellNLDKGT.Counter, self.n, self.node1, self.node2, self.node3, self.secName)
            self.command += "theDomain->addElement(%s);\n" % self.name

        def n(self):
            return self.n
        def node1(self):
            return self.node1
        def node2(self):
            return self.node2
        def node3(self):
            return self.node3
        def secTag(self):
            return self.secTag
        def name(self):
            return self.name
        def secName(self):
            return self.secName
        def include(self):
            return ['ShellNLDKGT.h']
        def command(self):
            return self.command

    class ShellMITC9Meshed:
        def __init__(self, node1, node2, node3, node4, div1, div2, StartNode, StartEle, secTag, Specialab = [], Specialbc= [], Specialcd = [], Specialda = [], IfCombineSameNode = True):
            # 4 nodes should be in counter-clockwise order
            # The format for Specialbc: Specialab = ['y', -0.1, 0.1], Specialbc = ['z', 3.3065, 3.6935]

            tolerance = 1e-3

            self.node1 = node1
            self.node2 = node2
            self.node3 = node3
            self.node4 = node4
            self.div1 = div1
            self.div2 = div2
            self.StartNode = StartNode
            self.StartEle = StartEle
            self.secTag = secTag
            self.Specialab = Specialab
            self.Specialbc = Specialbc
            self.Specialcd = Specialcd
            self.Specialda = Specialda
            self.IfCombineSameNode = IfCombineSameNode


            node1i = filter(lambda x: x.n == self.node1, Node.instances)
            if len(node1i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node1)
            else:
                xa = node1i[0].x
                ya = node1i[0].y
                za = node1i[0].z

            node2i = filter(lambda x: x.n == self.node2, Node.instances)
            if len(node2i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node2)
            else:
                xb = node2i[0].x
                yb = node2i[0].y
                zb = node2i[0].z

            node3i = filter(lambda x: x.n == self.node3, Node.instances)
            if len(node3i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node3)
            else:
                xc = node3i[0].x
                yc = node3i[0].y
                zc = node3i[0].z

            node4i = filter(lambda x: x.n == self.node4, Node.instances)
            if len(node4i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node4)
            else:
                xd = node4i[0].x
                yd = node4i[0].y
                zd = node4i[0].z

            # ============== Put Special Insert Point into right order =============
            if len(Specialab) > 1:
                pand = eval('%sb > %sa' % (Specialab[0], Specialab[0]))
                if pand:
                    sortlist = Specialab[1:len(Specialab)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialab)):
                        Specialab[i] = sortlist[i - 1]
                else:
                    sortlist = Specialab[1:len(Specialab)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialab)):
                        Specialab[i] = sortlist[i - 1]
            else:
                Specialab = []

            if len(Specialbc) > 1:
                pand = eval('%sc > %sb' % (Specialbc[0], Specialbc[0]))
                if pand:
                    sortlist = Specialbc[1:len(Specialbc)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialbc)):
                        Specialbc[i] = sortlist[i - 1]
                else:
                    sortlist = Specialbc[1:len(Specialbc)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialbc)):
                        Specialbc[i] = sortlist[i - 1]
            else:
                Specialbc = []

            if len(Specialcd) > 1:
                pand = eval('%sd > %sc' % (Specialcd[0], Specialcd[0]))
                if pand:
                    sortlist = Specialcd[1:len(Specialcd)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialcd)):
                        Specialcd[i] = sortlist[i - 1]
                else:
                    sortlist = Specialcd[1:len(Specialcd)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialcd)):
                        Specialcd[i] = sortlist[i - 1]
            else:
                Specialcd = []

            if len(Specialda) > 1:
                pand = eval('%sa > %sd' % (Specialda[0], Specialda[0]))
                if pand:
                    sortlist = Specialda[1:len(Specialda)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialda)):
                        Specialda[i] = sortlist[i - 1]
                else:
                    sortlist = Specialda[1:len(Specialda)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialda)):
                        Specialda[i] = sortlist[i - 1]
            else:
                Specialda = []

            print('abcd', Specialab, Specialbc, Specialcd, Specialda)

            # =========== Inserting nodes into the 4 boundaries =======================

            Nab = [[] for i in range(2 * self.div1 + 1)]
            Nbc = [[] for i in range(2 * self.div2 + 1)]
            Ncd = [[] for i in range(2 * self.div1 + 1)]
            Nda = [[] for i in range(2 * self.div2 + 1)]

            for i in range(0, 2 * self.div1 + 1):
                x1 = xa + float(xb - xa) / (2 * self.div1) * i
                y1 = ya + float(yb - ya) / (2 * self.div1) * i
                z1 = za + float(zb - za) / (2 * self.div1) * i
                Nab[i].append(x1)
                Nab[i].append(y1)
                Nab[i].append(z1)

            for i in range(0, 2 * self.div2 + 1):
                x1 = xb + float(xc - xb) / (2 * self.div2) * i
                y1 = yb + float(yc - yb) / (2 * self.div2) * i
                z1 = zb + float(zc - zb) / (2 * self.div2) * i
                Nbc[i].append(x1)
                Nbc[i].append(y1)
                Nbc[i].append(z1)

            for i in range(0, 2 * self.div1 + 1):
                x1 = xc + float(xd - xc) / (2 * self.div1) * i
                y1 = yc + float(yd - yc) / (2 * self.div1) * i
                z1 = zc + float(zd - zc) / (2 * self.div1) * i
                Ncd[i].append(x1)
                Ncd[i].append(y1)
                Ncd[i].append(z1)

            for i in range(0, 2 * self.div2 + 1):
                x1 = xd + float(xa - xd) / (2 * self.div2) * i
                y1 = yd + float(ya - yd) / (2 * self.div2) * i
                z1 = zd + float(za - zd) / (2 * self.div2) * i
                Nda[i].append(x1)
                Nda[i].append(y1)
                Nda[i].append(z1)


            if len(Specialab) > 0:
                if Specialab[0] == 'x' or Specialab[0] == 'X':
                    jj = 0
                elif Specialab[0] == 'y' or Specialab[0] == 'Y':
                    jj = 1
                elif Specialab[0] == 'z' or Specialab[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nab[i][jj], range(0, len(Nab)))

                OriginInsert = [0]
                for i in range(1, len(Specialab)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialab[i] - InsNodes[j - 1]
                        obj2 = Specialab[i] - InsNodes[j]
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        if j == len(InsNodes):
                            print('Error: Specialab[i] should between %f and %f' % (Nab[0][jj], Nab[-1][jj]))

                    prop = float(Specialab[i] - Nab[OriginInsert[i - 1]][jj]) / (
                        Nab[OriginInsert[i]][jj] - Nab[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nab[k][0] = (Nab[k][0] - Nab[OriginInsert[i - 1]][0]) * prop + Nab[OriginInsert[i - 1]][0]
                        Nab[k][1] = (Nab[k][1] - Nab[OriginInsert[i - 1]][1]) * prop + Nab[OriginInsert[i - 1]][1]
                        Nab[k][2] = (Nab[k][2] - Nab[OriginInsert[i - 1]][2]) * prop + Nab[OriginInsert[i - 1]][2]

                    prop = float(Nab[-1][jj] - Specialab[i]) / (Nab[-1][jj] - Nab[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div1 + 1):
                        Nab[k][0] = Nab[-1][0] - (Nab[-1][0] - Nab[k][0]) * prop
                        Nab[k][1] = Nab[-1][1] - (Nab[-1][1] - Nab[k][1]) * prop
                        Nab[k][2] = Nab[-1][2] - (Nab[-1][2] - Nab[k][2]) * prop

            if len(Specialbc) > 0:
                if Specialbc[0] == 'x' or Specialbc[0] == 'X':
                    jj = 0
                elif Specialbc[0] == 'y' or Specialbc[0] == 'Y':
                    jj = 1
                elif Specialbc[0] == 'z' or Specialbc[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nbc[i][jj], range(0, len(Nbc)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialbc)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialbc[i] - InsNodes[j - 1]
                        obj2 = Specialbc[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialbc[i] should between %f and %f' % (Nbc[0][jj], Nbc[-1][jj]))

                    prop = float(Specialbc[i] - Nbc[OriginInsert[i - 1]][jj]) / (
                        Nbc[OriginInsert[i]][jj] - Nbc[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nbc[k][0] = (Nbc[k][0] - Nbc[OriginInsert[i - 1]][0]) * prop + Nbc[OriginInsert[i - 1]][0]
                        Nbc[k][1] = (Nbc[k][1] - Nbc[OriginInsert[i - 1]][1]) * prop + Nbc[OriginInsert[i - 1]][1]
                        Nbc[k][2] = (Nbc[k][2] - Nbc[OriginInsert[i - 1]][2]) * prop + Nbc[OriginInsert[i - 1]][2]

                    prop = float(Nbc[-1][jj] - Specialbc[i]) / (Nbc[-1][jj] - Nbc[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div2 + 1):
                        Nbc[k][0] = Nbc[-1][0] - (Nbc[-1][0] - Nbc[k][0]) * prop
                        Nbc[k][1] = Nbc[-1][1] - (Nbc[-1][1] - Nbc[k][1]) * prop
                        Nbc[k][2] = Nbc[-1][2] - (Nbc[-1][2] - Nbc[k][2]) * prop

            if len(Specialcd) > 0:
                Ncd.reverse()
                if Specialcd[0] == 'x' or Specialcd[0] == 'X':
                    jj = 0
                elif Specialcd[0] == 'y' or Specialcd[0] == 'Y':
                    jj = 1
                elif Specialcd[0] == 'z' or Specialcd[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Ncd[i][jj], range(0, len(Ncd)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialcd)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialcd[i] - InsNodes[j - 1]
                        obj2 = Specialcd[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialcd[i] should between %f and %f' % (Ncd[0][jj], Ncd[-1][jj]))

                    prop = float(Specialcd[i] - Ncd[OriginInsert[i - 1]][jj]) / (
                        Ncd[OriginInsert[i]][jj] - Ncd[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Ncd[k][0] = (Ncd[k][0] - Ncd[OriginInsert[i - 1]][0]) * prop + Ncd[OriginInsert[i - 1]][0]
                        Ncd[k][1] = (Ncd[k][1] - Ncd[OriginInsert[i - 1]][1]) * prop + Ncd[OriginInsert[i - 1]][1]
                        Ncd[k][2] = (Ncd[k][2] - Ncd[OriginInsert[i - 1]][2]) * prop + Ncd[OriginInsert[i - 1]][2]

                    prop = float(Ncd[-1][jj] - Specialcd[i]) / (Ncd[-1][jj] - Ncd[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div1 + 1):
                        Ncd[k][0] = Ncd[-1][0] - (Ncd[-1][0] - Ncd[k][0]) * prop
                        Ncd[k][1] = Ncd[-1][1] - (Ncd[-1][1] - Ncd[k][1]) * prop
                        Ncd[k][2] = Ncd[-1][2] - (Ncd[-1][2] - Ncd[k][2]) * prop
                Ncd.reverse()

            if len(Specialda) > 0:
                Nda.reverse()
                if Specialda[0] == 'x' or Specialda[0] == 'X':
                    jj = 0
                elif Specialda[0] == 'y' or Specialda[0] == 'Y':
                    jj = 1
                elif Specialda[0] == 'z' or Specialda[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nda[i][jj], range(0, len(Nda)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialda)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialda[i] - InsNodes[j - 1]
                        obj2 = Specialda[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialda[i] should between %f and %f' % (Nda[0][jj], Nda[-1][jj]))

                    prop = float(Specialda[i] - Nda[OriginInsert[i - 1]][jj]) / (
                        Nda[OriginInsert[i]][jj] - Nda[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nda[k][0] = (Nda[k][0] - Nda[OriginInsert[i - 1]][0]) * prop + Nda[OriginInsert[i - 1]][0]
                        Nda[k][1] = (Nda[k][1] - Nda[OriginInsert[i - 1]][1]) * prop + Nda[OriginInsert[i - 1]][1]
                        Nda[k][2] = (Nda[k][2] - Nda[OriginInsert[i - 1]][2]) * prop + Nda[OriginInsert[i - 1]][2]

                    prop = float(Nda[-1][jj] - Specialda[i]) / (Nda[-1][jj] - Nda[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div2 + 1):
                        Nda[k][0] = Nda[-1][0] - (Nda[-1][0] - Nda[k][0]) * prop
                        Nda[k][1] = Nda[-1][1] - (Nda[-1][1] - Nda[k][1]) * prop
                        Nda[k][2] = Nda[-1][2] - (Nda[-1][2] - Nda[k][2]) * prop
                Nda.reverse()

            print('================================')
            # print('Nab', Nab[13])
            # print('Ncd', Ncd[-14])
            print('================================')
            # print('Nbc', Nbc[13])
            # print('Nda', Nda[-14])
            print('================================')

            # ============ Inserting nodes into area =============

            Narea = [[] for i in range((2 * self.div1 + 1) * (2 * self.div2 + 1))]
            for i in range(0, 2 * self.div1 + 1):
                Narea[i].append(Nab[i][0])
                Narea[i].append(Nab[i][1])
                Narea[i].append(Nab[i][2])

            for j in range(1, 2 * self.div2):
                for i in range(0, 2 * self.div1 + 1):
                    xx1 = Nab[i][0]
                    xx2 = Ncd[2 * self.div1 - i][0]
                    xx3 = Nbc[j][0]
                    xx4 = Nda[2 * self.div2 - j][0]

                    yy1 = Nab[i][1]
                    yy2 = Ncd[2 * self.div1 - i][1]
                    yy3 = Nbc[j][1]
                    yy4 = Nda[2 * self.div2 - j][1]

                    zz1 = Nab[i][2]
                    zz2 = Ncd[2 * self.div1 - i][2]
                    zz3 = Nbc[j][2]
                    zz4 = Nda[2 * self.div2 - j][2]

                    dx1 = xx2 - xx1
                    dx2 = xx4 - xx3
                    dy1 = yy2 - yy1
                    dy2 = yy4 - yy3
                    dz1 = zz2 - zz1
                    dz2 = zz4 - zz3

                    eqs = []

                    # print(dx1, dx2, dy1, dy2, dz1, dz2)

                    if dx1 != 0 or dx2 != 0:
                        eqs.append([dx1, -dx2, xx1 - xx3])

                    if dy1 != 0 or dy2 != 0:
                        eqs.append([dy1, -dy2, yy1 - yy3])

                    if dz1 != 0 or dz2 != 0:
                        eqs.append([dz1, -dz2, zz1 - zz3])

                    demon = eqs[0][0] * eqs[1][1] - eqs[0][1] * eqs[1][0]
                    if demon != 0:
                        p1 = float(eqs[0][1] * eqs[1][2] - eqs[0][2] * eqs[1][1]) / demon
                        p2 = -float(eqs[0][0] * eqs[1][2] - eqs[0][2] * eqs[1][0]) / demon

                    elif demon == 0 and len(eqs) == 3:
                        demon = eqs[1][0] * eqs[2][1] - eqs[1][1] * eqs[2][0]
                        p1 = float(eqs[1][1] * eqs[2][2] - eqs[1][2] * eqs[2][1]) / demon
                        p2 = -float(eqs[1][0] * eqs[2][2] - eqs[1][2] * eqs[2][0]) / demon
                    else:
                        print('Check your input')

                    x1 = xx1 + dx1 * p1
                    y1 = yy1 + dy1 * p1
                    z1 = zz1 + dz1 * p1

                    Narea[(2 * self.div1 + 1) * j + i].append(x1)
                    Narea[(2 * self.div1 + 1) * j + i].append(y1)
                    Narea[(2 * self.div1 + 1) * j + i].append(z1)

            j = 2 * self.div1

            for i in range(-2 * self.div1 - 1, 0):
                Narea[i].append(Ncd[j][0])
                Narea[i].append(Ncd[j][1])
                Narea[i].append(Ncd[j][2])
                j = j - 1

            #print(Narea)

            # ======================== Create Elements ==============================

            Elements = []
            for i in range(0, (2 * self.div1 + 1) * (2 * self.div2 - 1), 2):
                if i % (4 * self.div1 + 2) <= 2 * self.div1 - 2:
                    ele = [int(i), int(i + 2), int(i + 4 + 4 * self.div1), int(i + 2 + 4 * self.div1), int(i + 1), int(i + 2 * self.div1 + 3), int(i + 3 + 4 * self.div1), int(i + 2 * self.div1 + 1), int(i + 2 * self.div1 + 2)]
                    Elements.append(ele)

            #print(Elements)

            # ====================== Writing nodes to tcl file ======================

            i = self.StartNode
            NodeListforEle = []
            for obj in Narea:
                if IfCombineSameNode:
                    temp = filter(lambda x: abs(x.x - obj[0]) < tolerance and abs(x.y - obj[1]) < tolerance and abs(x.z - obj[2]) < tolerance, Node.instances)
                    if len(temp) > 0:
                        if len(temp) > 1:
                            _Warning("In ShellMITC9Meshed, more than 1 node at location (%f, %f, %f)" % (obj[0], obj[1], obj[2]))
                        NodeListforEle.append(temp[0].n)
                    else:
                        Node(i, obj[0], obj[1], obj[2])
                        NodeListforEle.append(i)
                        i += 1
                else:
                    Node(i, obj[0], obj[1], obj[2])
                    NodeListforEle.append(i)
                    i += 1

            self.NextAvailableNode = i

            i = self.StartEle
            for obj in Elements:
                ShellElement.ShellMITC9(i, NodeListforEle[obj[0]], NodeListforEle[obj[1]], NodeListforEle[obj[2]], NodeListforEle[obj[3]], NodeListforEle[obj[4]], NodeListforEle[obj[5]], NodeListforEle[obj[6]], NodeListforEle[obj[7]], NodeListforEle[obj[8]], self.secTag)
                i += 1

            self.NextAvailableElement = i

        def NextAvailableNode(self):
            return self.NextAvailableNode
        def NextAvailableElement(self):
            return self.NextAvailableElement
        def node1(self):
            return self.node1
        def node2(self):
            return self.node2
        def node3(self):
            return self.node3
        def node4(self):
            return self.node4
        def div1(self):
            return self.div1
        def div2(self):
            return self.div2
        def StartNode(self):
            return self.StartNode
        def StartEle(self):
            return self.StartEle
        def secTag(self):
            return self.secTag
        def Specialab(self):
            return self.Specialab
        def Specialbc(self):
            return self.Specialbc
        def Specialcd(self):
            return self.Specialcd
        def Specialda(self):
            return self.Specialda
        def IfCombineSameNode(self):
            return self.IfCombineSameNode


    class ShellNLDKGTMeshed:
        def __init__(self, node1, node2, node3, node4, div1, div2, StartNode, StartEle, secTag, Specialab = [], Specialbc= [], Specialcd = [], Specialda = [], IfCombineSameNode = True):
            # 4 nodes should be in counter-clockwise order
            # The format for Specialbc: Specialab = ['y', -0.1, 0.1], Specialbc = ['z', 3.3065, 3.6935]

            tolerance = 1e-3

            self.node1 = node1
            self.node2 = node2
            self.node3 = node3
            self.node4 = node4
            self.div1 = div1
            self.div2 = div2
            self.StartNode = StartNode
            self.StartEle = StartEle
            self.secTag = secTag
            self.Specialab = Specialab
            self.Specialbc = Specialbc
            self.Specialcd = Specialcd
            self.Specialda = Specialda
            self.IfCombineSameNode = IfCombineSameNode


            node1i = filter(lambda x: x.n == self.node1, Node.instances)
            if len(node1i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node1)
            else:
                xa = node1i[0].x
                ya = node1i[0].y
                za = node1i[0].z

            node2i = filter(lambda x: x.n == self.node2, Node.instances)
            if len(node2i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node2)
            else:
                xb = node2i[0].x
                yb = node2i[0].y
                zb = node2i[0].z

            node3i = filter(lambda x: x.n == self.node3, Node.instances)
            if len(node3i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node3)
            else:
                xc = node3i[0].x
                yc = node3i[0].y
                zc = node3i[0].z

            node4i = filter(lambda x: x.n == self.node4, Node.instances)
            if len(node4i) == 0:
                Error("In ShellMITC9Meshed, No node tagged %d" % self.node4)
            else:
                xd = node4i[0].x
                yd = node4i[0].y
                zd = node4i[0].z

            # ============== Put Special Insert Point into right order =============
            if len(Specialab) > 1:
                pand = eval('%sb > %sa' % (Specialab[0], Specialab[0]))
                if pand:
                    sortlist = Specialab[1:len(Specialab)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialab)):
                        Specialab[i] = sortlist[i - 1]
                else:
                    sortlist = Specialab[1:len(Specialab)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialab)):
                        Specialab[i] = sortlist[i - 1]
            else:
                Specialab = []

            if len(Specialbc) > 1:
                pand = eval('%sc > %sb' % (Specialbc[0], Specialbc[0]))
                if pand:
                    sortlist = Specialbc[1:len(Specialbc)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialbc)):
                        Specialbc[i] = sortlist[i - 1]
                else:
                    sortlist = Specialbc[1:len(Specialbc)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialbc)):
                        Specialbc[i] = sortlist[i - 1]
            else:
                Specialbc = []

            if len(Specialcd) > 1:
                pand = eval('%sd > %sc' % (Specialcd[0], Specialcd[0]))
                if pand:
                    sortlist = Specialcd[1:len(Specialcd)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialcd)):
                        Specialcd[i] = sortlist[i - 1]
                else:
                    sortlist = Specialcd[1:len(Specialcd)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialcd)):
                        Specialcd[i] = sortlist[i - 1]
            else:
                Specialcd = []

            if len(Specialda) > 1:
                pand = eval('%sa > %sd' % (Specialda[0], Specialda[0]))
                if pand:
                    sortlist = Specialda[1:len(Specialda)]
                    sortlist = sorted(sortlist, reverse=True)
                    for i in range(1, len(Specialda)):
                        Specialda[i] = sortlist[i - 1]
                else:
                    sortlist = Specialda[1:len(Specialda)]
                    sortlist = sorted(sortlist)
                    for i in range(1, len(Specialda)):
                        Specialda[i] = sortlist[i - 1]
            else:
                Specialda = []

            print('abcd', Specialab, Specialbc, Specialcd, Specialda)

            # =========== Inserting nodes into the 4 boundaries =======================

            Nab = [[] for i in range(self.div1 + 1)]
            Nbc = [[] for i in range(self.div2 + 1)]
            Ncd = [[] for i in range(self.div1 + 1)]
            Nda = [[] for i in range(self.div2 + 1)]

            for i in range(0, self.div1 + 1):
                x1 = xa + float(xb - xa) / (self.div1) * i
                y1 = ya + float(yb - ya) / (self.div1) * i
                z1 = za + float(zb - za) / (self.div1) * i
                Nab[i].append(x1)
                Nab[i].append(y1)
                Nab[i].append(z1)

            for i in range(0, self.div2 + 1):
                x1 = xb + float(xc - xb) / (self.div2) * i
                y1 = yb + float(yc - yb) / (self.div2) * i
                z1 = zb + float(zc - zb) / (self.div2) * i
                Nbc[i].append(x1)
                Nbc[i].append(y1)
                Nbc[i].append(z1)

            for i in range(0, self.div1 + 1):
                x1 = xc + float(xd - xc) / (self.div1) * i
                y1 = yc + float(yd - yc) / (self.div1) * i
                z1 = zc + float(zd - zc) / (self.div1) * i
                Ncd[i].append(x1)
                Ncd[i].append(y1)
                Ncd[i].append(z1)

            for i in range(0, self.div2 + 1):
                x1 = xd + float(xa - xd) / (self.div2) * i
                y1 = yd + float(ya - yd) / (self.div2) * i
                z1 = zd + float(za - zd) / (self.div2) * i
                Nda[i].append(x1)
                Nda[i].append(y1)
                Nda[i].append(z1)


            if len(Specialab) > 0:
                if Specialab[0] == 'x' or Specialab[0] == 'X':
                    jj = 0
                elif Specialab[0] == 'y' or Specialab[0] == 'Y':
                    jj = 1
                elif Specialab[0] == 'z' or Specialab[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nab[i][jj], range(0, len(Nab)))

                OriginInsert = [0]
                for i in range(1, len(Specialab)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialab[i] - InsNodes[j - 1]
                        obj2 = Specialab[i] - InsNodes[j]
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        if j == len(InsNodes):
                            print('Error: Specialab[i] should between %f and %f' % (Nab[0][jj], Nab[-1][jj]))

                    prop = float(Specialab[i] - Nab[OriginInsert[i - 1]][jj]) / (
                        Nab[OriginInsert[i]][jj] - Nab[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nab[k][0] = (Nab[k][0] - Nab[OriginInsert[i - 1]][0]) * prop + Nab[OriginInsert[i - 1]][0]
                        Nab[k][1] = (Nab[k][1] - Nab[OriginInsert[i - 1]][1]) * prop + Nab[OriginInsert[i - 1]][1]
                        Nab[k][2] = (Nab[k][2] - Nab[OriginInsert[i - 1]][2]) * prop + Nab[OriginInsert[i - 1]][2]

                    prop = float(Nab[-1][jj] - Specialab[i]) / (Nab[-1][jj] - Nab[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div1 + 1):
                        Nab[k][0] = Nab[-1][0] - (Nab[-1][0] - Nab[k][0]) * prop
                        Nab[k][1] = Nab[-1][1] - (Nab[-1][1] - Nab[k][1]) * prop
                        Nab[k][2] = Nab[-1][2] - (Nab[-1][2] - Nab[k][2]) * prop

            if len(Specialbc) > 0:
                if Specialbc[0] == 'x' or Specialbc[0] == 'X':
                    jj = 0
                elif Specialbc[0] == 'y' or Specialbc[0] == 'Y':
                    jj = 1
                elif Specialbc[0] == 'z' or Specialbc[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nbc[i][jj], range(0, len(Nbc)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialbc)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialbc[i] - InsNodes[j - 1]
                        obj2 = Specialbc[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialbc[i] should between %f and %f' % (Nbc[0][jj], Nbc[-1][jj]))

                    prop = float(Specialbc[i] - Nbc[OriginInsert[i - 1]][jj]) / (
                        Nbc[OriginInsert[i]][jj] - Nbc[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nbc[k][0] = (Nbc[k][0] - Nbc[OriginInsert[i - 1]][0]) * prop + Nbc[OriginInsert[i - 1]][0]
                        Nbc[k][1] = (Nbc[k][1] - Nbc[OriginInsert[i - 1]][1]) * prop + Nbc[OriginInsert[i - 1]][1]
                        Nbc[k][2] = (Nbc[k][2] - Nbc[OriginInsert[i - 1]][2]) * prop + Nbc[OriginInsert[i - 1]][2]

                    prop = float(Nbc[-1][jj] - Specialbc[i]) / (Nbc[-1][jj] - Nbc[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div2 + 1):
                        Nbc[k][0] = Nbc[-1][0] - (Nbc[-1][0] - Nbc[k][0]) * prop
                        Nbc[k][1] = Nbc[-1][1] - (Nbc[-1][1] - Nbc[k][1]) * prop
                        Nbc[k][2] = Nbc[-1][2] - (Nbc[-1][2] - Nbc[k][2]) * prop

            if len(Specialcd) > 0:
                Ncd.reverse()
                if Specialcd[0] == 'x' or Specialcd[0] == 'X':
                    jj = 0
                elif Specialcd[0] == 'y' or Specialcd[0] == 'Y':
                    jj = 1
                elif Specialcd[0] == 'z' or Specialcd[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Ncd[i][jj], range(0, len(Ncd)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialcd)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialcd[i] - InsNodes[j - 1]
                        obj2 = Specialcd[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialcd[i] should between %f and %f' % (Ncd[0][jj], Ncd[-1][jj]))

                    prop = float(Specialcd[i] - Ncd[OriginInsert[i - 1]][jj]) / (
                        Ncd[OriginInsert[i]][jj] - Ncd[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Ncd[k][0] = (Ncd[k][0] - Ncd[OriginInsert[i - 1]][0]) * prop + Ncd[OriginInsert[i - 1]][0]
                        Ncd[k][1] = (Ncd[k][1] - Ncd[OriginInsert[i - 1]][1]) * prop + Ncd[OriginInsert[i - 1]][1]
                        Ncd[k][2] = (Ncd[k][2] - Ncd[OriginInsert[i - 1]][2]) * prop + Ncd[OriginInsert[i - 1]][2]

                    prop = float(Ncd[-1][jj] - Specialcd[i]) / (Ncd[-1][jj] - Ncd[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div1 + 1):
                        Ncd[k][0] = Ncd[-1][0] - (Ncd[-1][0] - Ncd[k][0]) * prop
                        Ncd[k][1] = Ncd[-1][1] - (Ncd[-1][1] - Ncd[k][1]) * prop
                        Ncd[k][2] = Ncd[-1][2] - (Ncd[-1][2] - Ncd[k][2]) * prop
                Ncd.reverse()

            if len(Specialda) > 0:
                Nda.reverse()
                if Specialda[0] == 'x' or Specialda[0] == 'X':
                    jj = 0
                elif Specialda[0] == 'y' or Specialda[0] == 'Y':
                    jj = 1
                elif Specialda[0] == 'z' or Specialda[0] == 'Z':
                    jj = 2
                InsNodes = map(lambda i: Nda[i][jj], range(0, len(Nda)))
                print('InsNodes', InsNodes)

                OriginInsert = [0]
                for i in range(1, len(Specialda)):
                    for j in range(1, len(InsNodes)):
                        obj1 = Specialda[i] - InsNodes[j - 1]
                        obj2 = Specialda[i] - InsNodes[j]
                        print('Obj12', obj1, obj2)
                        if obj1 * obj2 <= 0:
                            if abs(obj1) <= abs(obj2):
                                OriginInsert.append(j - 1)
                            else:
                                OriginInsert.append(j)
                            break
                        print('OriginInsert', OriginInsert)
                        if j == len(InsNodes):
                            print('Error: Specialda[i] should between %f and %f' % (Nda[0][jj], Nda[-1][jj]))

                    prop = float(Specialda[i] - Nda[OriginInsert[i - 1]][jj]) / (
                        Nda[OriginInsert[i]][jj] - Nda[OriginInsert[i - 1]][jj])
                    for k in range(OriginInsert[i - 1], OriginInsert[i]):
                        Nda[k][0] = (Nda[k][0] - Nda[OriginInsert[i - 1]][0]) * prop + Nda[OriginInsert[i - 1]][0]
                        Nda[k][1] = (Nda[k][1] - Nda[OriginInsert[i - 1]][1]) * prop + Nda[OriginInsert[i - 1]][1]
                        Nda[k][2] = (Nda[k][2] - Nda[OriginInsert[i - 1]][2]) * prop + Nda[OriginInsert[i - 1]][2]

                    prop = float(Nda[-1][jj] - Specialda[i]) / (Nda[-1][jj] - Nda[OriginInsert[i]][jj])
                    for k in range(OriginInsert[i], 2 * self.div2 + 1):
                        Nda[k][0] = Nda[-1][0] - (Nda[-1][0] - Nda[k][0]) * prop
                        Nda[k][1] = Nda[-1][1] - (Nda[-1][1] - Nda[k][1]) * prop
                        Nda[k][2] = Nda[-1][2] - (Nda[-1][2] - Nda[k][2]) * prop
                Nda.reverse()

            print('================================')
            # print('Nab', Nab[13])
            # print('Ncd', Ncd[-14])
            print('================================')
            # print('Nbc', Nbc[13])
            # print('Nda', Nda[-14])
            print('================================')
            print('Nab', Nab)
            print('Nbc', Nbc)
            print('Ncd', Ncd)
            print('Nda', Nda)

            # ============ Inserting nodes into area =============

            Narea = [[] for i in range((self.div1 + 1) * (self.div2 + 1))]
            for i in range(0, self.div1 + 1):
                Narea[i].append(Nab[i][0])
                Narea[i].append(Nab[i][1])
                Narea[i].append(Nab[i][2])

            for j in range(1, self.div2):
                for i in range(0, self.div1 + 1):
                    xx1 = Nab[i][0]
                    xx2 = Ncd[self.div1 - i][0]
                    xx3 = Nbc[j][0]
                    xx4 = Nda[self.div2 - j][0]

                    yy1 = Nab[i][1]
                    yy2 = Ncd[self.div1 - i][1]
                    yy3 = Nbc[j][1]
                    yy4 = Nda[self.div2 - j][1]

                    zz1 = Nab[i][2]
                    zz2 = Ncd[self.div1 - i][2]
                    zz3 = Nbc[j][2]
                    zz4 = Nda[self.div2 - j][2]

                    dx1 = xx2 - xx1
                    dx2 = xx4 - xx3
                    dy1 = yy2 - yy1
                    dy2 = yy4 - yy3
                    dz1 = zz2 - zz1
                    dz2 = zz4 - zz3

                    eqs = []

                    # print(dx1, dx2, dy1, dy2, dz1, dz2)

                    if dx1 != 0 or dx2 != 0:
                        eqs.append([dx1, -dx2, xx1 - xx3])

                    if dy1 != 0 or dy2 != 0:
                        eqs.append([dy1, -dy2, yy1 - yy3])

                    if dz1 != 0 or dz2 != 0:
                        eqs.append([dz1, -dz2, zz1 - zz3])

                    demon = eqs[0][0] * eqs[1][1] - eqs[0][1] * eqs[1][0]
                    if demon != 0:
                        p1 = float(eqs[0][1] * eqs[1][2] - eqs[0][2] * eqs[1][1]) / demon
                        p2 = -float(eqs[0][0] * eqs[1][2] - eqs[0][2] * eqs[1][0]) / demon

                    elif demon == 0 and len(eqs) == 3:
                        demon = eqs[1][0] * eqs[2][1] - eqs[1][1] * eqs[2][0]
                        p1 = float(eqs[1][1] * eqs[2][2] - eqs[1][2] * eqs[2][1]) / demon
                        p2 = -float(eqs[1][0] * eqs[2][2] - eqs[1][2] * eqs[2][0]) / demon
                    else:
                        print('Check your input')

                    x1 = xx1 + dx1 * p1
                    y1 = yy1 + dy1 * p1
                    z1 = zz1 + dz1 * p1

                    Narea[(self.div1 + 1) * j + i].append(x1)
                    Narea[(self.div1 + 1) * j + i].append(y1)
                    Narea[(self.div1 + 1) * j + i].append(z1)

            j = self.div1

            for i in range(-self.div1 - 1, 0):
                Narea[i].append(Ncd[j][0])
                Narea[i].append(Ncd[j][1])
                Narea[i].append(Ncd[j][2])
                j = j - 1

            print('Narea', len(Narea))

            # ======================== Create Elements ==============================

            Elements = []
            for i in range(0, (self.div1 + 1) * (self.div2 + 1)):
                if i % (self.div1 + 1) != self.div1 and i / (self.div1 + 1) < self.div2:
                    ele = [int(i), int(i + 1), int(i + 2 + self.div1)]
                    Elements.append(ele)
                    ele = [int(i), int(i + 2 + self.div1), int(i + 1 + self.div1)]
                    Elements.append(ele)

            print(Elements)

            # ====================== Writing nodes to tcl file ======================

            i = self.StartNode
            NodeListforEle = []
            for obj in Narea:
                if IfCombineSameNode:
                    temp = filter(lambda x: abs(x.x - obj[0]) < tolerance and abs(x.y - obj[1]) < tolerance and abs(x.z - obj[2]) < tolerance, Node.instances)
                    if len(temp) > 0:
                        if len(temp) > 1:
                            _Warning("In ShellMITC9Meshed, more than 1 node at location (%f, %f, %f)" % (obj[0], obj[1], obj[2]))
                        NodeListforEle.append(temp[0].n)
                    else:
                        Node(i, obj[0], obj[1], obj[2])
                        NodeListforEle.append(i)
                        i += 1
                else:
                    Node(i, obj[0], obj[1], obj[2])
                    NodeListforEle.append(i)
                    i += 1

            self.NextAvailableNode = i

            i = self.StartEle
            for obj in Elements:
                ShellElement.ShellNLDKGT(i, NodeListforEle[obj[0]], NodeListforEle[obj[1]], NodeListforEle[obj[2]], self.secTag)
                i += 1

            self.NextAvailableElement = i

        def NextAvailableNode(self):
            return self.NextAvailableNode
        def NextAvailableElement(self):
            return self.NextAvailableElement
        def node1(self):
            return self.node1
        def node2(self):
            return self.node2
        def node3(self):
            return self.node3
        def node4(self):
            return self.node4
        def div1(self):
            return self.div1
        def div2(self):
            return self.div2
        def StartNode(self):
            return self.StartNode
        def StartEle(self):
            return self.StartEle
        def secTag(self):
            return self.secTag
        def Specialab(self):
            return self.Specialab
        def Specialbc(self):
            return self.Specialbc
        def Specialcd(self):
            return self.Specialcd
        def Specialda(self):
            return self.Specialda
        def IfCombineSameNode(self):
            return self.IfCombineSameNode