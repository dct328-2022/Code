NumList = [24,21,19,18,18,16,15,10,9,6]

length = len(NumList)
Area = 0

for i in range(0, length-1):
    Areai = ((NumList[i]-1)*0.1+0.05 + (NumList[i + 1]-1)*0.1+0.05)*0.2/2
    Area += Areai

print(Area)
