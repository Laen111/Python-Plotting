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

gl.verbose = True
if gl.verbose:
	print("\n~~~~~~~~~~~~~~~~~~~~~~~\n 'verbose' set to True \n~~~~~~~~~~~~~~~~~~~~~~~\n")

gl.save = True
if gl.save:
	print("\n~~~~~~~~~~~~~~~~~~~~\n 'save' set to True \n~~~~~~~~~~~~~~~~~~~~\n")

gl.plot = True
if gl.plot:
	print("\n~~~~~~~~~~~~~~~~~~~~\n 'plot' set to True \n~~~~~~~~~~~~~~~~~~~~\n")

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
if gl.verbose:
	import time

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

# planck curve from phys472 as function of omega (angular frequency)
def uomega(omega, temp):
	return 3.87*10**(-61) * omega**3 * 1/(m.exp(7.64*10**(-12)*omega/temp)-1)

# function of intensity output of laser as function of one mirror's transmisson coefficent
# normalized against I^saturation
# s (absorbtion cooeficent of mirror) = 0.04
# 1 = r + t + s
# a = g_0*L*g is set to 0.1, 1, 30
# eqn. 5.2.11 in M&E
def Iout_inexact(t,a):
	return t*(a/(0.04+t)-0.5)

# function of intensity output of laser as function of one mirror's transmisson coefficent
# normalized against I^saturation
# s (absorbtion cooeficent of mirror) = 0.04
# 1 = r + t + s
# a = g_0*L*g is set to 0.1, 1, 30
# eqn. 5.5.18 in M&E
def Iout_exact(t,a):
	term1 = (t*m.log(0.96-t))/(0.04+t)
	term2 = a/m.log(0.96-t) + 0.5
	return term1*term2

# ---------- ising model for phys 472 ----------------------
def initalizeSpins(gridSize, numpySeed=385037):
	np.random.seed(seed)
	spinArray = []
	for i in range(gridSize):
		spinArray.append([])
		for j in range(gridSize):
			if np.random.uniform() < 0.5:
				spinArray[i].append(1)
			else:
				spinArray[i].append(-1)
	return spinArray

# gives energy difference of dipole flip
def deltaU(i,j,spinArray):
	top = 0
	bot = 0
	left = 0
	right = 0
	if i == 1:
		top = spinArray[-1][j]
	else:
		top = spinArray[i-1][j]
	if i == len(spinArray)-1:
		bot = spinArray[0][j]
	else:
		bot = spinArray[i+1][j]
	if j == 1:
		left = spinArray[i][-1]
	else:
		left = spinArray[i][j-1]
	if j == len(spinArray[i])-1:
		right = spinArray[i][0]
	else:
		right = spinArray[i][j+1]
	return 2*spinArray[i][j]*(top+bot+left+right)

# goes through spin array and trys flipping
def ising(spinArray,gridSize):
	rowNum, colNum = np.random.randint(0, gridSize-1), np.random.randint(0, gridSize-1)
	Ediff = deltaU(rowNum,colNum,spinArray)
	if Ediff <= 0:
		spinArray[rowNum][colNum] = -spinArray[rowNum][colNum]
	elif np.random.uniform(0,1) < np.exp(-Ediff/temp):
		spinArray[rowNum][colNum] = -spinArray[rowNum][colNum]

# wraps the plotInit function to keep axes the same each call for Ising animation
def IsingInit():
	return rp.plotInit(xAx=r"Columns", yAx=r"Rows",plotTitle=r"Ising for "+str(attempts)+" attempts at T="+str(temp), grid=False)

# gets Ising data every frame, and plots it
def isingRun(data):
    ax = IsingInit()
    rp.plot2D(ax, data, colourmap="bwr")

# function that outputs Ising 2d array of spins
def isingDataFunc(timeArray, currentTime, spinArray):
	ising(spinArray,size)
	return spinArray

# problem 2.28 from Schroeder's Thermal Physics book
# determine total magnetization
def determineMag(spinArray):
	total = 0
	for subArray in spinArray:
		for spin in subArray:
			total += spin
	return total

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Scripting
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Npoints = 200
# ts = [i/Npoints * 0.96 for i in range(0,Npoints)]

# in_tenth = [Iout_inexact(i,0.1) for i in ts]
# in_one = [Iout_inexact(i,1) for i in ts]
# in_thirty = [Iout_inexact(i,30) for i in ts]

# ex_tenth = [Iout_exact(i,0.1) for i in ts]
# ex_one = [Iout_exact(i,1) for i in ts]
# ex_thirty = [Iout_exact(i,30) for i in ts]

# f = open(dataFolder+"Iout_inexact_exact.dat","w+")
# for i in range(len(ts)):
# 	f.write(str(ts[i])+"	"+str(in_tenth[i])+"	"+str(in_one[i])+"	"+str(in_thirty[i])+"	"+str(ex_tenth[i])+"	"+str(ex_one[i])+"	"+str(ex_thirty[i])+"	" + "\n")
# f.close()

