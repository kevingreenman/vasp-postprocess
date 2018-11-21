vasp_postprocess
==============================
[//]: # (Badges)
[![Travis Build Status](https://travis-ci.org/REPLACE_WITH_OWNER_ACCOUNT/vasp_postprocess.png)](https://travis-ci.org/REPLACE_WITH_OWNER_ACCOUNT/vasp_postprocess)
[![AppVeyor Build status](https://ci.appveyor.com/api/projects/status/REPLACE_WITH_APPVEYOR_LINK/branch/master?svg=true)](https://ci.appveyor.com/project/REPLACE_WITH_OWNER_ACCOUNT/vasp_postprocess/branch/master)
[![codecov](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/vasp_postprocess/branch/master/graph/badge.svg)](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/vasp_postprocess/branch/master)

Processes the output files from VASP to gather important data on structural and electronic properties

### Structural Output
The CONTCAR VASP output file is used to calculate the lattice parameters and angles of the unit cell.
These values are written to a text file in the following order:  

a, b, c, alpha, beta, gamma

### Electronic Output
The EIGENVAL VASP output file is used to calculate electronic properties.
This assumes a cubic unit cell (all three directions equivalent).
The output is written to a text file in the following order:  

VBM, VBM Location, True VBM 1, True VBM 2, True VBM 3, True VBM (avg), True VBM (avg) Location, CBM,
CBM Location, Band Gap, True Band Gap

The True VBM Max is calculated as an average of the highest three bands since all three
directions are equivalent in the crystal. This is often the same as the VBM, but not always.
The True band gap is the difference between the CBM and the True VBM (avg).

### Copyright

Copyright (c) 2018, kpgreenm


#### Acknowledgements
 
Project based on the 
[Computational Chemistry Python Cookiecutter](https://github.com/choderalab/cookiecutter-python-comp-chem)
