# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global Toggles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# allows importing of custom folders
import sys
sys.path.insert(0, './Backends')

# file supports global variables for the whole project
import Globals as gl

gl.verbose = False
if gl.verbose:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~\n 'verbose' set to True \n~~~~~~~~~~~~~~~~~~~~~~~\n")

gl.save = False
if gl.save:
	print("\n~~~~~~~~~~~~~~~~~~~~\n 'save' set to True \n~~~~~~~~~~~~~~~~~~~~\n")

gl.plot = True
if gl.plot:
	print("\n~~~~~~~~~~~~~~~~~~~~\n 'plot' set to True \n~~~~~~~~~~~~~~~~~~~~\n")

gl.fontscale = 1.0
if gl.fontscale != 1.0:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~\n 'fontscale' set to "+str(gl.fontscale)+"\n~~~~~~~~~~~~~~~~~~~~~~~\n")

gl.lengthscale = 1.0
if gl.lengthscale != 1.0:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\n 'lengthscale' set to "+str(gl.lengthscale)+"\n~~~~~~~~~~~~~~~~~~~~~~~~~\n")

gl.widthscale = 1.0
if gl.widthscale != 1.0:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~\n 'widthscale' set to "+str(gl.widthscale)+"\n~~~~~~~~~~~~~~~~~~~~~~~\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import math as m
import numpy as np
import FittingData as fd
import ReadAndPlot as rp
import AnimatePlot as ap
from uncertainties import ufloat
from uncertainties import umath
from uncertainties import unumpy

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

def expFit(x, A, B, C):
	exp = np.exp(1)
	return A * exp**(np.multiply(B,x)) + C

def expInit():
    return rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]", plotTitle=r"Test animation of exponential decay", grid=True, log=False, xLimits=[0,10], yLimits=[-0.1,1.1])

def expRun(data):
    ax = rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]", plotTitle=r"Test animation of exponential decay", grid=True, log=False, xLimits=[0,10], yLimits=[-0.1,1.1])
    rp.plotData(ax, data[0], data[1], eXs=0, eYs=0, dataLabel=r"$y=e^{-x}$", colour="Blue", lines=True, scale=1.0)

def expData(timeArray, currentTime, A, B, C):
	Xs = [timeArray[i] for i in range(currentTime)]
	Ys = [expFit(timeArray[i], A, B, C) for i in range(currentTime)]
	return Xs, Ys

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# generate an write data
xValues = np.linspace(0,10,100)
yValues = fd.testData(xValues, expFit, params=[1,-1,0], errY=0.1, seed=21448)
rp.writeColumnFile(dataFolder+"expDecayTest.dat", [xValues, yValues], "Test data of decaying exponential\nXs\tYs")

# read and plot data
data = rp.readColumnFile(dataFolder+"expDecayTest.dat", header=2)
ax = rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]", plotTitle=r"Decaying exponential data randomly generated", grid=True, log=False, xLimits=[0,10], yLimits=[-0.1,1.1])
rp.plotData(ax, data[0], data[1], eXs=0, eYs=0, dataLabel=r"$y=e^{-x}$", colour="Blue", lines=False, scale=1.0)
if gl.plot:
	if gl.save:
		rp.plotOutput(savefigname=plotFolder+"expDecayTest.png",resolution=500)
	else:
		rp.plotOutput()


# fit data
fitResults = fd.fitting(data[0], data[1], function=expFit, errYs=None, initGuess=None, bounds=(-5,5), attempts=10000)
popt, pcov = fitResults[0], fitResults[1]

params = [ufloat(popt[i], m.sqrt(pcov[i][i])) for i in range(len(popt))]
fitYs = []
errYs = []
for x in data[0]:
	value = expFit(x,*params)
	fitYs.append(value.n)
	errYs.append(value.s)

ax = rp.plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]", plotTitle=r"Decaying exponential fit", grid=True, log=False, xLimits=None, yLimits=None)
rp.plotData(ax, data[0], data[1], eXs=0, eYs=0, dataLabel=r"$y=e^{-x}$", colour="Blue", lines=False, scale=1.0)
rp.plotData(ax, data[0], fitYs, eXs=0, eYs=errYs, dataLabel=r"Fit data", colour="Red", lines=True, scale=1.0)
if gl.plot:
	if gl.save:
		rp.plotOutput(savefigname=plotFolder+"expDecayFitTest.png",resolution=500)
	else:
		rp.plotOutput()

print("Fit results:\nA\tB\tC")
for element in popt:
	print("{:.2}".format(element)+"\t", end="")
print()


# animation example
myAni = ap.animate(dataFunc=expData, dataFuncParams=popt, timeArray=data[0], frameTime=30, initFunc=expInit, runningFunc=expRun)
if gl.plot:
	if gl.save:
		ap.aniOutput(myAni, savefigname=animationFolder+"expDecayAniTest.mp4", framerate=10, resolution=500, bitrate=None)
	else:
		ap.aniOutput(myAni)
