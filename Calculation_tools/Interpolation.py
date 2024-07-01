status = "use"
#status = "try"
# choose "use" or "try"

import copy

def LinearInterpolation2D(x1, y1, x2, y2, xi, tol=0.01):
    if abs(x1 - xi) < tol:
        return y1
    elif abs(x2 - xi) < tol:
        return y2
    else:
        k = (y2 - y1)/(x2 - x1)
        yi = k*(xi - x1) + y1
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
	                if xi >= xlist[i-1] and xi <= xlist[i]:
	                    yi = LinearInterpolation2D(xlist[i-1], ylist[i-1], xlist[i], ylist[i], xi, tol)
	                    break
	    if xlist[1] < xlist[0]:
	        if xi > xlist[0]:
	            yi = LinearInterpolation2D(xlist[0], ylist[0], xlist[1], ylist[1], xi, tol)
	        elif xi < xlist[-1]:
	            yi = LinearInterpolation2D(xlist[-2], ylist[-2], xlist[-1], ylist[-1], xi, tol)
	        else:
	            for i in range(1, xlength):
	                if xi <= xlist[i-1] and xi >= xlist[i]:
	                    yi = LinearInterpolation2D(xlist[i-1], ylist[i-1], xlist[i], ylist[i], xi, tol)
	                    break
	return yi
	
def List2ListLinearInterpolation2D(xlist, ylist, xilist, tol=0.01):
	xilength = len(xilist)
	yilist = []
	for i, obj in enumerate(xilist):
	    yi = ListLinearInterpolation2D(xlist, ylist, obj, tol)
	    yilist.append(yi)
	return yilist

def IfColinear(x1, y1, x2, y2, x3, y3, tol=0.01):
    vector1 = [x2 - x1, y2 - y1]
    vector2 = [x3 - x1, y3 - y1]
    pand = vector1[0]*vector2[1] - vector1[1]*vector2[0]
    if abs(pand) < tol:
        return True
    else:
        return False

def LinearInterpolation3D(x1, y1, z1, x2, y2, z2, x3, y3, z3, xi, yi, tol=0.01):
    if abs(x1 - xi) < tol and abs(y1 - yi) < tol:
        return z1
    elif abs(x2 - xi) < tol and abs(y2 - yi) < tol:
        return z2
    elif abs(x3 - xi) < tol and abs(y3 - yi) < tol:
        return z3
    else:
        temp = x1*y2 - x1*y3 - x2*y1 + x2*y3 + x3*y1 - x3*y2
        if not temp == 0:
            return (x1*y2*z3 - x1*y3*z2 + x1*yi*z2 - x1*yi*z3 - x2*y1*z3 + x2*y3*z1 - x2*yi*z1 + x2*yi*z3 + x3*y1*z2 - x3*y2*z1 + x3*yi*z1 - x3*yi*z2 - xi*y1*z2 + xi*y1*z3 + xi*y2*z1 - xi*y2*z3 - xi*y3*z1 + xi*y3*z2)/(x1*y2 - x1*y3 - x2*y1 + x2*y3 + x3*y1 - x3*y2)
        else:
            print("Error, Three points are colinear")

'''from sympy import *
x1, y1, z1, x2, y2, z2, x3, y3, z3, xi, yi, zi = symbols('x1, y1, z1, x2, y2, z2, x3, y3, z3, xi, yi, zi')
v1 = [x2 - x1, y2 - y1, z2 - z1]
v2 = [x3 - x1, y3 - y1, z3 - z1]
v3 = [x3 - xi, y3 - yi, z3 - zi]
M = Matrix([v1, v2, v3])
DM = det(M)
print(DM)
zz = solve(DM, zi)
print(zz)'''

### ==================== Have a try ================================

if status == "try":
    '''yi = LinearInterpolation3D(0, 0, 0, 1, 0, 1, 0, 1, 2, 0.5, 0.5)
    print(yi)'''

    y1 = LinearInterpolation2D(1.1, 0.066, 1.2, 0.074, 7.4/6.6)
    print(y1)

    y1 = ListLinearInterpolation2D([0, 1, 2, 3, 4, 5], [0, 2, 4, 8, 20, 50], 4.233)
    print(y1)

    #yi = LinearInterpolation2D(88843.4, 1.072411, 93073.1, 1.080109, 1.10634898685)
    #print(yi)
    

