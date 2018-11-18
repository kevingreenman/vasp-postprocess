#!/usr/bin/env python
#unitcell.py v1.0 08-16-2018 Kevin Greenman kpgreenm@umich.edu
from itertools import islice
import numpy as np
import math

with open('CONTCAR') as lines:
    d = np.genfromtxt(islice(lines, 2, 5))
#print d

a = np.linalg.norm(d[0])
b = np.linalg.norm(d[1])
c = np.linalg.norm(d[2])
#print "%s\t%s\t%s" % (a,b,c)

alpha = math.acos((np.dot(d[1],d[2])/(b*c)))*(180/math.pi)
beta = math.acos((np.dot(d[0],d[2])/(a*c)))*(180/math.pi)
gamma = math.acos((np.dot(d[0],d[1])/(a*b)))*(180/math.pi)
print "%s\t%s\t%s\t%s\t%s\t%s" % (a,b,c,alpha,beta,gamma)
