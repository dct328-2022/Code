# This file reorder the references

# Original order
Inputs = [1, 89, 2, 3, 4, 5, 6, 88, 7, 8, 9, 10, 84, 85, 86, 87, 11, 12, 13, 14, 15]
inputs = range(16, 84)
Inputs = Inputs + inputs

# Program
Outputs = []
length = len(Inputs)
new = 1
for i, obj in enumerate(Inputs):
	if obj in Inputs[0:i]:
		ind = Inputs[0:i].index(obj)
		Outputs.append(Inputs[ind])
	else:
		Outputs.append(new)
		new += 1
		
print(Outputs)

for i in range(0, length*2):
	if i in Inputs:
		ind = Inputs.index(i)
		out = Outputs[ind]
		print(i, out)


