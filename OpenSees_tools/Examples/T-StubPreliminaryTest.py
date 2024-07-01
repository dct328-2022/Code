
execfile('__init__.py')


Domain()

Node(1, 0, 0, 0)
Node(2, 1000, 0, 0)
Node(3, 1458.9666779, 0, 0)
Node(4, 2000, 0, 0)
Node(5, 1000, -10, 0)

GeometricTransformation(1, 'Linear', 0, 0, 1)

uniaxialMaterial.Elastic(1, 205000)

Patch1 = RectPatch(1, 10, 10, -150, -150, -145, 150)
Patch2 = RectPatch(1, 10, 10, 145, -150, 150, 150)
Patch3 = RectPatch(1, 10, 10, -145, 145, 145, 150)
Patch4 = RectPatch(1, 10, 10, -145, -150, 145, -145)
Fiber1 = Fiber(1, [Patch1, Patch2, Patch3, Patch4])

Sec1 = Section.Fiber(1, Fiber1, 10)
Int1 = BeamIntegration.Lobatto()

# Columns
#LineElement.ForceBeamColumn(1, 1, 2, 1, 10, Int1, Sec1)
#LineElement.ForceBeamColumn(2, 2, 3, 1, 10, Int1, Sec1)
#LineElement.ForceBeamColumn(3, 3, 5, 1, 10, Int1, Sec1)
#LineElement.ForceBeamColumn(4, 5, 6, 1, 10, Int1, Sec1)

LineElement.ElasticBeamColumn(1, 1, 2, 5900, 205000, 500000, 985599166.67, 85599166.67, 85599166.67, 1)
LineElement.ElasticBeamColumn(2, 2, 3, 5900, 205000, 500000, 985599166.67, 85599166.67, 85599166.67, 1)
LineElement.ElasticBeamColumn(3, 3, 4, 5900, 205000, 500000, 985599166.67, 85599166.67, 85599166.67, 1)
LineElement.ElasticBeamColumn(4, 2, 5, 113.097336, 205000, 500000, 985599166.67, 1017.87602, 1017.87602, 1)

SPConstraint(1, 0, 0, 1, 1, 1, 1)
SPConstraint(5, 1, 1, 1, 1, 1, 1)
SPConstraint(4, 0, 1, 1, 1, 1, 1)
SPConstraint(3, 0, 1, 1, 1, 1, 1)

SPConstraint(2, 0, 0, 1, 1, 1, 0)

#TimeSeries.Linear(1, 1.0)
ConstantSeries = TimeSeries.Constant(1, 10.0)
ConstantSeries2 = TimeSeries.Constant(4, 0.01)
EmptySeries1 = TimeSeries.Empty(2)
EmptySeries2 = TimeSeries.Empty(3)
Recorder.NodeRecorder([0], range(1, 6), "disp", "nodesD1.out")
Recorder.NodeRecorder([1], range(1, 6), "disp", "nodesD2.out")
Recorder.NodeRecorder([5], range(1, 6), "disp", "nodesD3.out")
Recorder.NodeRecorder([0, 1, 5], [3], "reaction", "Node3Reaction.out")
Recorder.ElementRecorder(range(1, 6), "globalForce", "Elements.out")

MultipleSupportPattern = LoadPattern.MultipleSupport(1)
LoadPattern.addLoadPattern([1])
TheGM = GroundMotion(ConstantSeries, EmptySeries1, EmptySeries2, 1.0)
ImposedMotion(1, 1, MultipleSupportPattern, TheGM)

MultipleSupportPattern2 = LoadPattern.MultipleSupport(2)
LoadPattern.addLoadPattern([2])
TheGM2 = GroundMotion(ConstantSeries2, EmptySeries1, EmptySeries2, 1.0)
ImposedMotion(1, 0, MultipleSupportPattern2, TheGM2)

theModel = AnalysisOption.AnalysisModel()
#theIntegrator = AnalysisOption.Integrator.LoadControl(0.01, 100, 0.0001, 0.01)
theIntegrator = AnalysisOption.Integrator.Newmark(0.5, 0.25)
ConsHand = AnalysisOption.ConstraintHandler.Transformation()
theNumberer = AnalysisOption.Numberer().RCM()
theSolver = AnalysisOption.Solver.SparseSPD()
theTest = AnalysisOption.Test.EnergyIncrement(1e-8, 200)
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [0.001, 100, 0.1, 10])
#theAlgo = AnalysisOption.Algorithm.NewtonLineSearch(theTest, "Secant", [])
theAlgo = AnalysisOption.Algorithm.KrylovNewton(theTest)
#theAlgo = AnalysisOption.Algorithm.BFGS(theTest)
#theAnalysis = AnalysisOption.Analysis.StaticAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
theAnalysis = AnalysisOption.Analysis.VariableTransientAnalysis(ConsHand, theNumberer, theModel, theAlgo, theSolver, theIntegrator, theTest)
#AnalysisOption.Analyze(theAnalysis, [100])
AnalysisOption.Analyze(theAnalysis, [1, 1, 1, 1, 100])

'''
double h2;
   double r2;
   double M2;
   double V2;
   double newpos;
   VariableTransientAnalysis1.analyze(1, 1.000000, 1.000000, 1.000000, 100);
   h2=(node1->getDisp())(1);
   r2=(node1->getDisp())(5);
   M2=(ElasticBeamColumn4->getResistingForce())(5);
   V2=(ElasticBeamColumn4->getResistingForce())(1);
   opserr << "h2 " << h2 << "\n";
   opserr << "r2 " << r2 << "\n";
   opserr << "M2 " << M2 << "\n";
   opserr << "V2 " << V2 << "\n";
   newpos = -(2 * 205000 * 85599166.67 * 1000 * r2 + M2 * 1000 * 1000 + 6 * 205000 * 85599166.67 * h2) / (-V2 * 1000 * 1000 + 2 * 205000 * 85599166.67 * r2 - 2 * M2 * 1000);
   opserr << "newpos = " << newpos << "\n";

   node3->setCrds(1000+newpos, 0.000000, 0.000000);
   VariableTransientAnalysis1.analyze(1, 1.000000, 1.000000, 1.000000, 100);'''

WriteCpp('/home/chenting/Chenting/TestExp/OpenSees/EXAMPLES/FindContactPoint/main.cpp').WriteCommands()