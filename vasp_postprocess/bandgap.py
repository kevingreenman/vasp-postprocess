#!/usr/bin/env python
#bandgap.py v1.0 08-16-2018 Kevin Greenman kpgreenm@umich.edu
import numpy as np
import os
from fractions import Fraction

# Setup
direct = os.path.basename(os.getcwd())
with open('EIGENVAL','r') as eg:
    lines = eg.readlines()

# Find nbands
band_low = 1
i = 9
while i < 1000:
    try:
        band_high = int(lines[i].split()[0])
        diff = band_high - band_low
        i += 1
        band_low = band_high
    except:
        nbands = band_low
        break

# K-Points
kp_lines = np.arange(7,len(lines),nbands+2)
kpoints = [lines[i].rstrip('\n').split()[0:3] for i in kp_lines]
for i in range(0,len(kpoints)):
    for j in range(0,3):
        kpoints[i][j] = str(Fraction(float(kpoints[i][j])).limit_denominator(16))
    kpoints[i] = ' '.join(kpoints[i])
        
# CBM
cbm_lines = []
for kp in kp_lines:
    for i in range(kp+1,kp+nbands+1):
        occup = lines[i].split()[2]
        if int(float(occup)) == 0:
            cbm_lines.append(i)
            break
cbm_lines = np.array(cbm_lines)
cbm = [lines[i].split()[1] for i in cbm_lines]
cbm = map(float,cbm)

# VBM
vbm1_lines = cbm_lines - 1
vbm2_lines = cbm_lines - 2
vbm3_lines = cbm_lines - 3
vbm1 = []
vbm2 = []
vbm3 = []
for i in range(0,len(vbm1_lines)):
    vbm1.append(lines[vbm1_lines[i]].split()[1])
    vbm2.append(lines[vbm2_lines[i]].split()[1])
    vbm3.append(lines[vbm3_lines[i]].split()[1])
vbm1 = map(float,vbm1)
vbm2 = map(float,vbm2)
vbm3 = map(float,vbm3)

# VBM Average
avg_vbm = []
for i in range(0,len(vbm1)):
    avg = (vbm1[i] + vbm2[i] + vbm3[i])/3
    avg_vbm.append(avg)

# Energies
vbm_max = max(vbm1)
vbm_true_max = max(avg_vbm)
cbm_min = min(cbm)
gap = cbm_min - vbm_max
true_gap = cbm_min - vbm_true_max
vbm_true_1 = vbm1[avg_vbm.index(vbm_true_max)]
vbm_true_2 = vbm2[avg_vbm.index(vbm_true_max)]
vbm_true_3 = vbm3[avg_vbm.index(vbm_true_max)]

# Locations
vbm_location = kpoints[vbm1.index(vbm_max)]
vbm_true_location = kpoints[avg_vbm.index(vbm_true_max)]
cbm_location = kpoints[cbm.index(cbm_min)]

## Print outputs
#print 'Directory: ' + direct
#print ''
#print 'VBM: ' + str(vbm_max) + ' eV'
#print 'VBM location: ' + str(vbm_location)
#print ''
#print '1st Band at VBM: ' + str(vbm_true_1) + ' eV'
#print '2nd Band at VBM: ' + str(vbm_true_2) + ' eV'
#print '3rd Band at VBM: ' + str(vbm_true_3) + ' eV'
#print ''
#print 'True VBM (top 3 averaged): ' + str(vbm_true_max)  + ' eV'
#print 'True VBM location: ' + str(vbm_true_location)
#print ''
#print 'CBM: ' + str(cbm_min) + ' eV'
#print 'CBM location: ' + str(cbm_location)
#print ''
#print 'Band Gap: ' + str(gap) + ' eV'
#print 'True Band Gap: ' + str(true_gap)  + ' eV'

# Output to text file (comma separated)
data = [direct, vbm_max, vbm_location, vbm_true_1, vbm_true_2, vbm_true_3, vbm_true_max, vbm_true_location, cbm_min, 
        cbm_location, gap, true_gap]
data = map(str,data)
data = ', '.join(data)
with open('bandgap.txt', 'w') as bg:
    bg.write(data)
