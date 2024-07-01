def EquivalentMomentInertia(Is, L, bc1, bc2, hc):
	# Is: Moment of inertia of steel beam
	# L: Span Length of the beam
	# bci,i=1 or 2: actual slab width at two sides of the composite frame beam (half width at two sides)
	# hc: concrete slab thickness
	Ic = (min(0.1*L, bc1) + min(0.1*L, bc2))*(hc**3)/(12*6.87)
	print('Ic = %f' % Ic)
	alpha = 2.2/((float(Is)/Ic)**0.3 - 0.5) + 1
	Ie = alpha*Is
	return Ie

	

