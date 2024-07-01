class LoadPattern:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        LoadPattern.Counter += 1

    class LoadPattern:
        Counter = 0
        def __init__(self, n, tstag, factor = 1):
            LoadPattern.LoadPattern.Counter += 1
            self.n = n
            self.factor = factor
            self.tstag = tstag

            tslist = filter(lambda x: x.n == self.tstag, TimeSeries.instances)
            if len(tslist) == 0:
                Error("In LoadPattern, No TimeSeries tagged %d" % self.tstag)
            else:
                tsins = tslist[0]

            self.name = "LoadPattern%d" % LoadPattern.LoadPattern.Counter
            if self.factor == 1:
                self.command = "LoadPattern *%s = new LoadPattern(%d);\n" % (self.name, self.n)
            else:
                self.command = "LoadPattern *%s = new LoadPattern(%d, %f);\n" % (self.name, self.n, self.factor)

            self.command += "%s->setTimeSeries(%s);\n" % (self.name, tsins.name)
            #self.command += "theDomain->addLoadPattern(%s);\n" % self.name

            LoadPattern.nlist.append(self.n)
            LoadPattern.instances.append(self)

        def n(self):
            return self.n
        def factor(self):
            return self.factor
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["LoadPattern.h"]

    class addLoadPattern:
        Counter = 0
        def __init__(self, LoadPatternList):
            LoadPattern.addLoadPattern.Counter += 1
            self.LoadPatternList = LoadPatternList
            self.command = ""
            LoadPatternSet = []
            for item in LoadPattern.instances:
                if "theDomain->addLoadPattern" not in item.command:
                    LoadPatternSet.append(item)
            LoadPatterns = filter(lambda x: x.n in self.LoadPatternList, LoadPatternSet)
            for obj in LoadPatterns:
                self.command += "theDomain->addLoadPattern(%s);\n" % obj.name
            LoadPattern.instances.append(self)

        def command(self):
            return self.command

        def include(self):
            return []


    class MultipleSupport:
        Counter = 0

        def __init__(self, n):
            LoadPattern.MultipleSupport.Counter += 1
            self.n = n

            self.name = "LoadPattern%d" % LoadPattern.MultipleSupport.Counter
            self.command = "LoadPattern *%s = new MultiSupportPattern(%d);\n" % (self.name, self.n)

            LoadPattern.nlist.append(self.n)
            LoadPattern.instances.append(self)

        def n(self):
            return self.n

        def name(self):
            return self.name

        def command(self):
            return self.command

        def include(self):
            return ["LoadPattern.h", "MultiSupportPattern.h"]

class GroundMotion:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self, dispSeries, velSeries, accelSeries, factor):
        GroundMotion.Counter += 1
        self.dispSeries = dispSeries.name
        self.velSeries = velSeries.name
        self.accelSeries = accelSeries.name
        self.factor = factor
        self.name = "GroundMotion%d" % GroundMotion.Counter
        if GroundMotion.Counter == 1:
            self.command = "TimeSeriesIntegrator* seriesIntegrator = 0;\n"
        else:
            self.command = ""
        self.command += "GroundMotion *%s = new GroundMotion(%s, %s, %s, seriesIntegrator, 0.01, %f);\n" % (self.name, self.dispSeries, self.velSeries, self.accelSeries, self.factor)
        GroundMotion.instances.append(self)

    def dispSeries(self):
        return self.dispSeries
    def velSeries(self):
        return self.velSeries
    def accelSeries(self):
        return self.accelSeries
    def factor(self):
        return self.factor
    def name(self):
        return self.name
    def command(self):
        return self.command
    def include(self):
        return ['GroundMotion.h']

class ImposedMotion:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self, node, ndof, pattern, theGroundMotion):
        ImposedMotion.Counter += 1
        self.node = node
        self.ndof = ndof
        self.pattern = pattern
        self.theGroundMotion = theGroundMotion
        self.name = "ImposedMotion%d" % ImposedMotion.Counter
        self.command = "ImposedMotionSP *%s = new ImposedMotionSP(%d, %d, %d, *%s);\n" % (self.name, self.node, self.ndof, self.pattern.n, self.theGroundMotion.name)
        self.command += "theDomain->addSP_Constraint(%s, 1);\n" % self.name
        ImposedMotion.instances.append(self)
    def node(self):
        return self.node
    def ndof(self):
        return self.ndof
    def pattern(self):
        return self.pattern
    def theGroundMotion(self):
        return self.theGroundMotion
    def name(self):
        return self.name
    def commmand(self):
        return self.command
    def include(self):
        return ['ImposedMotionSP.h']

class Load:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        Load.Counter += 1

    class ConcentratedForce:
        Counter = 0
        def __init__(self, n, NodeTag, LoadList):
            Load.ConcentratedForce.Counter += 1
            self.n = n
            if self.n in Load.nlist:
                Error("In Load, ConcentratedForce, tag %d already exist" % self.n)
            else:
                Load.nlist.append(self.n)
            self.NodeTag = NodeTag
            self.LoadList = LoadList
            if len(self.LoadList) == 6:
                self.LoadList = LoadList
            else:
                Error("In Load, ConcentratedForce, LoadList should include 6 elements")

            self.name = "ConcentratedForce%d" % Load.ConcentratedForce.Counter

            self.command = "Vector Node%dLoad(6);\n" % self.NodeTag
            for i, obj in enumerate(self.LoadList):
                self.command += "Node%dLoad(%d) = %f;\n" % (self.NodeTag, i, obj)

            self.command += "NodalLoad *%s = new NodalLoad(%d, %d, Node%dLoad);\n" % (self.name, self.n, self.NodeTag, self.NodeTag)

            Load.nlist.append(self.n)
            Load.instances.append(self)

        def n(self):
            return self.n
        def type(self):
            return "ConcentratedForce"
        def NodeTag(self):
            return self.NodeTag
        def LoadList(self):
            return self.LoadList
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["NodalLoad.h"]

