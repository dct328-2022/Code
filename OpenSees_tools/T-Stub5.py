
execfile('__init__.py')


Domain()

Node(11, 0, 95, 0)
Node(12, 0, 6.5, 0)
Node(13, -47.5, 6.5, 0)
Node(14, -63.5, 6.5, 0)
Node(15, -1080, 6.5, 0)
Node(16, 47.5, 6.5, 0)
Node(17, 63.5, 6.5, 0)
Node(18, 1080, 6.5, 0)

Node(21, 0, -95, 0)
Node(22, 0, -6.5, 0)
Node(23, -47.5, -6.5, 0)
Node(24, -63.5, -6.5, 0)
Node(25, -1080, -6.5, 0)
Node(26, 47.5, -6.5, 0)
Node(27, 63.5, -6.5, 0)
Node(28, 1080, -6.5, 0)

GeometricTransformation(1, 'Linear', 0, 0, 1)

#uniaxialMaterial.Elastic(1, 204105)
#uniaxialMaterial.Elastic(2, 212866)
uniaxialMaterial.Steel02(1, 275, 205000, 0.01)
RigidMat = uniaxialMaterial.Elastic(3, 2050000000)
uniaxialMaterial.Elastic(4, 205000)

# Method for Computing k: 3*b*(15*a**4 - 10*a**2*b**2 + 3*b**4)/(20*a**5)
# Shear Area is A/k
uniaxialMaterial.Elastic(5, 205000/(2*(1+0.3))*5/6*13*190)
uniaxialMaterial.Elastic(6, 205000/(2*(1+0.3))*9/10*3.1415926*10*10)

uniaxialMaterial.Steel02(7, 1090, 205000, 0.01, sigInit=0.436)
ZeroMaterial = uniaxialMaterial.ENT(8, 205000000)

# Flange Section
Patch1 = RectPatch(1, 10, 10, -6.5, -43.5, 6.5, 43.5)
Fiber1 = Fiber(1, [Patch1])
Sec1 = Section.Fiber(1, Fiber1, 10)
Sec11 = Section.SectionAggregator(11, [5], ['Vy'], PSectionTag=1)
Int1 = BeamIntegration.Lobatto()

# Web Section
Patch2 = RectPatch(1, 10, 10, -4, -43.5, 4, 43.5)
Fiber2 = Fiber(2, [Patch2])
Sec2 = Section.Fiber(2, Fiber2, 10)
Int2 = BeamIntegration.Lobatto()

# Circular Section
Patch3 = CircularPatch(7, 10, 60, 0, 0, 10)
Fiber3 = Fiber(3, [Patch3])
Sec3 = Section.Fiber(3, Fiber3, 10)
Sec13 = Section.SectionAggregator(13, [5], ['Vy'], PSectionTag=3)
Int3 = BeamIntegration.Lobatto()

