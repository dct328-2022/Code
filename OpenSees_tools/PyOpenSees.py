class Domain:
    def __init(self):
        print("Domain Created")
    def include(self):
        return ["stdlib.h", "StandardStream.h", "OPS_Globals.h", "ArrayOfTaggedObjects.h", "Domain.h"]
    def command(self):
        return "Domain *theDomain = new Domain();"

class Node:
    def __init__(self, n, x, y, z, dof=6):
        self.n = n
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.dof = dof

    def x(self):
        return self.x

    def y(self):
        return self.y

    def z(self):
        return self.z

    def n(self):
        return self.n

    def dof(self):
        return self.dof

    def include(self):
        return ["Node.h"]

    def command(self):
        return "Node *node%d = new Node(%d, %d, %f, %f, %f);\ntheDomain->addNode(node%d);\n" % (self.n, self.n, self.dof, self.x, self.y, self.z, self.n)


class GeometricTransformation:
    Counter = 0
    def __init__(self, n, type, xzx, xzy, xzz):
        self.n = n
        self.type = type
        self.xzx = xzx
        self.xzy = xzy
        self.xzz = xzz
        GeometricTransformation.Counter += 1

    def type(self):
        return self.type

    def n(self):
        return self.n

    def xzx(self):
        return self.xzx

    def xzy(self):
        return self.xzy

    def xzz(self):
        return self.xzz

    def include(self):
        if self.type == "Linear":
            return ["LinearCrdTransf3d.h"]
        elif self.type == "PDelta":
            return ["PDeltaCrdTransf3d.h"]
        elif self.type == "Corotational":
            return ["CorotCrdTransf3d.h"]

    def command(self):
        if GeometricTransformation.Counter == 1:
            c01 = "Vector Trans0(3);\n"
            c02 = "Trans0(0) = 0.0;\n"
            c03 = "Trans0(1) = 0.0;\n"
            c04 = "Trans0(2) = 0.0;\n"
        c1 = "Vector XZ%d(3);\n" % self.n
        c2 = "XZ%d(0) = %f;\n" % (self.n, self.xzx)
        c3 = "XZ%d(1) = %f;\n" % (self.n, self.xzy)
        c4 = "XZ%d(2) = %f;\n" % (self.n, self.xzz)
        if self.type == "Linear":
            c5 = "CrdTransf *GTrans%d = new LinearCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.n, self.n, self.n)
        elif self.type == "PDelta":
            c5 = "CrdTransf *GTrans%d = new PDeltaCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.n, self.n, self.n)
        elif self.type == "Corotational":
            c5 = "CrdTransf *GTrans%d = new CorotCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.n, self.n, self.n)
        if GeometricTransformation.Counter == 1:
            return c01 + c02 + c03 + c04 + c1 + c2 + c3 + c4 + c5
        else:
            return c1 + c2 + c3 + c4 + c5

class ElasticMaterial:
    def __init__(self, n, E):
        self.n = n
        self.E = E
    def n(self):
        return self.n
    def E(self):
        return self.E
    def include(self):
        return ["ElasticMaterial.h"]
    def command(self):
        return "UniaxialMaterial *UniaxialMaterial%d = new ElasticMaterial(%d, %f);\n" % (self.n, self.n, self.E)

class Steel02:
    def __init__(self, n, Fy, E, b, r0=19.0, cr1=0.925, cr2=0.15, a1=0, a2=1, a3=0, a4=1, sigInit=0):
        self.n = n
        self.E = E
        self.b = b
        self.r0 = r0
        self.cr1 = cr1
        self.cr2 = cr2
        self.a1 = a1
        self.Fy = Fy
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.sigInit = sigInit
    def include(self):
        return ["Steel02.h"]
    def command(self):
        return "UniaxialMaterial *UniaxialMaterial%d = new Steel02(%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f);\n" % (self.n, self.n, self.Fy, self.E, self.b, self.r0, self.cr1, self.cr2, self.a1, self.a2, self.a3, self.a4, self.sigInit)

class ElasticBeamColumn:
    def __init__(self, n, node1, node2, A, E, G, J, Iy, Iz, Trans, mass=0):
        self.n = n
        if type(node1) is int:
            self.node1 = node1
        elif type(node1) is instance:
            self.node1 = node1.n
        else:
            print("Error when reading node1 at element %d" % self.n)
        if type(node2) is int:
            self.node2 = node2
        elif type(node2) is instance:
            self.node2 = node2.n
        else:
            print("Error when reading node2 at element %d" % self.n)
        self.A = A
        self.E = E
        self.G = G
        self.J = J
        self.Iy = Iy
        self.Iz = Iz
        if type(Trans) is int:
            self.Trans = Trans
        elif type(Trans) is instance:
            self.Trans = Trans.n
        else:
            print("Error when reading GeoTrans at element %d" % self.n)
        self.mass = mass
    def include(self):
        return ["ElasticBeam3d.h"]
    def command(self):
        c1 = "ElasticBeam3d *ElasticBeam%d = new ElasticBeam3d(%d, %f, %f, %f, %f, %f, %f, %d, %d, *GTrans%d);\n" % (self.n, self.A, self.E, self.G, self.J, self.Iy, self.Iz, self.node1, self.node2, self.Trans)
        c2 = "theDomain->addElement(ElasticBeam%d);\n" % self.n
        return c1 + c2

