# ========================== This script for generating local stiffness matrix for a 3D beam element ===========

import numpy as np

def StiffnessMatrix3DBeam(l, E, G, A, Iy, Iz, J):
  K = np.zeros((12, 12))
  K[0, 0] = E*A/l
  K[1, 1] = 12*E*Iz/(l**3)
  K[2, 2] = 12*E*Iy/(l**3)
  K[3, 3] = G*J/l
  K[4, 4] = 4*E*Iy/l
  K[5, 5] = 4*E*Iz/l

  K[6, 6] = K[0, 0]
  K[7, 7] = K[1, 1]
  K[8, 8] = K[2, 2]
  K[9, 9] = K[3, 3]
  K[10, 10] = K[4, 4]
  K[11, 11] = K[5, 5]

  K[2, 4] = K[4, 2] = -6*E*Iy/(l**2)
  K[1, 5] = K[5, 1] = 6*E*Iz/(l**2)
  K[0, 6] = K[6, 0] = -K[0, 0]
  K[1, 7] = K[7, 1] = -K[1, 1]
  K[1, 11] = K[11, 1] = 6*E*Iz/(l**2)
  K[2, 8] = K[8, 2] = -K[2, 2]
  K[2, 10] = K[10, 2] = K[2, 4]
  K[3, 9] = K[9, 3] = K[3, 3]
  K[4, 8] = K[8, 4] = 6*E*Iy/(l**2)
  K[4, 10] = K[10, 4] = 2*E*Iy/l
  K[5, 7] = K[7, 5] = -6*E*Iz/(l**2)
  K[5, 11] = K[11, 5] = 2*E*Iz/l
  K[7, 11] = K[11, 7] = -6*E*Iz/(l**2)
  K[8, 10] = K[10, 8] = 6*E*Iy/(l**2)
  return K

