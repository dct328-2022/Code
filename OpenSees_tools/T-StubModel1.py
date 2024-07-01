
execfile('__init__.py')


Domain()

Node(11, 0, 176.8, 0)
Node(12, 0, 5.35, 0)
Node(13, -33.7, 5.35, 0)
Node(14, -48.7, 5.35, 0)
Node(16, 33.7, 5.35, 0)
Node(17, 48.7, 5.35, 0)

Node(21, 0, -176.8, 0)
Node(22, 0, -5.35, 0)
Node(23, -33.7, -5.35, 0)
Node(24, -48.7, -5.35, 0)
Node(26, 33.7, -5.35, 0)
Node(27, 48.7, -5.35, 0)

GeometricTransformation(1, 'Linear', 0, 0, 1)

#uniaxialMaterial.Elastic(1, 204105)
#uniaxialMaterial.Elastic(2, 212866)
uniaxialMaterial.Steel01(1, 373.97, 204105, 0.01)
uniaxialMaterial.Steel01(2, 378.43, 212866, 0.01)
uniaxialMaterial.Elastic(3, 2050000000)
uniaxialMaterial.Elastic(4, 205000)

uniaxialMaterial.Elastic(5, 205000/(2*(1+0.3))*5/6*10.7*15)
uniaxialMaterial.Elastic(6, 205000/(2*(1+0.3))*9/10*3.1415926*3*3)

uniaxialMaterial.Steel01(7, 824.5, 205000, 0.01)
RigidENT = uniaxialMaterial.ENT(8, 2050000000)

# Flange Section
Patch1 = RectPatch(1, 10, 10, -5.35, -7.5, 5.35, 7.5)
Fiber1 = Fiber(1, [Patch1])
Sec1 = Section.Fiber(1, Fiber1, 10)
Sec11 = Section.SectionAggregator(11, [5], ['Vy'], PSectionTag=1)
Int1 = BeamIntegration.Lobatto()

# Web Section
Patch2 = RectPatch(2, 10, 10, -3.25, -7.5, 3.25, 7.5)
Fiber2 = Fiber(2, [Patch2])
Sec2 = Section.Fiber(2, Fiber2, 10)
Int2 = BeamIntegration.Lobatto()

# Circular Section
Patch3 = CircularPatch(7, 10, 60, 0, 0, 3)
Fiber3 = Fiber(3, [Patch3])
Sec3 = Section.Fiber(3, Fiber3, 10)
Sec13 = Section.SectionAggregator(13, [6], ['Vy'], PSectionTag=3)
Int3 = BeamIntegration.Lobatto()