class ElasticTimoshenkoBeamColumn:
    def __init__(self, n, node1, node2, E, G, A, Jx, Iy, Iz, Avy, Avz, Trans, mass=0, lenfactor=1):
        self.n = n
        self.E = E
        self.G = G
        self.A = A
        self.Jx = Jx
        self.Iy = Iy
        self.Iz = Iz
        self.Avy = Avy
        self.Avz = Avz
        self.mass = mass
        self.lenfactor = lenfactor
        if type(node1) is int:
            self.node1 = node1
        elif type(node1) is instance:
            self.node1 = node1.n
        else:
            print("Error when reading node1 at element %d" % self.n)
        if type(node2) is int:
            self.node2 = node2
        elif type(node2) is instance:
            self.node2 = node2.n
        else:
            print("Error when reading node2 at element %d" % self.n)
        if type(Trans) is int:
            self.Trans = Trans
        elif type(Trans) is instance:
            self.Trans = Trans.n
        else:
            print("Error when reading GeoTrans at element %d" % self.n)
    def include(self):
        return ["ElasticTimoshenkoBeam3d.h"]
    def command(self):
        c1 = "ElasticTimoshenkoBeam3d(%d, %d, %d, %f, %f, %f, %f, %f, %f, %f, %f, %d, %f, -lenfactor %f);" % (self.n, self.node1, self.node2, self.E, self.G, self.A, self.Jx, self.Iy, self.Iz, self.Avy, self.Avz, self.Trans, self.mass, self.lenfactor)
        c2 = "theDomain->addElement(ElasticTimoshenkoBeam%d);\n" % self.n
        return c1 + c2

