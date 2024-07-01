# Calculate the area of polygen

def CrossProduct(x1, y1, x2, y2):
	return x1*y2 - x2*y1
	
def PolygonArea(RefPoint, PointSet):
	# RefPoint should be inside the polygon
	length = len(PointSet)
	x0 = RefPoint[0]
	y0 = RefPoint[1]
	Area = 0
	for i in range(0, length - 1):
		x1 = PointSet[i][0]
		y1 = PointSet[i][1]
		x2 = PointSet[i + 1][0]
		y2 = PointSet[i + 1][1]
		AreaTemp = 0.5*abs(CrossProduct(x1 - x0, y1 - y0, x2 - x0, y2 - y0))
		Area += AreaTemp
	
	x1 = PointSet[length - 1][0]
	y1 = PointSet[length - 1][1]
	x2 = PointSet[0][0]
	y2 = PointSet[0][1]
	AreaTemp = 0.5*abs(CrossProduct(x1 - x0, y1 - y0, x2 - x0, y2 - y0))
	Area += AreaTemp
	return Area

# example	
#print(PolygonArea([0.5, 0.5], [[0, 0], [0, 1], [2, 1], [1, 0]]))
