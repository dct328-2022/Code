class TimeSeries:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        TimeSeries.Counter += 1

    class Constant:
        Counter = 0
        def __init__(self, n, factor):
            TimeSeries.Constant.Counter += 1
            self.n = n
            if self.n in TimeSeries.nlist:
                Error("In TimeSeries, Constant, tag %d already exist" % self.n)
            else:
                TimeSeries.nlist.append(self.n)
            self.factor = factor
            self.name = "ConstantSeries%d" % TimeSeries.Constant.Counter
            self.command = "TimeSeries *%s = new ConstantSeries(%d, %f);\n" % (self.name, self.n, self.factor)
            TimeSeries.instances.append(self)

        def n(self):
            return self.n
        def factor(self):
            return self.factor
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["ConstantSeries.h"]

    class Empty:
        Counter = 0
        def __init__(self, n):
            TimeSeries.Empty.Counter += 1
            self.n = n
            if self.n in TimeSeries.nlist:
                Error("In TimeSeries, Constant, tag %d already exist" % self.n)
            else:
                TimeSeries.nlist.append(self.n)
            self.name = "EmptySeries%d" % TimeSeries.Empty.Counter
            self.command = "TimeSeries *EmptySeries%d = 0;\n" % TimeSeries.Empty.Counter
            TimeSeries.instances.append(self)

        def n(self):
            return self.n
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["ConstantSeries.h"]

    class Linear:
        Counter = 0
        def __init__(self, n, factor):
            TimeSeries.Linear.Counter += 1
            self.n = n
            if self.n in TimeSeries.nlist:
                Error("In TimeSeries, Linear, tag %d already exist" % self.n)
            else:
                TimeSeries.nlist.append(self.n)
            self.factor = factor
            self.name = "LinearSeries%d" % TimeSeries.Constant.Counter
            self.command = "TimeSeries *%s = new LinearSeries(%d, %f);\n" % (self.name, self.n, self.factor)
            TimeSeries.instances.append(self)

        def n(self):
            return self.n
        def factor(self):
            return self.factor
        def name(self):
            return self.name
        def command(self):
            return self.command
        def include(self):
            return ["LinearSeries.h"]

    class Sin:
        Counter = 0
        def __init__(self, n, startTime, finishTime, T, phaseshift, factor, zeroshift):
            TimeSeries.Sin.Counter += 1
            self.n = n
            if self.n in TimeSeries.nlist:
                Error("In TimeSeries, Sin, tag %d already exist" % self.n)
            else:
                TimeSeries.nlist.append(self.n)
            self.startTime = startTime
            self.finishTime = finishTime
            self.T = T
            self.phaseshift = phaseshift
            self.factor = factor
            self.zeroshift = zeroshift

            self.name = "TrigSeries%d" % TimeSeries.Sin.Counter
            self.command = "TimeSeries *%s = new TriangleSeries(%d, %f, %f, %f, %f, %f, %f);\n" % (self.name, self.n, self.startTime, self.finishTime, self.T, self.phaseshift, self.factor, self.zeroshift)
            TimeSeries.instances.append(self)

        def n(self):
            return self.n
        def startTime(self):
            return self.startTime
        def finishTime(self):
            return self.finishTime
        def T(self):
            return self.T
        def phaseshift(self):
            return self.phaseshift
        def factor(self):
            return self.factor
        def zeroshift(self):
            return self.zeroshift
        def command(self):
            return self.command
        def name(self):
            return self.name
        def include(self):
            return ["TriangleSeries.h"]


    class Path:
        Counter = 0
        def __init__(self, n, filename, dt, factor, useLast = False, prependZero = False, startTime = 0):
            TimeSeries.Path.Counter += 1
            self.n = n
            if self.n in TimeSeries.nlist:
                Error("In TimeSeries, Path, tag %d already exist" % self.n)
            else:
                TimeSeries.nlist.append(self.n)
            self.filename = filename
            self.dt = dt
            self.factor = factor

            if useLast == False:
                self.useLast = 'false'
            elif useLast == True:
                self.useLast = 'true'

            if prependZero == False:
                self.prependZero = 'false'
            elif prependZero == True:
                self.prependZero = 'true'

            self.startTime = startTime
            self.name = "PathTimeSeries%d" % TimeSeries.Path.Counter
            self.command = '''TimeSeries *%s = new PathSeries(%d, "%s", %f, %f, %s, %s, %f);\n''' % (self.name, self.n, self.filename, self.dt, self.factor, self.useLast, self.prependZero, self.startTime)

            TimeSeries.instances.append(self)

        def n(self):
            return self.n
        def filename(self):
            return self.filename
        def dt(self):
            return self.dt
        def factor(self):
            return self.factor
        def useLast(self):
            return self.useLast
        def prependZero(self):
            return self.prependZero
        def startTime(self):
            return self.startTime
        def name(self):
            return self.name
        def include(self):
            return ['PathSeries.h']
        def command(self):
            return self.command


