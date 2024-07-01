class AnalysisOption:
    Counter = 0
    nlist = []
    instances = []
    def __init__(self):
        AnalysisOption.Counter += 1



    class addLoad:
        Counter = 0

        def __init__(self, LoadList, PatternTag):
            AnalysisOption.addLoad.Counter += 1
            self.LoadList = LoadList
            self.PatternTag = PatternTag
            self.Pattern = filter(lambda x: x.n == self.PatternTag, LoadPattern.instances)[0]
            self.command = ""
            Loads = filter(lambda x: x.n in LoadList, Load.instances)
            for obj in Loads:
                if obj.type() == "ConcentratedForce":
                    self.command += "theDomain->addNodalLoad(%s, %d);\n" % (obj.name, self.PatternTag)
            AnalysisOption.instances.append(self)

        def command(self):
            return self.command

        def include(self):
            return []

    class AnalysisModel:
        Counter = 0

        def __init__(self):
            AnalysisOption.AnalysisModel.Counter += 1
            self.name = "theModel%d" % AnalysisOption.AnalysisModel.Counter
            self.command = "AnalysisModel *theModel%d = new AnalysisModel();\n" % AnalysisOption.AnalysisModel.Counter
            AnalysisOption.instances.append(self)

        def command(self):
            return self.command
        def include(self):
            return ['AnalysisModel.h']
        def name(self):
            return self.name

    class Integrator:
        Counter = 0
        def __init__(self):
            AnalysisOption.Integrator.Counter += 1

        class LoadControl:
            Counter = 0
            def __init__(self, increment, iteration = 1, minstep = 'default', maxstep = 'default'):
                AnalysisOption.Integrator.LoadControl.Counter += 1
                self.increment = increment
                self.iteration = iteration

                if minstep == 'default':
                    self.minstep = self.increment
                else:
                    self.minstep = minstep

                if maxstep == 'default':
                    self.maxstep = self.increment
                else:
                    self.maxstep = maxstep

                self.name = "LoadControlIntegrator%d" % AnalysisOption.Integrator.LoadControl.Counter
                self.command = "StaticIntegrator *%s = new LoadControl(%f, %d, %f, %f);\n" % (self.name, self.increment, self.iteration, self.minstep, self.maxstep)
                AnalysisOption.instances.append(self)

            def command(self):
                return self.command
            def name(self):
                return self.name

            def increment(self):
                return self.increment
            def iteration(self):
                return self.iteration
            def minstep(self):
                return self.minstep
            def maxstep(self):
                return self.maxstep
            def include(self):
                return ['LoadControl.h']
            def type(self):
                return 'LoadControl'

        class Newmark:
            Counter = 0
            def __init__(self, gamma, beta):
                AnalysisOption.Integrator.Newmark.Counter += 1
                self.gamma = gamma
                self.beta = beta

                self.name = "NewmarkIntegrator%d" % AnalysisOption.Integrator.Newmark.Counter
                self.command = "TransientIntegrator *%s = new Newmark(%f, %f);\n" % (self.name, self.gamma, self.beta)
                AnalysisOption.instances.append(self)

            def gamma(self):
                return self.gamma
            def beta(self):
                return self.beta
            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['Newmark.h']
            def type(self):
                return 'Newmark'

    class ConstraintHandler:
        Counter = 0
        def __init__(self):
            AnalysisOption.ConstraintHandler.Counter += 1

        class Transformation:
            def __init__(self):
                self.command = "ConstraintHandler *TransfHandler = new TransformationConstraintHandler();\n"
                self.name = "TransfHandler"
                AnalysisOption.instances.append(self)

            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['TransformationConstraintHandler.h']
            def type(self):
                return 'Transformation'

    class Numberer:
        Counter = 0

        def __init__(self):
            pass

        class RCM:
            def __init__(self):
                AnalysisOption.Numberer.Counter += 1
                self.name = 'theNumberer%d' % AnalysisOption.Numberer.Counter
                self.command = "RCM *theRCM = new RCM();\n"
                self.command += "DOF_Numberer *%s = new DOF_Numberer(*theRCM);\n" % self.name
                AnalysisOption.instances.append(self)

            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['DOF_Numberer.h', 'RCM.h']
            def type(self):
                return 'RCM'

    class Solver:
        Counter = 0

        def __init__(self):
            pass

        class SparseSPD:
            def __init__(self):
                AnalysisOption.Solver.Counter += 1
                self.name = 'theSOE%d' % AnalysisOption.Solver.Counter
                self.command = "SymSparseLinSolver *SparseSPDSolver = new SymSparseLinSolver();\n"
                self.command += "SymSparseLinSOE *%s = new SymSparseLinSOE(*SparseSPDSolver, 1);\n" % self.name
                AnalysisOption.instances.append(self)

            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['SymSparseLinSOE.h', 'SymSparseLinSolver.h']
            def type(self):
                return 'SparseSPD'

        class UmfPack:
            def __init__(self):
                AnalysisOption.Solver.Counter += 1
                self.name = 'theSOE%d' % AnalysisOption.Solver.Counter
                self.command = "UmfpackGenLinSolver *UmfPackSolver = new UmfpackGenLinSolver();\n"
                self.command += "UmfpackGenLinSOE *%s = new UmfpackGenLinSOE(*UmfPackSolver, 1);\n" % self.name
                AnalysisOption.instances.append(self)

            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['UmfpackGenLinSOE.h', 'UmfpackGenLinSolver.h']
            def type(self):
                return 'UmfPack'

    class Test:
        Counter = 0

        def __init__(self):
            pass

        class EnergyIncrement:
            Counter = 0
            def __init__(self, tol, trialtimes):
                AnalysisOption.Test.EnergyIncrement.Counter += 1
                self.tol = str(tol)
                self.trialtimes = trialtimes
                self.name = "EnergyIncrementTest%d" % AnalysisOption.Test.EnergyIncrement.Counter
                self.command = "ConvergenceTest *%s = new CTestEnergyIncr(%s, %d, 1, 2, 100000);\n" % (self.name, self.tol, self.trialtimes)
                AnalysisOption.instances.append(self)

            def name(self):
                return self.name
            def tol(self):
                return self.tol
            def trialtimes(self):
                return self.trialtimes
            def command(self):
                return self.command
            def include(self):
                return ['CTestEnergyIncr.h']
            def type(self):
                return 'EnergyIncrement'

    class Algorithm:
        Counter = 0

        def __init__(self):
            pass

        class NewtonLineSearch:
            Counter = 0
            def __init__(self, TheTest, SearchType, parameters):
                AnalysisOption.Algorithm.NewtonLineSearch.Counter += 1
                self.TheTest = TheTest
                self.SearchType = SearchType
                self.parameters = parameters
                self.name = "NewtonLS%d" % AnalysisOption.Algorithm.NewtonLineSearch.Counter
                if self.SearchType == "InitialInterpolated":
                    if self.parameters == []:
                        self.command = "LineSearch *theSearch%d = new InitialInterpolatedLineSearch();\n" % AnalysisOption.Algorithm.NewtonLineSearch.Counter
                    else:
                        self.command = "LineSearch *theSearch%d = new InitialInterpolatedLineSearch(%f, %d, %f, %f, 1);\n" % (AnalysisOption.Algorithm.NewtonLineSearch.Counter, self.parameters[0], self.parameters[1], self.parameters[2], self.parameters[3])

                if self.SearchType == "Secant":
                    if self.parameters == []:
                        self.command = "LineSearch *theSearch%d = new SecantLineSearch();\n" % AnalysisOption.Algorithm.NewtonLineSearch.Counter
                    else:
                        self.command = "LineSearch *theSearch%d = new SecantLineSearch(%f, %d, %f, %f, 1);\n" % (AnalysisOption.Algorithm.NewtonLineSearch.Counter, self.parameters[0], self.parameters[1], self.parameters[2], self.parameters[3])
                self.command += "EquiSolnAlgo *%s = new NewtonLineSearch(*%s, theSearch%d);\n" % (self.name, self.TheTest.name, AnalysisOption.Algorithm.NewtonLineSearch.Counter)
                AnalysisOption.instances.append(self)

            def TheTest(self):
                return self.TheTest
            def SearchType(self):
                return self.SearchType
            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                if self.SearchType == "InitialInterpolated":
                    return ['LineSearch.h', 'NewtonLineSearch.h', 'InitialInterpolatedLineSearch.h']
                if self.SearchType == "Secant":
                    return ['LineSearch.h', 'NewtonLineSearch.h', 'SecantLineSearch.h']

            def type(self):
                return 'NewtonLineSearch'

        class KrylovNewton:
            Counter = 0
            def __init__(self, TheTest, tangent = 'Current', maxDim = 3):
                AnalysisOption.Algorithm.KrylovNewton.Counter += 1
                self.TheTest = TheTest
                self.tangent = tangent
                self.maxDim = maxDim
                self.name = "KLNewton%d" % AnalysisOption.Algorithm.KrylovNewton.Counter
                if self.tangent == 'Current' and self.maxDim == 3:
                    self.command = "EquiSolnAlgo *%s = new KrylovNewton();\n" % (self.name)
                else:
                    self.command = "EquiSolnAlgo *%s = new KrylovNewton(%s, %d);\n" % (self.name, self.tangent, self.maxDim)

                AnalysisOption.instances.append(self)

            def TheTest(self):
                return self.TheTest
            def tangent(self):
                return self.tangent
            def maxDim(self):
                return self.maxDim
            def command(self):
                return self.command
            def include(self):
                return ['KrylovNewton.h']
            def name(self):
                return self.name
            def type(self):
                return 'KrylovNewton'

        class BFGS:
            Counter = 0
            def __init__(self, TheTest, tangent = 'Current', maxDim = 10):
                AnalysisOption.Algorithm.BFGS.Counter += 1
                self.TheTest = TheTest
                self.tangent = tangent
                self.maxDim = maxDim
                self.name = "BFGS%d" % AnalysisOption.Algorithm.BFGS.Counter
                if self.tangent == 'Current' and self.maxDim == 10:
                    self.command = "EquiSolnAlgo *%s = new BFGS();\n" % (self.name)
                else:
                    self.command = "EquiSolnAlgo *%s = new BFGS(%s, %d);\n" % (self.name, self.tangent, self.maxDim)

                AnalysisOption.instances.append(self)

            def TheTest(self):
                return self.TheTest
            def tangent(self):
                return self.tangent
            def maxDim(self):
                return self.maxDim
            def command(self):
                return self.command
            def include(self):
                return ['BFGS.h']
            def name(self):
                return self.name
            def type(self):
                return 'BFGS'


    class Analysis:
        Counter = 0

        def __init__(self):
            pass

        class StaticAnalysis:
            Counter = 0
            def __init__(self, theHandler, theNumberer, theModel, theSolnAlgo, theSOE, theIntegrator, theTest):
                AnalysisOption.Analysis.StaticAnalysis.Counter += 1
                self.theHandler = theHandler
                self.theNumberer = theNumberer
                self.theModel = theModel
                self.theSolnAlgo = theSolnAlgo
                self.theSOE = theSOE
                self.theIntegrator = theIntegrator
                self.theTest = theTest

                self.name = "StaticAnalysis%d" % AnalysisOption.Analysis.StaticAnalysis.Counter
                self.command = "StaticAnalysis %s(*theDomain, *%s, *%s, *%s, *%s, *%s, *%s, %s);\n" % (self.name, self.theHandler.name, self.theNumberer.name, self.theModel.name, self.theSolnAlgo.name, self.theSOE.name, self.theIntegrator.name, self.theTest.name)
                AnalysisOption.instances.append(self)

            def theHandler(self):
                return self.theHandler
            def theNumberer(self):
                return self.theNumberer
            def theModel(self):
                return self.theModel
            def theSolnAlgo(self):
                return self.theSolnAlgo
            def theSOE(self):
                return self.theSOE
            def theIntegrator(self):
                return self.theIntegrator
            def theTest(self):
                return self.theTest
            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['StaticAnalysis.h']
            def type(self):
                return "StaticAnalysis"

        class VariableTransientAnalysis:
            Counter = 0
            def __init__(self, theHandler, theNumberer, theModel, theSolnAlgo, theSOE, theIntegrator, theTest):
                AnalysisOption.Analysis.VariableTransientAnalysis.Counter += 1
                self.theHandler = theHandler
                self.theNumberer = theNumberer
                self.theModel = theModel
                self.theSolnAlgo = theSolnAlgo
                self.theSOE = theSOE
                self.theIntegrator = theIntegrator
                self.theTest = theTest

                self.name = "VariableTransientAnalysis%d" % AnalysisOption.Analysis.VariableTransientAnalysis.Counter
                self.command = "VariableTimeStepDirectIntegrationAnalysis %s(*theDomain, *%s, *%s, *%s, *%s, *%s, *%s, %s);\n" % (self.name, self.theHandler.name, self.theNumberer.name, self.theModel.name, self.theSolnAlgo.name, self.theSOE.name, self.theIntegrator.name, self.theTest.name)
                AnalysisOption.instances.append(self)

            def theHandler(self):
                return self.theHandler
            def theNumberer(self):
                return self.theNumberer
            def theModel(self):
                return self.theModel
            def theSolnAlgo(self):
                return self.theSolnAlgo
            def theSOE(self):
                return self.theSOE
            def theIntegrator(self):
                return self.theIntegrator
            def theTest(self):
                return self.theTest
            def name(self):
                return self.name
            def command(self):
                return self.command
            def include(self):
                return ['VariableTimeStepDirectIntegrationAnalysis.h']
            def type(self):
                return 'VariableTransientAnalysis'

    class Analyze:
        Counter = 0

        def __init__(self, Analysis, parameters):
            if type(parameters) != list:
                Error("In Analyze, parameter should be a list")
            else:
                self.parameters = parameters
            self.Analysis = Analysis

            if self.Analysis.type() == 'StaticAnalysis':
                if len(self.parameters) != 1:
                    Error("In Analysis, parameters should include 1 number")
                self.command = "%s.analyze(%d);\n" % (self.Analysis.name, self.parameters[0])

            if self.Analysis.type() == 'VariableTransientAnalysis':
                if len(self.parameters) != 5:
                    Error("In Analysis, parameters should include 5 numbers")
                self.command = "%s.analyze(%d, %f, %f, %f, %d);\n" % (self.Analysis.name, self.parameters[0], self.parameters[1], self.parameters[2], self.parameters[3], self.parameters[4])

            AnalysisOption.instances.append(self)

        def command(self):
            return self.command
        def include(self):
            return []
        def type(self):
            return 'Analyze'

    class setCurrentTime:
        def __init__(self, time):
            self.time = time
            self.command = "theDomain->setCurrentTime(%f);\n" % self.time
            AnalysisOption.instances.append(self)

        def command(self):
            return self.command
        def include(self):
            return []
        def type(self):
            return "setCurrentTime"