# data = rp.readColumnFile(dataFolder+"Iout_inexact_exact.dat")

# ax =rp.plotInit(xAx=r"t", yAx=r"$\frac{I_\nu^{out}}{I_\nu^{sat}}$", plotTitle=r"$I_\nu^{out}$ Eqn. 5.2.11 for several values of $g_0 L_g$ and $s=0.04$")
# rp.plotData(ax, data[0], data[1], 0, 0, dataLabel=r"$g_0 L_g = 0.1$", colour="Black")
# rp.plotData(ax, data[0], data[2], 0, 0, dataLabel=r"$g_0 L_g = 1$", colour="Blue")
# rp.plotData(ax, data[0], data[3], 0, 0, dataLabel=r"$g_0 L_g = 30$", colour="Green")
# rp.plotOutput(plotFolder+"InexactIout.png")

# rp.plotInit(xAx=r"t", yAx=r"$\frac{I_\nu^{out}}{I_\nu^{sat}}$", plotTitle=r"$I_\nu^{out}$ Eqn. 5.8.18 for several values of $g_0 L_g$ and $s=0.04$")
# rp.plotData(data[0], data[4], 0, 0, dataLabel=r"$g_0 L_g = 0.1$", colour="Black")
# rp.plotData(data[0], data[5], 0, 0, dataLabel=r"$g_0 L_g = 1$", colour="Blue")
# rp.plotData(data[0], data[6], 0, 0, dataLabel=r"$g_0 L_g = 30$", colour="Green")
# rp.plotOutput(plotFolder+"ExactIout.png")

# rp.plotInit(xAx=r"t", yAx=r"$\frac{I_\nu^{out}}{I_\nu^{sat}}$", plotTitle=r"$I_\nu^{out}$ where $g_0 L_g = 0.1$ and $s=0.04$")
# rp.plotData(data[0], data[1], 0, 0, dataLabel=r"Inexact Eqn. 5.2.ll", colour="Black")
# rp.plotData(data[0], data[4], 0, 0, dataLabel=r"Exact Eqn. 5.8.l8", colour="Blue")
# rp.plotOutput(plotFolder+"Iout_tenth.png")

# rp.plotInit(xAx=r"t", yAx=r"$\frac{I_\nu^{out}}{I_\nu^{sat}}$", plotTitle=r"$I_\nu^{out}$ where $g_0 L_g = 1$ and $s=0.04$")
# rp.plotData(data[0], data[2], 0, 0, dataLabel=r"Inexact Eqn. 5.2.ll", colour="Black")
# rp.plotData(data[0], data[5], 0, 0, dataLabel=r"Exact Eqn. 5.8.l8", colour="Blue")
# rp.plotOutput(plotFolder+"Iout_one.png")

# rp.plotInit(xAx=r"t", yAx=r"$\frac{I_\nu^{out}}{I_\nu^{sat}}$", plotTitle=r"$I_\nu^{out}$ where $g_0 L_g = 30$ and $s=0.04$")
# rp.plotData(data[0], data[3], 0, 0, dataLabel=r"Inexact Eqn. 5.2.ll", colour="Black")
# rp.plotData(data[0], data[6], 0, 0, dataLabel=r"Exact Eqn. 5.8.l8", colour="Blue")
# rp.plotOutput(plotFolder+"Iout_thirty.png")


# -------- ising model ----------------------------
# seed = 254393
# temp = 2.4 # units of epsilon/Kelvin
# size = 5
# attempts = 100
# filename = "ising_T"+str(temp)

# np.random.seed(seed)
# spins = initalizeSpins(size)
# for i in range(attempts*size**2):
# 	ising(spins,size)

# ax = IsingInit()
# rp.plot2D(ax, spins, colourmap="bwr")
# if not gl.save:
# 	rp.plotOutput()
# else:
# 	rp.plotOutput(plotFolder+"image_"+filename+".png")

# ax = rp.plotInit(xAx=r"Columns", yAx=r"Rows",plotTitle=r"Ising for "+str(attempts)+" attempts at T="+str(temp), grid=False)
# rp.plotHist(ax, magnets, binColour="Blue", dataLabel=r"Default")
# if not gl.save:
# 	rp.plotOutput()
# else:
# 	rp.plotOutput(plotFolder+"hist_magnet_"+filename+".png")

# np.random.seed(seed)
# spins = initalizeSpins(size)
# animationTime = np.linspace(0,0,attempts*size**2)
# myAni = ap.animate(dataFunc=isingDataFunc, dataFuncParams=[spins], timeArray=animationTime, frameTime=30, initFunc=IsingInit, runningFunc=isingRun)
# if not gl.save:
# 	ap.aniOutput(myAni)
# else:
# 	ap.aniOutput(myAni, framerate=30, savefigname=animationFolder+"animate_"+filename+".mp4")



