
execfile('__init__.py')


Domain()

Node(1, 0, 0, 0)
Node(2, 6, 0, 0)
Node(3, 12, 0, 0)
Node(4, 18, 0, 0)

Node(5, 0, 0, 3.6)
Node(6, 6, 0, 3.6)
Node(7, 12, 0, 3.6)
Node(8, 18, 0, 3.6)

Node(9, 0, 0, 7.2)
Node(10, 6, 0, 7.2)
Node(11, 12, 0, 7.2)
Node(12, 18, 0, 7.2)

Node(13, 0, 5, 0)
Node(14, 6, 5, 0)
Node(15, 12, 5, 0)
Node(16, 18, 5, 0)

Node(17, 0, 5, 3.6)
Node(18, 6, 5, 3.6)
Node(19, 12, 5, 3.6)
Node(20, 18, 5, 3.6)

Node(21, 0, 5, 7.2)
Node(22, 6, 5, 7.2)
Node(23, 12, 5, 7.2)
Node(24, 18, 5, 7.2)

Node(25, 0, 10, 0)
Node(26, 6, 10, 0)
Node(27, 12, 10, 0)
Node(28, 18, 10, 0)

Node(29, 0, 10, 3.6)
Node(30, 6, 10, 3.6)
Node(31, 12, 10, 3.6)
Node(32, 18, 10, 3.6)

Node(33, 0, 10, 7.2)
Node(34, 6, 10, 7.2)
Node(35, 12, 10, 7.2)
Node(36, 18, 10, 7.2)

GeometricTransformation(1, 'Corotational', 1, 0, 0)
GeometricTransformation(2, 'Corotational', 0, 1, 0)
GeometricTransformation(3, 'Corotational', 0, 0, 1)

uniaxialMaterial.Steel02(1, 345, 205000, 0.01)

uniaxialMaterial.Elastic(101, 205000)
uniaxialMaterial.Elastic(102, 206000)
uniaxialMaterial.ElasticPP(103, 205000, 0.001)
uniaxialMaterial.ElasticPP(104, 205000, 0.001, -0.0005)
uniaxialMaterial.ElasticPP(105, 205000, 0.001, eps0=0.001)
uniaxialMaterial.Steel01(106, 345, 205000, 0.01)

NDMaterial.ElasticIsotropic(107, 205000, 0.2)
NDMaterial.DruckerPrager(108, 185000, 90000, 345, 0, 0, 1, 1, 0.1, 0.1, 1850, 0.1, 0)
NDMaterial.DruckerPrager(109, 185000, 90000, 390, 0, 0, 1, 1, 0.1, 0.1, 1850, 0.2, 0)

NDMaterial.PlateFiberMaterial(1007, 107)
NDMaterial.PlateFiberMaterial(1008, 108)
NDMaterial.PlateFiberMaterial(1009, 109)

#LineElement.ElasticBeamColumn(1, 1, 2, 0.1, 205000, 109000, 0.02, 0.01, 0.01, 1)
#LineElement.ElasticBeamColumn(2, 2, 3, 0.1, 205000, 109000, 0.02, 0.01, 0.01, 2)

Patch1 = RectPatch(1, 10, 10, -150, -150, -140, 150)
Patch2 = RectPatch(1, 10, 10, -140, 140, 140, 150)
Patch3 = RectPatch(1, 10, 10, 140, -150, 150, 150)
Patch4 = RectPatch(1, 10, 10, -140, -150, 140, -140)
Fiber1 = Fiber(1, [Patch1, Patch2, Patch3, Patch4])

Sec1 = Section.Fiber(1, Fiber1, 10)

Patch5 = RectPatch(1, 10, 10, -100, 140, 100, 150)
Patch6 = RectPatch(1, 10, 10, -4, -140, 4, 140)
Patch7 = RectPatch(1, 10, 10, -100, -150, 100, -140)
Fiber2 = Fiber(2, [Patch5, Patch6, Patch7])

Sec2 = Section.Fiber(2, Fiber2, 7)

#For Beam with variable cross section:
#Section.Fiber(2, [Fiber1, Fiber1, Fiber1, Fiber2, Fiber2, Fiber2, Fiber2], 7)

#Section.Elastic(3, 205000, 0.1, 0.01, 0.01, 105001, 0.02, 7)
#Section.SectionAggregator(4, [1, 4, 6], ['P', 'T', 'My'], 2, 7, [0, 1, 5, 6])
#Se1 = Section.Fiber(5, Fiber1, 7)

Int1 = BeamIntegration.Lobatto()
Int2 = BeamIntegration.FixedLocation(7)
Int3 = BeamIntegration.FixedLocation(7, [0, 0.1, 0.2, 0.3, 0.7, 0.8, 1])
Int4 = BeamIntegration.Legendre()

