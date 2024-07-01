class Friction:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        Friction.Counter += 1

    class Coulomb:
        # section Elastic $secTag $E $A $Iz $Iy $G $J
        Counter = 0
        def __init__(self, n, mu):
            Friction.Coulomb.Counter += 1
            self.name = "Coulomb%d" % Friction.Coulomb.Counter
            self.n = n
            self.mu = mu
            if self.n in Friction.nlist:
                Error("There's already an Friction Model No.%d" % self.n)
            else:
                Friction.nlist.append(n)
            self.command = "Coulomb *%s = new Coulomb(%d, %f);\n" % (self.name, self.n, self.mu)
            Friction.instances.append(self)

        def n(self):
            return n
        def name(self):
            return name
        def mu(self):
            return mu
        def command(self):
            return self.command
        def include(self):
            return ["Coulomb.h"]