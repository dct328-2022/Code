
execfile('__init__.py')


Domain()

Node(1, 0, 0, 0)
Node(2, 90, 0, 0)
Node(3, 90, 100, 0)
Node(4, 0, 100, 0)

Node(5, 0, 50, 0.1)

GeometricTransformation(1, 'Linear', 1, 0, 0)

uniaxialMaterial.Steel02(1, 345, 205000, 0.01)

RigidMat = uniaxialMaterial.Elastic(101, 205000000)
TensileOnlyMat = uniaxialMaterial.ENT(102, 205000000)

NDMaterial.ElasticIsotropic(107, 205000, 0.3)
NDMaterial.DruckerPrager(108, 170833.3333, 78846.15385, 345, 0, 0, 1, 1, 0, 0, 1708.3333, 1.0, 0)

NDMaterial.PlateFiberMaterial(1007, 107)
NDMaterial.PlateFiberMaterial(1008, 108)
Section.PlateFiber(10007, 1007, 10)
Section.PlateFiber(10008, 1008, 10)

Patch1 = RectPatch(101, 10, 10, -500, -500, 500, 500)

Fiber1 = Fiber(1, [Patch1])

Sec1 = Section.Fiber(1, Fiber1, 5)

Int1 = BeamIntegration.Lobatto()

ShellElement.ShellMITC9Meshed(1, 2, 3, 4, 90, 100, 100001, 100001, 10008)

EndNodeSet = filter(lambda x: x.x == 0 and x.z == 0, Node.instances)

for i, obj in enumerate(EndNodeSet):
    LineElement.ForceBeamColumn(200001 + i, obj.n, 10, 1, 5, Int1, Sec1)

Point = filter(lambda x: x.x == 60 and x.z == 0 and x.y == 50, Node.instances)[0]
SPConstraint(Point.n, 1, 1, 1, 1, 1, 1)

PlaneNodes = filter(lambda x: x.z == 0, Node.instances)
CopyNodes(PlaneNodes, [0, 0, -1], 200001)
BaseNodes = filter(lambda x: x.n > 200000, Node.instances)
for obj in BaseNodes:
    SPConstraint(obj.n, 1, 1, 1, 1, 1, 1)

for i, obj in enumerate(PlaneNodes):
    node2 = filter(lambda x: x.x == obj.x and x.y == obj.y and x.z == obj.z, BaseNodes)[0]
    Truss(300001 + i, obj.n, node2.n, 100000, RigidMat)


LinearSeries = TimeSeries.Linear(1, 5.0)
EmptySeries1 = TimeSeries.Empty(2)
EmptySeries2 = TimeSeries.Empty(3)
Recorder.NodeRecorder([0, 1, 2, 3, 4, 5], [5], "disp", "Node5disp.out")
Recorder.NodeRecorder([0, 1, 2, 3, 4, 5], [5], "reaction", "Node5rec.out")
Recorder.ElementRecorder(map(lambda x: x.n, PlaneNodes), "strains", "ElementStrains.out")
Recorder.ElementRecorder(map(lambda x: x.n, PlaneNodes), "stresses", "ElementStresses.out")


# =================================================   Apply Gravity Load for the first floor =========================

MultipleSupportPattern = LoadPattern.MultipleSupport(1)
LoadPattern.addLoadPattern([1])
TheGM = GroundMotion(LinearSeries, EmptySeries1, EmptySeries2, 1.0)
ImposedMotion(5, 2, MultipleSupportPattern, TheGM)

theModel = AnalysisOption.AnalysisModel()
#theIntegrator = AnalysisOption.Integrator.LoadControl(0.01, 100, 0.0001, 0.01)
theIntegrator = AnalysisOption.Integrator.Newmark(0.5, 0.25)
ConsHand = AnalysisOption.ConstraintHandler.Transformation()
theNumberer = AnalysisOption.Numberer().RCM()
theSolver = AnalysisOption.Solver.SparseSPD()
theTest = AnalysisOption.Test.EnergyIncrement(1e-8, 200)
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [0.001, 100, 0.1, 10])
theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [])
#theAlgo = AnalysisOption.Algorithm.KrylovNewton(theTest)
#theAlgo = AnalysisOption.Algorithm.BFGS(theTest)
#theAnalysis = AnalysisOption.Analysis.StaticAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
theAnalysis = AnalysisOption.Analysis.VariableTransientAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
#AnalysisOption.Analyze(theAnalysis, [100])
AnalysisOption.Analyze(theAnalysis, [100, 0.01, 0.0001, 0.02, 100])

WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/T-Stub/main.cpp').WriteCommands()