# script to complete problem 2.28 in Schroeder's Thermal Physics book
seed = 259383
size = 5
attempts = 100
num = 20
initT = 3.0
finalT = 1.0

np.random.seed(seed)
spins = initalizeSpins(size) # only initalize once, let each lower temp start from previous final state
magnets = []
hist2DData = []
for i in range(num):
	if gl.verbose:
		print("\nOn step "+str(i)+" of "+str(num)+"\t"+'{0:.1f}'.format(100*i/num)+"% complete")
		print('{0:.1f}'.format(time.process_time()/60)+" minutes elapsed\t"+'{0:.1f}'.format(time.process_time()*(num/(i+0.1) - 1)/60)+" minutes remain")

	temp = initT + i * (finalT - initT)/num # temp in units of epsilon/Kelvin
	filename = "ising_T"+str(temp)+"_size"+str(size)+"_attempts"+str(attempts)
	
	magnets.append([])
	magnets[i].append(determineMag(spins))

	for ampt in range(attempts*size**2):
		ising(spins,size)
		magnets[i].append(determineMag(spins))
	
	rp.writeColumnFile(dataFolder+"/spins/"+str(i)+".dat", spins, header="Final array of spins for temperature "+str(temp)+"\n")

	ax = IsingInit()
	rp.plot2D(ax, spins, colourmap="bwr")
	if gl.plot:
		if not gl.save:
			rp.plotOutput()
		else:
			rp.plotOutput(plotFolder+"image_"+filename+".png")

	ax = rp.plotInit(xAx=r"Total magnetization", yAx=r"Count",plotTitle=r"Ising for "+str(attempts)+" attempts at T="+str(temp), grid=False)
	n, bins, patches = rp.plotHist(ax, magnets[i], xLimits=[-size**2,+size**2],binNumber=1+size**2, binColour="Blue", dataLabel=r"Total magnetization", log=True)
	if gl.plot:
		if not gl.save:
			rp.plotOutput()
		else:
			rp.plotOutput(plotFolder+"hist_"+filename+".png")
	hist2DData.append(n)


# write counts data to plot hist
tempRange = np.linspace(initT, finalT, num)
head = "Binned counts of frequency of total magnetization (summed Spins) of Ising model\n"
head += "Rows are each occurance of the total magnetizations, (only even or only odd numbers allowed)\n"
head += "Columns are each of the different temperature trials\n"

setUpParams = [seed, size, attempts, num, initT, finalT]
paramName = ["seed", "size", "attempts", "num", "initT", "finalT"]
for i in range(len(setUpParams)):
	head += str(paramName[i]+": "+str(setUpParams[i])+"\t")
head += "\n\n"

for i in tempRange:
	head += str(setUpParams[1])+"\t"
head += "\n"
for temp in tempRange:
	head += '{0:.2f}'.format(temp)+"\t"

rp.writeColumnFile(dataFolder+"magnetizationFreq_"+str(initT)+"to"+str(finalT)+".dat", magnets, header=head)


# write binned data that can be 2d plot
tempRange = np.linspace(initT, finalT, num)
head = "Counts of frequency of total magnetization (summed Spins) of Ising model\n"
head += "Bins(Rows) are the total magnetizations, starting at -size^2, runs to +size^2, (only even or only odd numbers allowed)\n"
head += "Columns are each of the different temperature trials\n"

setUpParams = [seed, size, attempts, num, initT, finalT]
paramName = ["seed", "size", "attempts", "num", "initT", "finalT"]
for i in range(len(setUpParams)):
	head += str(paramName[i]+": "+str(setUpParams[i])+"\t")
head += "\n\n"

for i in tempRange:
	head += str(setUpParams[1])+"\t"
head += "\n"
for temp in tempRange:
	head += '{0:.2f}'.format(temp)+"\t"

rp.writeColumnFile(dataFolder+"magnetizationHistograms_"+str(initT)+"to"+str(finalT)+".dat", hist2DData, header=head)


# plot the 2D histogram
readData = rp.readColumnFile(dataFolder+"magnetizationHistograms_"+str(initT)+"to"+str(finalT)+".dat", header=5)
# the first two entries of each sub array is the size and current temperature
histData = []
for subArray in readData:
	histData.append([subArray[i] for i in range(2,len(subArray))])

ax = rp.plotInit(xAx=r"Total Magnetization", yAx=r"Temperature",plotTitle=r"Ising for "+str(attempts)+" attempts at various tempratures", grid=True)
rp.plot2D(ax, histData, xLimits=[-readData[-1][0]**2,+readData[0][0]**2], yLimits=[readData[-1][1], readData[0][1]], colourmap="gist_rainbow", log=False)
if gl.plot():
	if not gl.save:
		rp.plotOutput()
	else:
		rp.plotOutput(plotFolder+"hist2D_ising_T"+str(readData[-1][1])+"to"+str(readData[0][1])+"_size"+str(size)+"_attempts"+str(attempts)+".png")

