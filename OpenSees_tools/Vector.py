class Vector:
    Counter = 0
    instances = []
    def __init__(self, name, dim, ValueList):
        self.ValueList = ValueList
        self.dim = dim
        self.name = name
        self.command = "Vector %s(%d);\n" % (self.name, self.dim)
        for i in range(0, self.dim):
            self.command += "%s(%d) = %f;\n" % (self.name, i, self.ValueList[i])
        Vector.Counter += 1
        Vector.instances.append(self)

    def x(self):
        return self.x
    def y(self):
        return self.y
    def z(self):
        return self.z
    def dim(self):
        return self.dim
    def name(self):
        return self.name
    def command(self):
        return self.command
    def include(self):
        return []