class HSSFiberSection:
    Counter = 0
    def __init__(self, n, Width, Thick, Mat, nthick, nwidth):
        self.n = n
        self.Width = Width
        self.Thick = Thick
        self.nthick = nthick
        self.nwidth = nwidth
        if type(Mat) is instance
            self.Mat = Mat.n
        elif type(Mat) is int
            self.Mat = Mat
        HSSFiberSection.Counter += 1
    def include(self):
        return ['Fiber.h', 'FiberSection3d.h', 'UniaxialFiber3d.h']
    def command(self):
        if HSSFiberSection.Counter == 1:
            c1 = "int i = 1;\n"
            c1 = c1 + "int j = 1;\n"
            c1 = c1 + "double locx;\n"
            c1 = c1 + "double locy;\n"
            c1 = c1 + "double AFiber;\n"
            c1 = c1 + "double Thick;\n"
            c1 = c1 + "double Width;\n"
            c1 = c1 + "double nthick;\n"
            c1 = c1 + "double nwidth;\n"
            c1 = c1 + "int tempno;\n"
            c1 = c1 + "Fiber *fibers%d[%d];\n" % (self.n, 4*self.nthick*self.nwidth)
        else:
            c1 = "Fiber *fibers%d[%d];\n" % (self.n, 4*self.nthick*self.nwidth)
        c1 = c1 + "Thick = %f\n" % self.Thick
        c1 = c1 + "Width = %f\n" % self.Width
        c1 = c1 + "nthick = %d\n" % self.nthick
        c1 = c1 + "nwidth = %d\n" % self.nwidth

        c1 = c1 + "for (i = 0; i < nthick; i++)\n{\n"
        c1 = c1 + "for (j = 0; j < nwidth; j++)\n{\n"
        c1 = c1 + "locx = ((4 * Thick * j * i - 4 * Thick * j * nthick - 2 * Thick * i * nwidth + 2 * Thick * nthick * nwidth + 2 * Width * j * nthick - Width * nthick * nwidth + 2 * Thick * j + 2 * Thick * i - 2 * Thick * nthick - Thick * nwidth + Width * nthick + Thick) / nthick / nwidth) / 0.2e1;\n"
        c1 = c1 + "locy = ((2 * Thick * i - 2 * Thick * nthick + Width * nthick - Thick) / nthick) / 0.2e1;\n"
        c1 = c1 + "AFiber = (2 * Thick * i - 2 * Thick * nthick + Width * nthick + Thick) * Thick * pow((double) nthick, (double) (-2)) / nwidth;\n"
        c1 = c1 + "tempno = 10*(i - 1) + j - 1;\n"
        c1 = c1 + "fibers%d[tempno] = new UniaxialFiber3d(tempno + 1, *ElsPla1, AFiber, locx, locy);\n}\n}\n" % self.n

        c1 = c1 + "for (i = 0; i < nthick; i++)\n{\n"
        c1 = c1 + "for (j = 0; j < nwidth; j++)\n{\n"
        c1 = c1 + "locy = -(((4 * Thick * j * i - 4 * Thick * j * nthick - 2 * Thick * i * nwidth + 2 * Thick * nthick * nwidth + 2 * Width * j * nthick - Width * nthick * nwidth + 2 * Thick * j + 2 * Thick * i - 2 * Thick * nthick - Thick * nwidth + Width * nthick + Thick) / nthick / nwidth) / 0.2e1);\n"
        c1 = c1 + "locx = ((2 * Thick * i - 2 * Thick * nthick + Width * nthick - Thick) / nthick) / 0.2e1;\n"
        c1 = c1 + "AFiber = (2 * Thick * i - 2 * Thick * nthick + Width * nthick + Thick) * Thick * pow((double) nthick, (double) (-2)) / nwidth;\n"
        c1 = c1 + "tempno = 10*(i - 1) + j - 1 + 100;\n"
        c1 = c1 + "fibers%d[tempno] = new UniaxialFiber3d(tempno + 1, *ElsPla1, AFiber, locx, locy);\n}\n}\n" % self.n

        c1 = c1 + "for (i = 0; i < nthick; i++)\n{\n"
        c1 = c1 + "for (j = 0; j < nwidth; j++)\n{\n"
        c1 = c1 + "locx = -(((4 * Thick * j * i - 4 * Thick * j * nthick - 2 * Thick * i * nwidth + 2 * Thick * nthick * nwidth + 2 * Width * j * nthick - Width * nthick * nwidth + 2 * Thick * j + 2 * Thick * i - 2 * Thick * nthick - Thick * nwidth + Width * nthick + Thick) / nthick / nwidth) / 0.2e1);\n"
        c1 = c1 + "locy = -(((2 * Thick * i - 2 * Thick * nthick + Width * nthick - Thick) / nthick) / 0.2e1);\n"
        c1 = c1 + "AFiber = (2 * Thick * i - 2 * Thick * nthick + Width * nthick + Thick) * Thick * pow((double) nthick, (double) (-2)) / nwidth;\n"
        c1 = c1 + "tempno = 10*(i - 1) + j - 1 + 200;\n"
        c1 = c1 + "fibers%d[tempno] = new UniaxialFiber3d(tempno + 1, *ElsPla1, AFiber, locx, locy);\n}\n}\n" % self.n

        c1 = c1 + "for (i = 0; i < nthick; i++)\n{\n"
        c1 = c1 + "for (j = 0; j < nwidth; j++)\n{\n"
        c1 = c1 + "locy = (((4 * Thick * j * i - 4 * Thick * j * nthick - 2 * Thick * i * nwidth + 2 * Thick * nthick * nwidth + 2 * Width * j * nthick - Width * nthick * nwidth + 2 * Thick * j + 2 * Thick * i - 2 * Thick * nthick - Thick * nwidth + Width * nthick + Thick) / nthick / nwidth) / 0.2e1);\n"
        c1 = c1 + "locx = -(((2 * Thick * i - 2 * Thick * nthick + Width * nthick - Thick) / nthick) / 0.2e1);\n"
        c1 = c1 + "AFiber = (2 * Thick * i - 2 * Thick * nthick + Width * nthick + Thick) * Thick * pow((double) nthick, (double) (-2)) / nwidth;\n"
        c1 = c1 + "tempno = 10*(i - 1) + j - 1 + 300;\n"
        c1 = c1 + "fibers%d[tempno] = new UniaxialFiber3d(tempno + 1, *ElsPla1, AFiber, locx, locy);\n}\n}\n" % self.n

        c1 = c1 + "SectionForceDeformation *ColumnSection%d[10];\n" % self.n
        c1 = c1 + "for (i = 0; i < 10; i++)\n"
        c1 = c1 + "ColumnSection%d[i] = new FiberSection3d(i + 1, 400, fibers%d);\n" % (self.n, self.n)

        return c1

class BeamIntegration:
    def __init__(self, n, type, nIP=10, Locs=0):
        self.n = n
        self.type = type
        self.nIP = nIP
        self.Locs = Locs
    def include(self):
        if self.type == "Lobatto":
            return ["LobattoBeamIntegration.h"]
        elif self.type == "FixedLocation":
            return ["FixedLocationBeamIntegration.h"]
    def command(self):
        if self.type == "Lobatto":
            return "BeamIntegration *integrateon%d = new LobattoBeamIntegration();\n" % self.n
        elif self.type == "FixedLocation":
            c1 = "Vector VecLoc%d(10);\n" % self.n
            c1 = c1 + "for(i=0;i<%d;i++)\n" % self.nIP
            c1 = c1 + "VecLoc%d(i) = 1.0/%d * (double)i;\n" % (self.n, nIP - 1)
            c1 = c1 + "BeamIntegration *integrateon%d = new FixedLocationBeamIntegration(%d, VecLoc%d);\n" % (self.n, self.n)
            return c1


theDomain = Domain()
n1 = Node(1, 0.0, 0.0, 0.0)
print(type(n1))
