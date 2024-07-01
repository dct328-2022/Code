class Domain:
    instances = []
    def __init__(self):
        print("Domain Created")
        Domain.instances.append(self)
        self.command = "Domain *theDomain = new Domain();\n"
        self.command += "int i = 1;\nint j = 1;\n"
    def include(self):
        return ["stdlib.h", "StandardStream.h", "OPS_Globals.h", "ArrayOfTaggedObjects.h", "OPS_Stream.h", "DOF_Numberer.h", "Domain.h", "ID.h", "OPS_Stream.h", "FileStream.h", "Vector.h", "math.h"]
    def command(self):
        return self.command

class Node:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self, n, x, y, z, dof=6):
        self.n = n
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.dof = dof
        Node.Counter += 1

        self.command = "Node *node%d = new Node(%d, %d, %f, %f, %f);\ntheDomain->addNode(node%d);\n" % (self.n, self.n, self.dof, self.x, self.y, self.z, self.n)
        if self.n in Node.nlist:
            Error("There's already a Node No.%d" % self.n)
        else:
            Node.nlist.append(n)
            Node.instances.append(self)

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
        return self.command

class CopyNodes:
    def __init__(self, nodeset, dirvector, TagPlus):
        for node in nodeset:
            Node(node.n + TagPlus, node.x + dirvector[0], node.y + dirvector[1], node.z + dirvector[2])

class SPConstraint:
    Counter = 0
    instances = []
    def __init__(self, NodeTag, s1, s2, s3, s4, s5, s6):
        self.NodeTag = NodeTag
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.s5 = s5
        self.s6 = s6
        SPConstraint.Counter += 1
        self.name = "sp%d" % SPConstraint.Counter

        self.command = ""

        if self.s1 == 1:
            self.command += "SP_Constraint *%s_1 = new SP_Constraint(%d, 0, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_1);\n" % self.name
        if self.s2 == 1:
            self.command += "SP_Constraint *%s_2 = new SP_Constraint(%d, 1, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_2);\n" % self.name
        if self.s3 == 1:
            self.command += "SP_Constraint *%s_3 = new SP_Constraint(%d, 2, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_3);\n" % self.name
        if self.s4 == 1:
            self.command += "SP_Constraint *%s_4 = new SP_Constraint(%d, 3, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_4);\n" % self.name
        if self.s5 == 1:
            self.command += "SP_Constraint *%s_5 = new SP_Constraint(%d, 4, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_5);\n" % self.name
        if self.s6 == 1:
            self.command += "SP_Constraint *%s_6 = new SP_Constraint(%d, 5, 1);\n" % (self.name, self.NodeTag)
            self.command += "theDomain->addSP_Constraint(%s_6);\n" % self.name

        SPConstraint.instances.append(self)

    def NodeTag(self):
        return self.NodeTag
    def s1(self):
        return self.s1
    def s2(self):
        return self.s2
    def s3(self):
        return self.s3
    def s4(self):
        return self.s4
    def s5(self):
        return self.s5
    def s6(self):
        return self.s6
    def command(self):
        return self.command
    def include(self):
        return ["SP_Constraint.h"]


class MPConstraint:
    Counter = 0
    instances = []
    def __init__(self):
        MPConstraint.Counter += 1

    class equalDOF:
        Counter = 0
        def __init__(self, node1, node2, equaleddofs):
            MPConstraint.equalDOF.Counter += 1
            self.node1 = node1
            self.node2 = node2
            self.equaleddofs = equaleddofs
            self.n = MPConstraint.equalDOF.Counter
            self.name = "mp%d" % MPConstraint.equalDOF.Counter
            self.command = ""
            self.status = False

            for obj in MPConstraint.instances:
                if hasattr(obj, 'equaleddofs'):
                    if sorted(self.equaleddofs) == sorted(obj.equaleddofs):
                        self.status = True
                        self.constrmat = obj.n


            if MPConstraint.equalDOF.Counter == 1:
                self.command += "ID DofsForEqualDof(6);\n"
                self.command += "DofsForEqualDof(0) = 0;\n"
                self.command += "DofsForEqualDof(1) = 1;\n"
                self.command += "DofsForEqualDof(2) = 2;\n"
                self.command += "DofsForEqualDof(3) = 3;\n"
                self.command += "DofsForEqualDof(4) = 4;\n"
                self.command += "DofsForEqualDof(5) = 5;\n"

            if self.status == False:
                self.command += "Matrix mpconstr%d(6, 6);\n" % self.n
                for obj in self.equaleddofs:
                    self.command += "mpconstr%d(%d, %d) = 1;\n" % (self.n, obj - 1, obj - 1)
                self.constrmat = self.n

            self.command += "MP_Constraint *%s = new MP_Constraint(%d, %d, %s, DofsForEqualDof, DofsForEqualDof);\n" % (self.name, self.node1, self.node2, self.constrmat)


            MPConstraint.instances.append(self)

        def node1(self):
            return self.node1
        def node2(self):
            return self.node2
        def equaleddofs(self):
            return self.equaleddofs
        def command(self):
            return self.command
        def include(self):
            return ["MP_Constraint.h"]
