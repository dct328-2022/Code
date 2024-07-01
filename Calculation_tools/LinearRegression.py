def LinearRegression(x, y):
	length1 = len(x)
	length2 = len(y)
	if length1 != length2:
		print("Error, In LinearRegression: Lengths of x and y are different!")
	else:
		ax = float(sum(x))/length1
		ay = float(sum(y))/length2
		cov = 0
		var = 0
		for i in range(0, length1):
			cov += (x[i] - ax)*(y[i] - ay)
			var += (x[i] - ax)*(x[i] - ax)
		k = cov/var
		a = ay - k*ax
		return [k, a]