# Elements
LineElement.ForceBeamColumn(1, 11, 12, 1, 10, Int2, Sec2)
LineElement.ForceBeamColumn(2, 12, 13, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(3, 13, 14, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(5, 12, 16, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(6, 16, 17, 1, 10, Int1, Sec11)

LineElement.ForceBeamColumn(8, 21, 22, 1, 10, Int2, Sec2)
LineElement.ForceBeamColumn(9, 22, 23, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(10, 23, 24, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(12, 22, 26, 1, 10, Int1, Sec11)
LineElement.ForceBeamColumn(13, 26, 27, 1, 10, Int1, Sec11)

#LineElement.ElasticTimoshenkoBeamColumn(15, 13, 23, 205000, 78846.154, 28.2743, 127.2345, 63.61725, 63.61725, 25.44687, 25.44687, 1)
#LineElement.ElasticTimoshenkoBeamColumn(16, 16, 26, 205000, 78846.154, 28.2743, 127.2345, 63.61725, 63.61725, 25.44687, 25.44687, 1)

LineElement.ForceBeamColumn(15, 13, 23, 1, 10, Int3, Sec13)
LineElement.ForceBeamColumn(16, 16, 26, 1, 10, Int3, Sec13)

#LineElement.ElasticBeamColumn(17, 14, 24, 999999, 20500000, 999999, 999999, 999999, 999999, 1)
#LineElement.ElasticBeamColumn(18, 17, 27, 999999, 20500000, 999999, 999999, 999999, 999999, 1)

LineElement.Truss(17, 14, 24, 999999, RigidENT)
LineElement.Truss(18, 17, 27, 999999, RigidENT)

SPConstraint(21, 1, 1, 1, 1, 1, 1)

SPConstraint(11, 0, 0, 1, 1, 1, 0)
SPConstraint(12, 0, 0, 1, 1, 1, 0)
SPConstraint(13, 0, 0, 1, 1, 1, 0)
SPConstraint(14, 0, 0, 1, 1, 1, 0)
SPConstraint(16, 0, 0, 1, 1, 1, 0)
SPConstraint(17, 0, 0, 1, 1, 1, 0)
SPConstraint(22, 0, 0, 1, 1, 1, 0)
SPConstraint(23, 0, 0, 1, 1, 1, 0)
SPConstraint(24, 0, 0, 1, 1, 1, 0)
SPConstraint(26, 0, 0, 1, 1, 1, 0)
SPConstraint(27, 0, 0, 1, 1, 1, 0)

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
theTest = AnalysisOption.Test.EnergyIncrement(1e-10, 200)
theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [0.001, 100, 0.1, 10])
theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [])
#theAlgo = AnalysisOption.Algorithm.KrylovNewton(theTest)
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

    VariableTransientAnalysis1.analyze(1, 1.000000, 1.000000, 1.000000, 100);
    i = 1;

    do {
        h2 = (node12->getDisp())(1) - (node17->getDisp())(1);
        opserr << "h2 " << h2 << "\n";
        r2 = (node12->getDisp())(5) - (node17->getDisp())(5);
        opserr << "r2 " << r2 << "\n";
        M2 = (ForceBeamColumn12->getResistingForce())(5);
        opserr << "M2 " << M2 << "\n";
        V2 = (ForceBeamColumn12->getResistingForce())(1);
        opserr << "V2 " << V2 << "\n";
        res2 = - (node17->getDisp())(5) + (node27->getDisp())(5);
        opserr << "res2 " << res2*100000 << "\n";
        if (i == 1) {
            newpos2 = 15;
        }
        k2 = -(V2 * 33.7 * 33.7 * 33.7 + 3 * M2 * 33.7 * 33.7 + 6 * 204105 * 1531.30375 * h2) / (204105 * 1531.30375 * (33.7 + newpos2) * (33.7 + newpos2));
        if (-res2/k2 + newpos2 > 0) {
            newpos2 = -res2/k2 + newpos2;
        }

        if (-res2/k2 + newpos2 > 30.1 && i > 10) {
            newpos2 = 30.1;
        }

        opserr << "newpos2 = " << newpos2 << "\n";
        node17->setCrds(33.7 + newpos2, 5.350000, 0.000000);
        node27->setCrds(33.7 + newpos2, -5.350000, 0.000000);

        h1 = (node12->getDisp())(1) - (node14->getDisp())(1);
        opserr << "h1 " << h1 << "\n";
        r1 = - (node12->getDisp())(5) + (node14->getDisp())(5);
        opserr << "r1 " << r1 << "\n";
        M1 = -(ForceBeamColumn11->getResistingForce())(5);
        opserr << "M1 " << M1 << "\n";
        V1 = (ForceBeamColumn11->getResistingForce())(1);
        opserr << "V1 " << V1 << "\n";
        res1 = (node14->getDisp())(5) - (node24->getDisp())(5);
        opserr << "res1 " << res1*100000 << "\n";
        if (i == 1) {
            newpos1 = 15;
        }
        k1 = -(V1 * 33.7 * 33.7 * 33.7 + 3 * M1 * 33.7 * 33.7 + 6 * 204105 * 1531.30375 * h1) / (204105 * 1531.30375 * (33.7 + newpos1) * (33.7 + newpos1));

        if (-res1/k1 + newpos1 > 0) {
        newpos1 = -res1/k1 + newpos1;
        }

        if (-res1/k1 + newpos1 > 30.1 && i > 10) {
        newpos1 = 30.1;
        }

        opserr << "newpos1 = " << newpos1 << "\n";
        node14->setCrds(-33.7 - newpos1, 5.350000, 0.000000);
        node24->setCrds(-33.7 - newpos1, -5.350000, 0.000000);
        VariableTransientAnalysis1.analyze(1, 1.000000, 1.000000, 1.000000, 100);
        i++;
    } while(i <= 200);
    opserr << "Iterations: " << i << "\n";
'''

WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/T-Stub/Model1/main.cpp').WriteCommands()
