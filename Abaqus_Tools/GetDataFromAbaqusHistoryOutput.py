fnread = "C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConductionStage3-6/NodePairs3-6.txt"
fnr = open(fnread, 'r')
NodeSet = []

for line in fnr:
    split = line.split()
    if len(split) == 2:
        NodeSet.append(int(split[0]))

for obj in NodeSet:
    f =  session.openOdb(name='C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConductionStage3-6/HeatTransfer2D-SGP%d.odb'%obj)
    Hi = f.steps['HeatTransfer'].historyRegions['Node PART-1-1.1'].historyOutputs['NT11'].data
    fn = open("C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConductionStage3-6/ff%d.txt"%obj, 'w')
    for obj in Hi:
        fn.write("%f %f"%(obj[0], obj[1]))
        fn.write('\n')

