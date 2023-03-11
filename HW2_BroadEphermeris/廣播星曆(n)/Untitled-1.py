delta_n =       4.0662*10**(-9)
M0 =            0.6297
Cuc =           0.410899519920*10**(-5)
e =             0.113407603931*10**(-1)
Cus =           0.756420195103*10**(-5)
sqrt_a =        0.515367056465*10**(4)
toe =          0.518400000000*10**(-6)
Cic =          -0.128522515297*10**(-6)
BigOmega0 =    -1.66303701434
Cis =          0.132247805595*10**(-6)
i0 =           0.986587764323
Crc =          246.9375
omega =        0.882160600524
BigOmega1 =    -0.808819404861*10**(-8)
i1 =           0.168935608275*10**(-9) 

#Step1
μ = float(398600800000000)
omegae = float(0.00007292115147)

# Step2
a = (sqrt_a)**2
n0 = float((μ/(a**3))**(0.5))

#Step3
t = 86400*6+15*60
toe = 86400*6
tk = t - toe

# Step4
n = n0 + delta_n

# Step5
from cmath import pi
import math
M = M0 + n * tk
##迭代解
E = M
for m in range(1000):
    E = E - ((E - e*(math.sin(E)) - M) / (1 - e*(math.cos(E))))
    
# Step6
import numpy as np
cos_fk = (math.cos(E) - e)/(1 - e*math.cos(E))
sin_fk = (1 - e**2)**(0.5) * math.sin(E) / (1 - e * math.cos(E))
fk = math.atan((sin_fk/cos_fk)) #* (180 / np.pi)
   
#Step7
uk = omega + fk + Cus*(math.sin(2*(omega+fk)))+ Cuc*(math.cos(2*(omega+fk)))
rk = a*(1-e*math.cos(E)) + Crc*math.sin(2*(omega+fk)) +Crc*math.cos(2*(omega+fk))
ik = i0 + i1*tk + Cis*math.sin(2*(omega+fk)) +Cic*math.cos(2*(omega+fk))

#Step8
lk = BigOmega0 + (BigOmega1-omegae)*tk-omegae*toe

# Step9
x = rk*math.cos(uk)
y = rk*math.sin(uk)

#
X = (x*math.cos(lk)-y*math.cos(ik)*math.sin(lk)) / 1000
Y = (x*math.sin(lk)+y*math.cos(ik)*math.cos(lk)) / 1000
Z = (y*math.sin(ik)) / 1000
print("X=",X)
print("Y=",Y)
print("Z=",Z)

#誤差
X_IGS = 14581.408067
Y_IGS = -1494.739422
Z_IGS = 21889.107258
error_X = X-X_IGS
error_Y = Y-Y_IGS
error_Z = Z-Z_IGS
print(error_X)
print(error_Y)
print(error_Z)