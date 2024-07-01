import math

class ExpansionFactor:
  def __init__(self, Radius, Length, TemperatureChange, Preload, E, dw, Di, Ec):
    # Radius is the radius of the bolt
    # Length is the length of the bolt shank
    # TemperatureChange is the change of temperature in the predefined field
    # E is the Young's modulus of the bolt
    # dw is the diameter of bolt head
    # Di is the bolt hole diameter
    # Ec is the Young's modulus of the plate
    
    lf = Length
    A = math.pi*Radius*Radius
    Deq = dw + lf/10.0
    Aeq = math.pi/4*(Deq*Deq - Di*Di)
    kc = Ec*math.pi*(dw*dw/4-Di*Di/4)/Length
    #kc = 0.1e1 / (math.log(dw + Di) - math.log(dw - Di) - math.log(Length + dw + Di) + math.log(Length - Di + dw)) * math.pi * E * Di / 2
    k = E*A/Length
    dl = -Preload*Length*(k + kc)/(A*E*(k - kc))
    self.alpha = dl/(TemperatureChange*Length)
    print(kc, k)
  def alpha(self):
    return self.alpha



# Usage
#alpha = ExpansionFactor(18, 80, 1, 1000, 205000).alpha
alpha = ExpansionFactor(6.0, 12.0, 1.0, 33929, 205000, 24.0, 14.0, 205000).alpha
print(alpha)

