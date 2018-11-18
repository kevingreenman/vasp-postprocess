#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
lattice_and_bandgap.py
Processes the output files from VASP to gather important data on structural and electronic properties

Handles the primary functions
"""

import sys
import argparse
from itertools import islice
import numpy as np
import math
from fractions import Fraction
from common import (warning, ArgumentParserError, GOOD_RET, INPUT_ERROR, IO_ERROR)

__author__ = 'kpgreenm'


# Constants #

# Defaults
# DEF_CONTCAR = None
# DEF_EIGENVAL = None


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--structural", help="Calculate structural properties (lattice parameters and angles)",
                        action='store_true')
    parser.add_argument("-e", "--electronic", help="Calculate electronic properties (band gap, VBM, CBM, etc.)",
                        action='store_true')
    parser.add_argument("-a", "--all", help="Calculate both structural and electronic properties", action='store_true')
    args = None
    try:
        args = parser.parse_args(argv)
    except ArgumentParserError as e:
        warning("Argument Parser Error:", e)
        parser.print_help()
        return args, INPUT_ERROR

    return args, GOOD_RET


def unitcell():
    # Setup
    try:
        with open('./data/CONTCAR') as lines:
            d = np.genfromtxt(islice(lines, 2, 5))
    except FileNotFoundError as e:
        warning("CONTCAR file not found:", e)
        return IO_ERROR

    # Calculate lattice parameters and angles
    a = np.linalg.norm(d[0])
    b = np.linalg.norm(d[1])
    c = np.linalg.norm(d[2])
    alpha = math.acos((np.dot(d[1], d[2]) / (b * c))) * (180 / math.pi)
    beta = math.acos((np.dot(d[0], d[2]) / (a * c))) * (180 / math.pi)
    gamma = math.acos((np.dot(d[0], d[1]) / (a * b))) * (180 / math.pi)

    # Output to text file (comma separated)
    data = [a, b, c, alpha, beta, gamma]
    data = map(str, data)
    data = ', '.join(data)
    with open('unitcell.txt', 'w') as uc:
        uc.write(data)


def bandgap():
    # Setup
    try:
        with open('./data/EIGENVAL', 'r') as eg:
            lines = eg.readlines()
    except FileNotFoundError as e:
        warning("EIGENVAL file not found:", e)
        return IO_ERROR

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
    kp_lines = np.arange(7, len(lines), nbands + 2)
    kpoints = [lines[i].rstrip('\n').split()[0:3] for i in kp_lines]
    for i in range(0, len(kpoints)):
        for j in range(0, 3):
            kpoints[i][j] = str(Fraction(float(kpoints[i][j])).limit_denominator(16))
        kpoints[i] = ' '.join(kpoints[i])

    # CBM
    cbm_lines = []
    for kp in kp_lines:
        for i in range(kp + 1, kp + nbands + 1):
            occup = lines[i].split()[2]
            if int(float(occup)) == 0:
                cbm_lines.append(i)
                break
    cbm_lines = np.array(cbm_lines)
    cbm = [lines[i].split()[1] for i in cbm_lines]
    cbm = map(float, cbm)

    # VBM
    vbm1_lines = cbm_lines - 1
    vbm2_lines = cbm_lines - 2
    vbm3_lines = cbm_lines - 3
    vbm1 = []
    vbm2 = []
    vbm3 = []
    for i in range(0, len(vbm1_lines)):
        vbm1.append(lines[vbm1_lines[i]].split()[1])
        vbm2.append(lines[vbm2_lines[i]].split()[1])
        vbm3.append(lines[vbm3_lines[i]].split()[1])
    vbm1 = map(float, vbm1)
    vbm2 = map(float, vbm2)
    vbm3 = map(float, vbm3)

    # VBM Average
    avg_vbm = []
    for i in range(0, len(vbm1)):
        avg = (vbm1[i] + vbm2[i] + vbm3[i]) / 3
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

    # Output to text file (comma separated)
    data = [vbm_max, vbm_location, vbm_true_1, vbm_true_2, vbm_true_3, vbm_true_max, vbm_true_location, cbm_min,
            cbm_location, gap, true_gap]
    data = map(str, data)
    data = ', '.join(data)
    with open('bandgap.txt', 'w') as bg:
        bg.write(data)


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != GOOD_RET:
        return ret

    if args.structural is True:
        unitcell()
    elif args.electronic is True:
        bandgap()
    elif args.all is True:
        unitcell()
        bandgap()

    return GOOD_RET  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
