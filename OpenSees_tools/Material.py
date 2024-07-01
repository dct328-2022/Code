class uniaxialMaterial:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        uniaxialMaterial.Counter += 1


    class Elastic:
        Counter = 0
        def __init__(self, n, E):
            self.n = n
            self.E = float(E)
            uniaxialMaterial.Elastic.Counter += 1
            self.name = 'ElasticMaterial%d' % uniaxialMaterial.Elastic.Counter
            self.command = "UniaxialMaterial *%s = new ElasticMaterial(%d, %f);\n" % (self.name, self.n, self.E)
            uniaxialMaterial.instances.append(self)
            if self.n in uniaxialMaterial.nlist:
                Error("There's already an uniaxialMaterial No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def include(self):
            return ["ElasticMaterial.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class ElasticPP:
        Counter = 0
        # uniaxialMaterial ElasticPP $matTag $E $epsyP <$epsyN $eps0>
        def __init__(self, n, E, epsyP, epsyN='epsyN', eps0=0):
            self.n = n
            self.E = float(E)
            self.epsyP = epsyP
            if epsyN == 'epsyN':
                self.epsyN = -epsyP
            else:
                self.epsyN = epsyN
            self.eps0 = eps0
            uniaxialMaterial.ElasticPP.Counter += 1
            self.name = 'ElasticPPMaterial%d' % uniaxialMaterial.ElasticPP.Counter
            if self.epsyP + self.epsyN == 0 and eps0 == 0:
                self.command = "UniaxialMaterial *%s = new ElasticPPMaterial(%d, %f, %f);\n" % (self.name, self.n, self.E, self.epsyP)
            else:
                self.command = "UniaxialMaterial *%s = new ElasticPPMaterial(%d, %f, %f, %f, %f);\n" % (self.name, self.n, self.E, self.epsyP, self.epsyN, self.eps0)
            uniaxialMaterial.instances.append(self)

            if self.n in uniaxialMaterial.nlist:
                Error("There's already an uniaxialMaterial No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def epsyP(self):
            return self.epsyP

        def epsyN(self):
            return self.epsyN

        def eps0(self):
            return self.eps0

        def include(self):
            return ["ElasticPPMaterial.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class Steel02:
        Counter = 0
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
            uniaxialMaterial.Steel02.Counter += 1
            self.name = 'Steel02Material%d' % uniaxialMaterial.Steel02.Counter
            self.command = "Steel02 *%s = new Steel02(%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f);\n" % (self.name, self.n, self.Fy, self.E, self.b, self.r0, self.cr1, self.cr2, self.a1, self.a2, self.a3, self.a4, self.sigInit)
            uniaxialMaterial.instances.append(self)
            if self.n in uniaxialMaterial.nlist:
                Error("There's already an uniaxialMaterial No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def b(self):
            return self.b

        def Fy(self):
            return self.Fy

        def sigInit(self):
            return self.sigInit

        def include(self):
            return ["Steel02.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class Steel01:
        Counter = 0
        def __init__(self, n, Fy, E, b, a1=0, a2=1, a3=0, a4=1):
            self.n = n
            self.E = E
            self.b = b
            self.a1 = a1
            self.Fy = Fy
            self.a2 = a2
            self.a3 = a3
            self.a4 = a4
            uniaxialMaterial.Steel01.Counter += 1
            self.name = 'Steel01Material%d' % uniaxialMaterial.Steel01.Counter
            self.command = "UniaxialMaterial *%s = new Steel01(%d, %f, %f, %f, %f, %f, %f, %f);\n" % (self.name, self.n, self.Fy, self.E, self.b, self.a1, self.a2, self.a3, self.a4)
            uniaxialMaterial.instances.append(self)
            if self.n in uniaxialMaterial.nlist:
                Error("There's already an uniaxialMaterial No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def include(self):
            return ["Steel01.h"]

        def n(self):
            return self.n

        def E(self):
            return self.E

        def b(self):
            return self.b

        def Fy(self):
            return self.Fy

        def name(self):
            return self.name

        def command(self):
            return self.command

    class ENT:
        Counter = 0
        def __init__(self, n, E):
            self.n = n
            self.E = E
            uniaxialMaterial.ENT.Counter += 1
            self.name = 'ENTMaterial%d' % uniaxialMaterial.ENT.Counter
            self.command = "UniaxialMaterial *%s = new ENTMaterial(%d, %f);\n" % (self.name, self.n, self.E)
            uniaxialMaterial.instances.append(self)
            if self.n in uniaxialMaterial.nlist:
                Error("There's already an uniaxialMaterial No.%d" % self.n)
            else:
                uniaxialMaterial.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def include(self):
            return ["ENTMaterial.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command


class NDMaterial:
    # nDMaterial ElasticIsotropic $matTag $E $v <$rho>
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        NDMaterial.Counter += 1

    class ElasticIsotropic:
        Counter = 0
        def __init__(self, n, E, v, rho=0):
            self.n = n
            self.E = E
            self.v = v
            self.rho = rho
            NDMaterial.ElasticIsotropic.Counter += 1
            self.name = 'ElasticIsotropic%d' % NDMaterial.ElasticIsotropic.Counter
            self.command = "NDMaterial *%s = new ElasticIsotropicThreeDimensional(%d, %f, %f, %f);\n" % (self.name, self.n, self.E, self.v, self.rho)
            NDMaterial.instances.append(self)
            if self.n in NDMaterial.nlist:
                Error("There's already a NDMaterial No.%d" % self.n)
            else:
                NDMaterial.nlist.append(n)

        def n(self):
            return self.n

        def E(self):
            return self.E

        def v(self):
            return self.v

        def rho(self):
            return self.rho

        def include(self):
            return ["ElasticIsotropicThreeDimensional.h"]

        def name(self):
            return self.name

        def command(self):
            return self.command

    class DruckerPrager:
        # nDMaterial DruckerPrager $matTag $k $G $sigmaY $rho $rhoBar $Kinf $Ko $delta1 $delta2 $H $theta $density <$atmPressure>
        Counter = 0
        def __init__(self, n, k, G, sigmaY, rho, rhoBar, Kinf, Ko, delta1, delta2, H, theta, density, atmPressure=101.0):
            self.n = n
            self.k = k
            self.G = G
            self.sigmaY = sigmaY
            self.rho = rho
            self.rhoBar = rhoBar
            self.Kinf = Kinf
            self.Ko = Ko
            self.delta1 = delta1
            self.delta2 = delta2
            self.H = H
            self.theta = theta
            self.density = density
            self.atmPressure = atmPressure
            NDMaterial.DruckerPrager.Counter += 1
            self.name = 'DruckerPrager%d' % NDMaterial.DruckerPrager.Counter
            self.command = "NDMaterial *%s = new DruckerPrager3D(%d, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f, %f);\n" % (self.name, self.n, self.k, self.G, self.sigmaY, self.rho, self.rhoBar, self.Kinf, self.Ko, self.delta1, self.delta2, self.H, self.theta, self.density, self.atmPressure)
            NDMaterial.instances.append(self)
            if self.n in NDMaterial.nlist:
                Error("There's already a NDMaterial No.%d" % self.n)
            else:
                NDMaterial.nlist.append(n)

        def n(self):
            return self.n

        def k(self):
            return self.k

        def G(self):
            return self.G

        def sigmaY(self):
            return self.sigmaY

        def rho(self):
            return self.rho

        def rhoBar(self):
            return self.rhoBar

        def Kinf(self):
            return self.Kinf

        def Ko(self):
            return sefl.Ko

        def delta1(self):
            return self.delta1

        def delta2(self):
            return self.delta2

        def H(self):
            return self.H

        def theta(self):
            return self.theta

        def density(self):
            return self.density

        def atmPressure(self):
            return self.atmPressure

        def include(self):
            return ['DruckerPrager3D.h']

        def name(self):
            return self.name

        def command(self):
            return self.command

    class PlateFiberMaterial:
        #nDMaterial PlateFiber $matTag $threeDTag
        Counter = 0
        def __init__(self, n, n2):
            self.n = n
            self.n2 = n2
            NDMaterial.PlateFiberMaterial.Counter += 1
            pnamelist = filter(lambda x: x.n == self.n2, NDMaterial.instances)
            if len(pnamelist) == 1:
                pname = pnamelist[0].name
            else:
                Error('In Plate Fiber Material, there are more than 1 element filtered from the list')

            self.name = pname + 'Plane'
            self.pname = pname
            self.command = "NDMaterial *%s = new PlateFiberMaterial(%d, *%s);\n" % (self.name, self.n, self.pname)
            NDMaterial.instances.append(self)
            if self.n in NDMaterial.nlist:
                Error("There's already a NDMaterial No.%d" % self.n)
            else:
                NDMaterial.nlist.append(n)

        def n(self):
            return self.n

        def n2(self):
            return self.n2

        def name(self):
            return self.name

        def pname(self):
            return self.pname

        def include(self):
            return ['PlateFiberMaterial.h']

        def command(self):
            return self.command




