import math

class Matrix:
  def __init__(self, M1):
    self.M1 = M1
    self.n11 = len(self.M1)
    self.n12 = len(self.M1[0])

  def MultiplyMatrix(self, M2):
    self.M2 = M2
    self.n21 = len(self.M2)
    self.n22 = len(self.M2[0])
    if self.n21 != self.n12:
      print("Matrices cannot multiply!")
    else:
      self.M3 = []
      for i in range(0, self.n11):
        self.M3.append([])
        for j in range(0, self.n22):
          sum = 0
          for k in range(0, self.n12):
            sum += self.M1[i][k] * self.M2[k][j]
          self.M3[-1].append(sum)
      return self.M3

  def MultiplyNumber(self, num):
    self.M3 = []
    for i in range(0, self.n11):
      self.M3.append([])
      for j in range(0, self.n12):
        self.M3[-1].append(num * self.M1[i][j])
    return self.M3

class StrainRossette:
  def __init__(self, StrainX, StrainS, StrainY, E, v):
    # StrainX: A list of horizontal strains
    # StrainY: A list of vertical strains
    # StrainS: A list of strains in 45 degree direction
    # E is Young's Modulus
    # v is Poisson's Ratio
    length1 = len(StrainX)
    length2 = len(StrainY)
    length3 = len(StrainS)
    if length1 != length2 or length2 != length3 or length1 != length3:
      print("Three Strain Components should have same length")
    else:
      Angle = []
      Px = []
      Py = []
      VMStrain = []
      VMStress = []
      for i in range(0, length1):
        ShearStrain = -StrainX[i] + 2*StrainS[i] - StrainY[i]
        SquareMatrix = [[1, v, 0], [v, -1, 0], [0, 0, (1 - v)/2]]
        Step1 = Matrix(SquareMatrix).MultiplyNumber(float(E)/(1 - v**2))
        Step2 = Matrix(Step1).MultiplyMatrix([[StrainX[i]], [StrainY[i]], [ShearStrain]])
        VMStress.append((Step2[0][0]**2 - Step2[0][0]*Step2[1][0] + Step2[1][0]**2 + 3*Step2[2][0]**2)**0.5)
        Angle.append(math.atan(ShearStrain/(StrainX[i] - StrainY[i]))*0.5)
        p1 = (StrainX[i] + StrainY[i])/2
        p2 = (((StrainX[i] - StrainY[i])/2)**2 + (ShearStrain/2)**2)**0.5
        Px.append(p1 + p2)
        Py.append(p1 - p2)
        VMStrain.append(2.0**0.5/3*((2*p2)**2 + (p1 + p2)**2 + (p1 - p2)**2)**0.5)

    self.Px = Px
    self.Py = Py
    self.Angle = Angle
    self.VMStrain = VMStrain
    self.VMStress = VMStress

  def Px(self):
    # ============ Principal Strain 1 ================
    return self.Px

  def Py(self):
    # ============ Principal Strain 2 ===============
    return self.Py

  def Angle(self):
    return self.Angle

  def VMStrain(self):
    # ============== Equivalent Von-mises Strain =====================
    return self.VMStrain


# ================ ImportFile =========================
File = open('/media/chenting/Work/ProgramCode/StrainRossette/SX1-1StrainGuages.txt')
Px = []
Py = []
Angle = []
n = 0

for line in File:
  content = line.split()
  if len(content) == 3:
    n = n + 1
    Px.append(float(content[2]))
    Py.append(float(content[1]))
    Angle.append(float(content[0]))

File.close()

Result = StrainRossette(Px, Py, Angle, 205e-3, 0.3)

File = open('/media/chenting/Work/ProgramCode/StrainRossette/SX1-1StrainGuagesResult.txt', 'w')
for i in range(0, n):
  File.write('%f %f %f %f\n' % (Result.Px[i], Result.Py[i], Result.Angle[i], Result.VMStress[i]))

print('2nd')
r2 = StrainRossette([97], [455], [-122], 205e-3, 0.3)
print(r2.VMStress[0])

File.close()
