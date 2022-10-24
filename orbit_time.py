import math
from math import sqrt

e = 0.205630
a = 57909050

b = sqrt(1-e**2)

c = a * b

print(c)

d = (c + a)/2

print(d)

g = a / 149597870
print(g)

e = g ** 3 

f = sqrt(e)

print(f"Years of orbit = {f}")