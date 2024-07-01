def NumberList(Copied):
	numbers = Copied.split()
	EmptyList = []
	for obj in numbers:
		EmptyList.append(float(obj))
	return EmptyList
