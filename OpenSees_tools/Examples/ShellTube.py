
execfile('__init__.py')


Domain()

Node(1, 0, 150, 150)
Node(2, 0, -150, 150)
Node(3, 0, -150, -150)
Node(4, 0, 150, -150)

Node(5, 5000, 150, 150)
Node(6, 5000, -150, 150)
Node(7, 5000, -150, -150)
Node(8, 5000, 150, -150)

Node(9, 0, 0, 0)
Node(10, 5000, 0, 0)

GeometricTransformation(1, 'Linear', 1, 0, 0)

uniaxialMaterial.Steel02(1, 345, 205000, 0.01)

uniaxialMaterial.Elastic(101, 2050000000)

NDMaterial.ElasticIsotropic(107, 205000, 0.3)
NDMaterial.DruckerPrager(108, 170833.3333, 78846.15385, 345, 0, 0, 1, 1, 0.1, 0.1, 1708.3333, 0.1, 0)

NDMaterial.PlateFiberMaterial(1007, 107)
NDMaterial.PlateFiberMaterial(1008, 108)
Section.PlateFiber(10007, 1007, 10)
Section.PlateFiber(10008, 1008, 10)

Patch1 = RectPatch(101, 10, 10, -500, -500, 500, 500)

Fiber1 = Fiber(1, [Patch1])

Sec1 = Section.Fiber(1, Fiber1, 5)

Int1 = BeamIntegration.Lobatto()

ShellElement.ShellMITC9Meshed(5, 8, 4, 1, 6, 100, 10001, 10001, 10007)
ShellElement.ShellMITC9Meshed(6, 7, 3, 2, 6, 100, 20001, 20001, 10007)
ShellElement.ShellMITC9Meshed(5, 1, 2, 6, 100, 6, 30001, 30001, 10007)
ShellElement.ShellMITC9Meshed(8, 4, 3, 7, 100, 6, 40001, 40001, 10007)

StartNodeSet = filter(lambda x: x.x == 0 and x.n != 9, Node.instances)
EndNodeSet = filter(lambda x: x.x == 5000 and x.n != 10, Node.instances)

for i, obj in enumerate(StartNodeSet):
    LineElement.ForceBeamColumn(50000 + i, obj.n, 9, 1, 5, Int1, Sec1)

for i, obj in enumerate(EndNodeSet):
    LineElement.ForceBeamColumn(60000 + i, obj.n, 10, 1, 5, Int1, Sec1)

SPConstraint(9, 1, 1, 1, 1, 1, 1)

TimeSeries.Linear(1, 1.0)
Recorder.NodeRecorder([0, 1, 2, 3, 4, 5], [10], "disp", "Node10.out")

LoadPattern.LoadPattern(1, 1)

# =================================================   Apply Gravity Load for the first floor =========================
ConcentratedLoadTag = 1

Load.ConcentratedForce(ConcentratedLoadTag, 10, [0, 0, -100000, 0, 0, 0])

AnalysisOption.addLoadPattern([1])
AnalysisOption.addLoad([1], 1)

theModel = AnalysisOption.AnalysisModel()
theIntegrator = AnalysisOption.Integrator.LoadControl(0.01, 100, 0.001, 0.01)
ConsHand = AnalysisOption.ConstraintHandler.Transformation()
theNumberer = AnalysisOption.Numberer().RCM()
theSolver = AnalysisOption.Solver.SparseSPD()
theTest = AnalysisOption.Test.EnergyIncrement(1e-8, 200)
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "InitialInterpolated", [0.001, 100, 0.1, 10])
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "InitialInterpolated", [])
theAlgo = AnalysisOption.Algorithm.KrylovNewton(theTest)
theAnalysis = AnalysisOption.Analysis.StaticAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
AnalysisOption.Analyze(theAnalysis, [100])

WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/ShellTube/main.cpp').WriteCommands()