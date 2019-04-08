# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Read and Plotting file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Imports
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import matplotlib.pyplot as plot
import Globals as gl

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# reads a generic column seperated file, reaturns array of data arrays (same order as file)
def readColumnFile(filename, header=0):
	file = open(filename,'r')
	# skips the header
	for i in range(header):
		file.readline()
	#start reading data
	currentLine = file.readline()

	# checks how many columns are in the data set
	if currentLine != "" or "\n":
		allData = []
		for i in range(len(currentLine.split())):
			allData.append([])

	# reads data into the array of data arrays
	while currentLine != "":
		if currentLine != "\n": # the final line is empty and would break if split is called
			theLine = currentLine.split()
			for i in range(len(theLine)):
				allData[i].append(float(theLine[i]))
		currentLine = file.readline()
	file.close()
	return allData

# writes a generic column separated file, each sub array of data must be same length
def writeColumnFile(filename, data, header=None):
	f = open(filename,"w+")
	f.write(str(header)+"\n")
	# loop through length of data sub array
	for i in range(len(data[0])):
		# loop through data array
		for subArray in data:
			f.write(str(subArray[i])+"\t")
		f.write("\n")
	f.close()

# note plotInit returns ax, the axis that holds the legend - need to pass this to plotData to make legend work
# chose linear or log scale and limits for x and y axes
def plotInit(xAx=r"Xs [unitless]", yAx=r"Ys [unitless]",plotTitle=r"Default Title", grid=True, log=False, xLimits=None, yLimits=None):
	plot.clf()
	ax = plot.subplot(111)
	box = ax.get_position()
	ax.set_position([box.x0, box.y0, box.width*0.8, box.height])
	
	if grid:
		plot.grid()
	if log:
		plot.yscale('log')
		plot.xscale('log')
	
	if xLimits != None:
		plot.xlim(xLimits[0],xLimits[1])
	if yLimits!= None:
		plot.ylim(yLimits[0],yLimits[1])
	
	plot.xlabel(xAx)
	plot.ylabel(yAx)
	plot.title(plotTitle)
	return ax

# call for as much data as you want
# don't forget to pass ax from plotInit() to make the legend work!
def plotData(ax, dXs, dYs, eXs=0, eYs=0, dataLabel=r"default", colour="Blue", lines=False):
	plot.errorbar(dXs, dYs, xerr=eXs, yerr=eYs, ecolor=colour, fmt='none', elinewidth=0.3)
	if lines:
		plot.plot(dXs, dYs, label=dataLabel, color=colour, marker='', linestyle='-', linewidth=0.8)
	else:
		plot.plot(dXs, dYs, label=dataLabel, color=colour, marker='.', linestyle='', markersize=0.8)
	ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# plots a 2D image
# dataArray is a 2D array with valued entries, this informs the colour scale
# see all maps here: https://matplotlib.org/gallery/color/colormap_reference.html
def plot2D(ax, dataArray, colourmap=None, dataLabel=r"default"):
	plot.imshow(dataArray, cmap=colourmap, label=dataLabel)
	plot.colorbar()

# call once to show the plot
def plotOutput(savefigname=None,resolution=500):
	if savefigname != None:
		plot.savefig(savefigname, dpi=resolution, bbox_inches="tight")
	else:
		plot.show()