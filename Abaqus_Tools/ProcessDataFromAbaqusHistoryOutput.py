def LinearInterpolation2D(x1, y1, x2, y2, xi, tol=0.01):
    if abs(x1 - xi) < tol:
        return y1
    elif abs(x2 - xi) < tol:
        return y2
    else:
        k = (y2 - y1) / (x2 - x1)
        yi = k * (xi - x1) + y1
        return yi


def ListLinearInterpolation2D(xlist, ylist, xi, tol=0.01):
    # xlist must be monotonic
    xlength = len(xlist)
    ylength = len(ylist)
    if xlist[1] < xlist[0]:
        case = 1
    else:
        case = 0
    if xlength != ylength:
        print("The lengths of xlist and ylist are not the same!")
    else:
        if xlist[1] >= xlist[0]:
            if xi < xlist[0]:
                yi = LinearInterpolation2D(xlist[0], ylist[0], xlist[1], ylist[1], xi, tol)
            elif xi > xlist[-1]:
                yi = LinearInterpolation2D(xlist[-2], ylist[-2], xlist[-1], ylist[-1], xi, tol)
            else:
                for i in range(1, xlength):
                    if xi >= xlist[i - 1] and xi <= xlist[i]:
                        yi = LinearInterpolation2D(xlist[i - 1], ylist[i - 1], xlist[i], ylist[i], xi, tol)
                        break
        if xlist[1] < xlist[0]:
            if xi > xlist[0]:
                yi = LinearInterpolation2D(xlist[0], ylist[0], xlist[1], ylist[1], xi, tol)
            elif xi < xlist[-1]:
                yi = LinearInterpolation2D(xlist[-2], ylist[-2], xlist[-1], ylist[-1], xi, tol)
            else:
                for i in range(1, xlength):
                    if xi <= xlist[i - 1] and xi >= xlist[i]:
                        yi = LinearInterpolation2D(xlist[i - 1], ylist[i - 1], xlist[i], ylist[i], xi, tol)
                        break
    return yi

def List2ListLinearInterpolation2D(xlist, ylist, xilist, tol=0.01):
	xilength = len(xilist)
	yilist = []
	for i, obj in enumerate(xilist):
	    yi = ListLinearInterpolation2D(xlist, ylist, obj, tol)
	    yilist.append(yi)
	return yilist

fnread = "C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConduction3/NodePairs11.txt"
fnr = open(fnread, 'r')
NodeSet = []

for line in fnr:
    split = line.split()
    if len(split) == 2:
        NodeSet.append(int(split[0]))

NewTime = range(0, 3610, 60)
NewTime = list(NewTime)
fnw = open("C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConduction3/ffresult.txt", 'w')

for obj in NodeSet:
    Time = []
    Tempr = []
    fnn = open("C:/Users/cdin0015/OneDrive - Monash University/Documents/FDS/PythonAbaqusHeatConduction3/ff%d.txt"%obj)
    for line in fnn:
        split = line.split()
        Time.append(float(split[0]))
        Tempr.append(float(split[1]))
        NewTempr = List2ListLinearInterpolation2D(Time, Tempr, NewTime)
        for item in NewTempr:
            fnw.write("%f "%item)
            fnw.write('\n')



