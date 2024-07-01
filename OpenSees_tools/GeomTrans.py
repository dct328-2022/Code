class GeometricTransformation:
    Counter = 0
    LinearCounter = 0
    PDeltaCounter = 0
    CorotCounter = 0
    nlist = []
    instances = []
    def __init__(self, n, type, xzx, xzy, xzz):
        self.n = n
        self.type = type
        self.xzx = xzx
        self.xzy = xzy
        self.xzz = xzz
        GeometricTransformation.Counter += 1
        GeometricTransformation.instances.append(self)

        # If n is a unique tag for the node
        if self.n in GeometricTransformation.nlist:
            Error("There's already a Geometric Transformation No.%d" % self.n)
        else:
            GeometricTransformation.nlist.append(n)

        # Count the 3 types of Transformation
        if self.type == "Linear":
            GeometricTransformation.LinearCounter += 1
            self.name = self.type + str(GeometricTransformation.LinearCounter)
        elif self.type == "PDelta":
            GeometricTransformation.PDeltaCounter += 1
            self.name = self.type + str(GeometricTransformation.PDeltaCounter)
        elif self.type == "Corotational":
            GeometricTransformation.CorotCounter += 1
            self.name = self.type + str(GeometricTransformation.CorotCounter)
        else:
            Error('Unrecognized Type of Geometric Transformation %s No.%d' % (self.type, self.n))

        # commands
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
            c5 = "CrdTransf *%s = new LinearCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.name, self.n, self.n)
        elif self.type == "PDelta":
            c5 = "CrdTransf *%s = new PDeltaCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.name, self.n, self.n)
        elif self.type == "Corotational":
            c5 = "CrdTransf *%s = new CorotCrdTransf3d(%d, XZ%d, Trans0, Trans0);\n" % (self.name, self.n, self.n)
        if GeometricTransformation.Counter == 1:
            self.command = c01 + c02 + c03 + c04 + c1 + c2 + c3 + c4 + c5
        else:
            self.command = c1 + c2 + c3 + c4 + c5

    def type(self):
        return self.type

    def n(self):
        return self.n

    def include(self):
        return ["LinearCrdTransf3d.h", "PDeltaCrdTransf3d.h", "CorotCrdTransf3d.h"]

    def name(self):
        return self.name

    def xzx(self):
        return self.xzx

    def xzy(self):
        return self.xzy

    def xzz(self):
        return self.xzz

    def command(self):
        return self.command