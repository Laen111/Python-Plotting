# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# allows importing of custom folders
import sys
sys.path.insert(0, './Backends')

import math as m
import numpy as np
import Globals as gl
import FittingData as fd
import ReadAndPlot as rp
import AnimatePlot as ap
from uncertainties import ufloat
from uncertainties import unumpy

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Toggles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

gl.verbose = False
if gl.verbose:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~\n 'verbose' set to True \n~~~~~~~~~~~~~~~~~~~~~~~\n")

gl.save = False
if gl.save:
	print("\n~~~~~~~~~~~~~~~~~~~~\n 'save' set to True \n~~~~~~~~~~~~~~~~~~~~\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Constants
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

h = 6.62607015*10**(-34) #Js
e = 1.602176634*10**(-19) #C
hbar = 6.58*10**(-16) #eV s

dataFolder = "./Data/"
plotFolder = "./Plots/"
animationFolder = "./Animations/"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def expDecay(x, xErr=0):
	if xErr == 0:
		xVal = ufloat(x, xErr)
		result = m.exp(-xVal)
		return [result.n, result.s]
	else:
		return m.exp(-x)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