# Columns
LineElement.ForceBeamColumn(1, 1, 5, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(2, 5, 9, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(3, 2, 6, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(4, 6, 10, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(5, 3, 7, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(6, 7, 11, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(7, 4, 8, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(8, 8, 12, 2, 10, Int1, Sec1)

LineElement.ForceBeamColumn(9, 13, 17, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(10, 17, 21, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(11, 14, 18, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(12, 18, 22, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(13, 15, 19, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(14, 19, 23, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(15, 16, 20, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(16, 20, 24, 2, 10, Int1, Sec1)

LineElement.ForceBeamColumn(17, 25, 29, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(18, 29, 33, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(19, 26, 30, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(20, 30, 34, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(21, 27, 31, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(22, 31, 35, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(23, 28, 32, 2, 10, Int1, Sec1)
LineElement.ForceBeamColumn(24, 32, 36, 2, 10, Int1, Sec1)

AvailableNode = 37
AvailableElement = 25

# Beams in XZ Plane
LineElement.DispBeamColumnMeshed(AvailableElement, 5, 6, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 6, 7, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 7, 8, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 9, 10, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 10, 11, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 11, 12, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10

LineElement.DispBeamColumnMeshed(AvailableElement, 17, 18, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 18, 19, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 19, 20, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 21, 22, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 22, 23, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 23, 24, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10

LineElement.DispBeamColumnMeshed(AvailableElement, 29, 30, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 30, 31, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 31, 32, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 33, 34, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 34, 35, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 35, 36, 2, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10

# Beams in YZ Plane
LineElement.DispBeamColumnMeshed(AvailableElement, 5, 17, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 17, 29, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 6, 18, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 18, 30, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 7, 19, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 19, 31, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 8, 20, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 20, 32, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10

LineElement.DispBeamColumnMeshed(AvailableElement, 9, 21, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 21, 33, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 10, 22, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 22, 34, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 11, 23, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 23, 35, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 12, 24, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10
LineElement.DispBeamColumnMeshed(AvailableElement, 24, 36, 1, 7, Int4, Sec2, 10, True, AvailableNode)
AvailableNode += 9
AvailableElement += 10

SPConstraint(1, 1, 1, 1, 1, 1, 1)
SPConstraint(2, 1, 1, 1, 1, 1, 1)
SPConstraint(3, 1, 1, 1, 1, 1, 1)
SPConstraint(4, 1, 1, 1, 1, 1, 1)
SPConstraint(13, 1, 1, 1, 1, 1, 1)
SPConstraint(14, 1, 1, 1, 1, 1, 1)
SPConstraint(15, 1, 1, 1, 1, 1, 1)
SPConstraint(16, 1, 1, 1, 1, 1, 1)
SPConstraint(25, 1, 1, 1, 1, 1, 1)
SPConstraint(26, 1, 1, 1, 1, 1, 1)
SPConstraint(27, 1, 1, 1, 1, 1, 1)
SPConstraint(28, 1, 1, 1, 1, 1, 1)

#MPConstraint.equalDOF(1, 2, [1, 4, 5])
#MPConstraint.equalDOF(2, 3, [1, 4, 5])

TimeSeries.Linear(1, 1.0)
Recorder.NodeRecorder([0, 1, 2, 3, 4, 5], range(1, 37), "disp", "AllNodes.out")
Recorder.ElementRecorder(range(1, 11), "globalForce", "Elements.out")

LoadPattern.LoadPattern(1, 1)

# =================================================   Apply Gravity Load for the first floor =========================
ConcentratedLoadTag = 1
CNodeList1 = filter(lambda x: x.z == 3.6, Node.instances)
CNodeList1 = map(lambda x: x.n, CNodeList1)
print('CNodeList1', len(CNodeList1))

for obj in CNodeList1:
    Load.ConcentratedForce(ConcentratedLoadTag, obj, [0, 0, -1000, 0, 0, 0])
    ConcentratedLoadTag += 1
ConcentratedLoadTag1 = ConcentratedLoadTag

# =================================================   Apply Gravity Load for the second floor =========================
CNodeList2 = filter(lambda x: x.z == 7.2, Node.instances)
CNodeList2 = map(lambda x: x.n, CNodeList2)
print('CNodeList2', len(CNodeList2))

for obj in CNodeList2:
    Load.ConcentratedForce(ConcentratedLoadTag, obj, [0, 0, -600, 0, 0, 0])
    ConcentratedLoadTag += 1
ConcentratedLoadTag2 = ConcentratedLoadTag

AnalysisOption.addLoadPattern([1])
AnalysisOption.addLoad(range(1, ConcentratedLoadTag2), 1)

theModel = AnalysisOption.AnalysisModel()
theIntegrator = AnalysisOption.Integrator.LoadControl(0.1, 10, 0.1, 0.1)
ConsHand = AnalysisOption.ConstraintHandler.Transformation()
theNumberer = AnalysisOption.Numberer().RCM()
theSolver = AnalysisOption.Solver.SparseSPD()
theTest = AnalysisOption.Test.EnergyIncrement(1e-8, 200)
theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "InitialInterpolated", [])
theAnalysis = AnalysisOption.Analysis.StaticAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
AnalysisOption.Analyze(theAnalysis, [10])

WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/TestPyOpenSees/main.cpp').WriteCommands()