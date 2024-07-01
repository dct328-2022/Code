execfile("/media/chenting/Work/ProgramCode/Tools/Interpolation.py")

filepath1 = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/SY2InternalStiffenerStressYN.txt"
fileout = "/media/chenting/Work/ProgramCode/AbaqusInpScript2/TplllYNY2.txt"

f1 = open(filepath1, 'r')
f2 = open(fileout, 'w')

step = 1.0
TStressSet = []

for line in f1:
    content = line.split()
    if content[0] == 'X':
        f2.write(line)
        NodeNumber = len(content) - 1
    else:
        print(float(content[0]))
        if step == float(content[0]):
            TStressSet.append([])
            for obj in content[1:]:
                if not obj.startswith("NoValue"):
                    TStressSet[-1].append(float(obj))
                else:
                    TStressSet[-1].append('No')
        else:
            f2.write('%f ' % step)

            for j in range(0, NodeNumber):
                temp = 0
                LastStepLength = len(TStressSet)
                for i in range(0, LastStepLength):
                    if not type(TStressSet[i][j]) == float or type(TStressSet[i][j]) == int:
                        LastStepLength = LastStepLength - 1
                    else:
                        temp = temp + TStressSet[i][j]
                temp = temp/LastStepLength
                f2.write('%f ' % temp)
            f2.write('\n')

            step = float(content[0])
            TStressSet = [[]]
            for obj in content[1:]:
                if not obj.startswith("NoValue"):
                    TStressSet[-1].append(float(obj))
                else:
                    TStressSet[-1].append('No')

