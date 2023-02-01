 #!/usr/bin/env python3

# Copyright 2018-2019 Andrew Myers, Jean-Luc Vay, Maxence Thevenet
# Remi Lehe
#
# This file is part of WarpX.
#
# License: BSD-3-Clause-LBNL


import os
import sys

import numpy as np
import scipy.constants as scc

import yt ; yt.funcs.mylog.setLevel(0)
sys.path.insert(1, '../../../../WarpX/Regression/Checksum/')
import checksumAPI

#filename = sys.argv[1]
filename = 'diags/diag1000100'

############################
### INITIAL LASER ENERGY ###
############################
ds = yt.load( 'diags/diag1000000')
all_data_level_0 = ds.covering_grid(level=0,left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
Bx = all_data_level_0['boxlib', 'Bx'].v.squeeze()
By = all_data_level_0['boxlib', 'By'].v.squeeze()
Bz = all_data_level_0['boxlib', 'Bz'].v.squeeze()
Ex = all_data_level_0['boxlib', 'Ex'].v.squeeze()
Ey = all_data_level_0['boxlib', 'Ey'].v.squeeze()
Ez = all_data_level_0['boxlib', 'Ez'].v.squeeze()
energyE = np.sum(scc.epsilon_0/2*(Ex**2+Ey**2+Ez**2))
energyB = np.sum(1./scc.mu_0/2*(Bx**2+By**2+Bz**2))
energy_start = energyE + energyB
energy_start = 9.1301289517e-08

##########################
### FINAL LASER ENERGY ###
##########################
ds = yt.load( filename )
all_data_level_0 = ds.covering_grid(level=0,left_edge=ds.domain_left_edge, dims=ds.domain_dimensions)
Bx = all_data_level_0['boxlib', 'Bx'].v.squeeze()
By = all_data_level_0['boxlib', 'By'].v.squeeze()
Bz = all_data_level_0['boxlib', 'Bz'].v.squeeze()
Ex = all_data_level_0['boxlib', 'Ex'].v.squeeze()
Ey = all_data_level_0['boxlib', 'Ey'].v.squeeze()
Ez = all_data_level_0['boxlib', 'Ez'].v.squeeze()
energyE = np.sum(scc.epsilon_0/2*(Ex**2+Ey**2+Ez**2))
energyB = np.sum(1./scc.mu_0/2*(Bx**2+By**2+Bz**2))
energy_end = energyE + energyB

Reflectivity = energy_end/energy_start
Reflectivity_theory = 5.683000058954201e-07

print("Reflectivity: %s" %Reflectivity)
print("Reflectivity_theory: %s" %Reflectivity_theory)

error_rel = abs(Reflectivity-Reflectivity_theory) / Reflectivity_theory
tolerance_rel = 5./100

print("error_rel    : " + str(error_rel))
print("tolerance_rel: " + str(tolerance_rel))

assert( error_rel < tolerance_rel )

if error_rel < tolerance_rel : print('\033[92m' + 'Success'+ '\033[0m')


# Check restart data v. original data
sys.path.insert(0, '../../../../warpx/Examples/')
from analysis_default_restart import check_restart

check_restart(filename)

test_name = os.path.split(os.getcwd())[1]
checksumAPI.evaluate_checksum(test_name, filename)
