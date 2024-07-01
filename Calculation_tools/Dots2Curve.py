from sympy import *

def curvify(xlist, ylist, pointnum):
	length1 = len(xlist)
	length2 = len(ylist)
	if length1 != length2:
		print("In curvify, input error")
		return 0
	else:
		a = symbols('a0:%d' % (length1 - 1))
		b = symbols('b0:%d' % (length1 - 1))
		c = symbols('c0:%d' % (length1 - 1))
		eqlist = []
		for i in range(0, length1 - 1):
			eq = a[i]*xlist[i]*xlist[i] + b[i]*xlist[i] + c[i] - ylist[i]
			eqlist.append(eq)
			eq = a[i]*xlist[i+1]*xlist[i+1] + b[i]*xlist[i+1] + c[i] - ylist[i+1]
			eqlist.append(eq)
		
		for i in range(1, length1 - 1):
			eq = 2*a[i]*xlist[i] + b[i] - 2*a[i-1]*xlist[i] - b[i-1]
			eqlist.append(eq)
		varibles = a[1:] + b + c
		sol = solve(eqlist, varibles)
		expp = 0
		for i in range(1, length1 - 1):
			temp = (a[i] - a[0])**2
			temp = temp.subs(sol)
			expp += temp
		expp = simplify(expp)
		print(expp)
		aa = expp.subs(a[0], 2)
		bb = expp.subs(a[0], 1)
		cc = expp.subs(a[0], 0)
		x0 = -bb/(2*aa)
		finalsubs = {a[0]:x0}
		for i in range(1, length1 - 1):
			finalsubs[a[i]] = sol[a[i]].subs({a[0]:x0})
		for i in range(0, length1 - 1):
			finalsubs[b[i]] = sol[b[i]].subs({a[0]:x0})
			finalsubs[c[i]] = sol[c[i]].subs({a[0]:x0})
		interval = (xlist[-1] - xlist[0])/pointnum
		xxlist = []
		yylist = []
		for i in range(0, pointnum + 1):
			xx = xlist[0] + i*interval
			xxlist.append(xx)
			for i in range(0, length1 - 1):
				if xx >= xlist[i] and xx < xlist[i+1]:
					yy = a[i].subs(finalsubs)*xx*xx + b[i].subs(finalsubs)*xx + c[i].subs(finalsubs)
					yylist.append(yy)
					break
		return [xxlist, yylist]
			
		

xx = [0.0446, 0.0565, 0.0838, 0.0923, 0.1093, 0.1332, 0.169, 0.2113, 0.2707, 0.3091]
yy = [125, 150.6, 200.7, 219.5, 244.5, 284.6, 348.4, 389.2, 423.5, 440.3]
curvify(xx, yy, 100)