# Elements
LineElement.ForceBeamColumn(1, 11, 12, 1, 10, Int2, Sec2)
LineElement.ForceBeamColumn(2, 12, 13, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(3, 13, 14, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(4, 14, 15, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(5, 12, 16, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(6, 16, 17, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(7, 17, 18, 1, 10, Int1, Sec11)

LineElement.ForceBeamColumn(8, 21, 22, 1, 10, Int2, Sec2)
LineElement.ForceBeamColumn(9, 22, 23, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(10, 23, 24, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(11, 24, 25, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(12, 22, 26, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(13, 26, 27, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(14, 27, 28, 1, 10, Int1, Sec11)

#LineElement.ElasticTimoshenkoBeamColumn(15, 13, 23, 205000, 78846.154, 28.2743, 127.2345, 63.61725, 63.61725, 25.44687, 25.44687, 1)
#LineElement.ElasticTimoshenkoBeamColumn(16, 16, 26, 205000, 78846.154, 28.2743, 127.2345, 63.61725, 63.61725, 25.44687, 25.44687, 1)

LineElement.ForceBeamColumn(15, 13, 23, 1, 10, Int3, Sec13)
LineElement.ForceBeamColumn(16, 16, 26, 1, 10, Int3, Sec13)

#MaterialList1 = LineElement.MaterialList([RigidMat, RigidMat, RigidMat, RigidMat])
#FSB1y = Vector('FSB1y', 3, [1, 0, 0])
#FSB1x = Vector('FSB1x', 3, [0, 1, 0])
#LineElement.flatSliderBearing(15, 13, 23, 1, 100000000, MaterialList1, FSB1y, FSB1x, 0.5)
#LineElement.flatSliderBearing(16, 16, 26, 1, 100000000, MaterialList1, FSB1y, FSB1x, 0.5)

LineElement.ElasticBeamColumn(17, 14, 24, 999999, 20500000, 999999, 999999, 999999, 999999, 1)
LineElement.ElasticBeamColumn(18, 17, 27, 999999, 20500000, 999999, 999999, 999999, 999999, 1)
LineElement.ElasticBeamColumn(19, 15, 25, 999999, 20500000, 999999, 999999, 999999, 999999, 1)
LineElement.ElasticBeamColumn(20, 18, 28, 999999, 20500000, 999999, 999999, 999999, 999999, 1)

ABolt = 3.1415926*10*10
LineElement.Truss(21, 13, 23, ABolt, ZeroMaterial)
LineElement.Truss(22, 16, 26, ABolt, ZeroMaterial)

SPConstraint(21, 1, 1, 1, 1, 1, 1)

SPConstraint(11, 0, 0, 1, 1, 1, 0)
SPConstraint(12, 0, 0, 1, 1, 1, 0)
SPConstraint(13, 0, 0, 1, 1, 1, 0)
SPConstraint(14, 0, 0, 1, 1, 1, 0)
SPConstraint(15, 0, 0, 1, 1, 1, 0)
SPConstraint(16, 0, 0, 1, 1, 1, 0)
SPConstraint(17, 0, 0, 1, 1, 1, 0)
SPConstraint(18, 0, 0, 1, 1, 1, 0)
SPConstraint(22, 0, 0, 1, 1, 1, 0)
SPConstraint(23, 0, 0, 1, 1, 1, 0)
SPConstraint(24, 0, 0, 1, 1, 1, 0)
SPConstraint(25, 0, 0, 1, 1, 1, 0)
SPConstraint(26, 0, 0, 1, 1, 1, 0)
SPConstraint(27, 0, 0, 1, 1, 1, 0)
SPConstraint(28, 0, 0, 1, 1, 1, 0)

#TimeSeries.Linear(1, 1.0)
#ConstantSeries = TimeSeries.Constant(1, 0.1)
PathTimeSeries = TimeSeries.Path(1, '/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/T-Stub/TS1.txt', 1, 1.0)
EmptySeries1 = TimeSeries.Empty(2)
EmptySeries2 = TimeSeries.Empty(3)
Recorder.NodeRecorder([0], range(11, 19), "disp", "nodesD1.out")
Recorder.NodeRecorder([1], range(11, 19), "disp", "nodesD2.out")
Recorder.NodeRecorder([5], range(11, 19), "disp", "nodesD3.out")
Recorder.NodeRecorder([1], [11], "reaction", "nodesR2.out")
Recorder.NodeRecorder([5], [13, 23, 16, 26], "disp", "nodesD6.out")
Recorder.NodeRecorder([1], [12, 22], "disp", "nodes12&22D2.out")
Recorder.ElementRecorder(range(2, 8), "globalForce", "FlangeElements.out")
Recorder.ElementRecorder([2, 9], "globalForce", "FlangeElementsContrast.out")
Recorder.ElementRecorder([1], "globalForce", "WebElements.out")
Recorder.ElementRecorder([15, 16], "globalForce", "BoltElements.out")
Recorder.ElementRecorder([21, 22], "axialForce", "PretensionElements.out")
Recorder.ElementRecorder([17, 18], "globalForce", "ReactionElements.out")

MultipleSupportPattern = LoadPattern.MultipleSupport(1)
LoadPattern.addLoadPattern([1])
TheGM = GroundMotion(PathTimeSeries, EmptySeries1, EmptySeries2, 1.0)
ImposedMotion(11, 1, MultipleSupportPattern, TheGM)

theModel = AnalysisOption.AnalysisModel()
#theIntegrator = AnalysisOption.Integrator.LoadControl(0.01, 100, 0.0001, 0.01)
theIntegrator = AnalysisOption.Integrator.Newmark(0.5, 0.25)
ConsHand = AnalysisOption.ConstraintHandler.Transformation()
theNumberer = AnalysisOption.Numberer().RCM()
theSolver = AnalysisOption.Solver.SparseSPD()
theTest = AnalysisOption.Test.EnergyIncrement(1e-8, 600)
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [0.001, 100, 0.1, 10])
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [])
theAlgo = AnalysisOption.Algorithm.KrylovNewton(theTest)
#theAlgo = AnalysisOption.Algorithm.BFGS(theTest)
#theAnalysis = AnalysisOption.Analysis.StaticAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
theAnalysis = AnalysisOption.Analysis.VariableTransientAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
#AnalysisOption.Analyze(theAnalysis, [100])
AnalysisOption.Analyze(theAnalysis, [1, 1, 1, 1, 100])

'''
double M1;
    double r1;
    double M2;
    double r2;
    double h2;
    double h1;
    double V1;
    double V2;
    double newpos1;
    double newpos2;
    double res1;
    double res2;
    double k2;
    double k1;

for (i=1;i<121;i++) {
        h2 = (node12->getDisp())(1) - (node17->getDisp())(1);
        opserr << "h2 " << h2 << "\n";
        r2 = (node12->getDisp())(5) - (node17->getDisp())(5);
        opserr << "r2 " << r2 << "\n";
        M2 = (ForceBeamColumn16->getResistingForce())(5);
        opserr << "M2 " << M2 << "\n";
        V2 = (ForceBeamColumn16->getResistingForce())(1);
        opserr << "V2 " << V2 << "\n";
        res2 = (ElasticBeamColumn2->getResistingForce())(11);
        opserr << "res2 " << res2 << "\n";
        if (i == 1) {
            newpos2 = 16;
        }
        k2 = -(V2 * 47.5 * 47.5 * 47.5 - V2 * 47.5 * 47.5 * newpos2 + 2 * 205000 * 34785.8333 * 47.5 * r2 + 2 * 205000 * 34785.8333 * newpos2 * r2 - 4 * M2 * 47.5 * 47.5 + 2 * M2 * 47.5 * newpos2 + 12 * 205000 * 34785.8333 * h2) / (47.5 + newpos2) / (47.5 + newpos2) / (47.5 + newpos2);

        if (-res2/k2 + newpos2 > 0) {
            newpos2 = -res2/k2 + newpos2;
        }

        opserr << "newpos2 = " << newpos2 << "\n";
        node17->setCrds(47.5 + newpos2, 6.5, 0.000000);
        node27->setCrds(47.5 + newpos2, -6.5, 0.000000);

        h1 = (node12->getDisp())(1) - (node17->getDisp())(1);
        opserr << "h1 " << h1 << "\n";
        r1 = (node12->getDisp())(5) - (node17->getDisp())(5);
        opserr << "r1 " << r1 << "\n";
        M1 = -(ForceBeamColumn15->getResistingForce())(5);
        opserr << "M1 " << M1 << "\n";
        V1 = (ForceBeamColumn15->getResistingForce())(1);
        opserr << "V1 " << V1 << "\n";
        res1 = (ElasticBeamColumn1->getResistingForce())(11);
        opserr << "res1 " << res1 << "\n";
        if (i == 1) {
            newpos1 = 16;
        }
        k1 = -(V1 * 47.5 * 47.5 * 47.5 - V1 * 47.5 * 47.5 * newpos1 + 2 * 205000 * 34785.8333 * 47.5 * r1 + 2 * 205000 * 34785.8333 * newpos1 * r1 - 4 * M1 * 47.5 * 47.5 + 2 * M1 * 47.5 * newpos1 + 12 * 205000 * 34785.8333 * h1) / (47.5 + newpos1) / (47.5 + newpos1) / (47.5 + newpos1);

        if (res1/k1 + newpos1 > 0) {
        newpos1 = res1/k1 + newpos1;
        }
        opserr << "newpos1 = " << newpos1 << "\n";
        node14->setCrds(-47.5 - newpos1, 6.5, 0.000000);
        node24->setCrds(-47.5 - newpos1, -6.5, 0.000000);
        VariableTransientAnalysis1.analyze(1, 1.000000, 1.000000, 1.000000, 100);
}
'''


WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/T-Stub/T-Stub5/main.cpp').WriteCommands()
