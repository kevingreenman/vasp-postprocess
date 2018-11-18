#!/usr/bin/env python
from itertools import islice
import numpy as np
import math

with open('CONTCAR') as lines:
    d = np.genfromtxt(islice(lines, 2, 5))

a = np.linalg.norm(d[0])
b = np.linalg.norm(d[1])
c = np.linalg.norm(d[2])

alpha = math.acos((np.dot(d[1],d[2])/(b*c)))*(180/math.pi)
beta = math.acos((np.dot(d[0],d[2])/(a*c)))*(180/math.pi)
gamma = math.acos((np.dot(d[0],d[1])/(a*b)))*(180/math.pi)

# Output to text file (comma separated)
data = [a, b, c, alpha, beta, gamma]
data = map(str, data)
data = ', '.join(data)
with open('unitcell.txt', 'w') as uc:
    uc.write(data)
