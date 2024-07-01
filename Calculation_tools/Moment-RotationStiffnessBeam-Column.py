# Computation of the initial moment-rotation of bolted beam-column connections 
# From the book "Structural steel semi-rigid connection" P254

# Bolt row in tension
class Stiffness:
	def __init__(self, Eb, Ab, Lb, E, tta, twa, mta, mwa, I1ta, I2ta, L1ta, L2ta, I1wa, I2wa, L1wa, L2wa, dhta, dhwa, w, bta, ex, exw, p, tpta, tpwa, dbta, dbwa):
		# Eb: Young's modulus of bolts
		# Ab: resistant area of bolts
		# Lb: the sum of the thickness of the connected plates
		# E: Young's modulus of steel plates
		# tta: thickness of flange cleat or side plate
		# twa: thickness of the fin plate
		# mta: P261, Fig6.19
		# mwa: P261, Fig6.19
		# I1, I2, L1, L2: P261 Fig6.19
		# dhta: diameter of bolt nut at web
		# dhwa: diameter of bolt nut at flange
		# w, bta, ex, exw, p: P262 Fig6.20
		# tpta: the thickness of the connected plate elements (flange cleat and beam flange)
		# tpwa: the thickness of the connected plate elements (fin plate and beam web)
		# dbta: the diameter of the bolts at beam flange
		# dbwa: the diameter of the bolts at beam web
		self.Kb = 1.6*Eb*Ab/Lb*(5.1 + 3.25*tpta/dbta)
		
		gmta = (float(I2ta)/L2ta)/(float(I1ta)/L1ta)
		gmwa = (float(I2wa)/L2wa)/(float(I1wa)/L1wa)
		beffta = min(dhta + 2*mta, float(dhta)/2 + mta + 0.5*w, ex + dhta*0.5 + mta)
		bwa = min(dhwa + 2*mwa, p)
		beffwa = min(dhwa + 2*mwa, 0.5*dhwa + mwa + 0.5*p, exw + 0.5*p, exw + dhwa*0.5 + mwa)
		faita = 0.57*(tpta/(dbta*(mta/dbta)**0.5))**(-1.28)
		faiwa = 0.57*(tpwa/(dbwa*(mwa/dbwa)**0.5))**(-1.28)
		self.Kta = faita*E*0.5*beffta*tta**3/(mta**3)*(4*gmta/(4*gmta + 3))
		self.Kwa = faiwa*E*0.5*beffwa*twa**3/(mwa**3)*(4*gmwa/(4*gmwa + 3))
	def Kb(self):
		return self.Kb
	def Kta(self):
		return self.Kta
	def Kwa(self):
		return self.Kwa
