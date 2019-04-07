# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Animating Plots file
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import numpy as np
import matplotlib.pyplot as plot
import matplotlib.animation as ani
import ReadAndPlot as rp
if verbose:
    import time

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# put functions here
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# test function to initalize test animation
# this is called at animation start up (so what the first frame looks like)
# when making a new one keep this same formatting (no parameters, just return rp.plotinit)
def testInit():
    return rp.plotInit(plotTitle="Test animation of exponential decay",xLimits=[0,10], yLimits=[-0.1,1.1])

# test tunction that gets data every frame, and plots it
# this command is executed every animation step, so do stuff like grabbing new dataa and plotting here
# when making a new one keep formatting (the data as the only parameter, plotting data, don't need plot output though)
def testRun(data):
    ax = rp.plotInit(plotTitle="Test animation of exponential decay",xLimits=[0,10], yLimits=[-0.1,1.1])
    rp.plotData(ax, data[0], data[1], dataLabel=r"$y=e^{-x}$")

# test function that outputs a set of x and y data points
# this is called every frame with currentTime being updated
# currentTime is the current index of timeArray, which is an array of every time step the animation will undergo
# when making a new one, keep formatting ((timeArray,currentTime,extraParams), )
def testDataFunction(timeArray, currentTime):
    Xs = [timeArray[i] for i in range(currentTime)]
    Ys = [np.exp(-timeArray[i]) for i in range(currentTime)]
    return Xs, Ys

# generator for data to plot
# don't make a new one, let animate use this
def genFunc(timeArray, dataFunction, dataFuncParams):
    t = 0
    while t < len(timeArray):
        if verbose:
            if t%25 == 0:
                print("\nOn step "+str(t)+" of "+str(len(timeArray))+"\t"+'{0:.1f}'.format(100*t/len(timeArray))+"% complete\n"+'{0:.1f}'.format(time.process_time()/60/60)+" minutes elapsed\t"+'{0:.1f}'.format(time.process_time()*(len(timeArray)/(t+0.1) - 1)/60/60)+" hours remain")
        yield dataFunction(timeArray, t, *dataFuncParams)
        t += 1

# this is the main function used to create animations
# dataFunc is the function used to construct new data for each frame
# dataFuncParams is the set of parameters after the first two: (timeArray, currentTime, *dataFuncParams)
# timeArray is an array of each time step in the animation (np.linspace gives you choice of time range and number of frames)
# frametime tells how long to display each frame during live playback (does not effect saved playback)
# initFunc is the function called once at the begining of the animation
# runningFunc is the function called every frame, its only parameter is the return value of the dataFunc
def animate(dataFunc=testDataFunction, dataFuncParams=[], timeArray=np.linspace(0,12,100), frameTime=30, initFunc=testInit, runningFunc=testRun):
    if not isinstance(dataFuncParams, list):
        raise ValueError("dataFuncParams must be a list (even if it is just a single entry, eg. dataFuncParams=[alpha])")
    return ani.FuncAnimation(plot.figure(), runningFunc, genFunc(timeArray,dataFunc,dataFuncParams), interval=frameTime, init_func=initFunc, save_count=len(timeArray))

# outputs the animation
# if no savefigname is None, then displays the animation live
# with a name it saves with:
    # framerate: the playback fps (mocies run at 24 or 30, games run at 60)
    # resolution: the individual frames' ppi
    # bitrate: the number of bits per second the video can store (higher=less artifacting, larger file size)
def aniOutput(myAnimation, savefigname=None, framerate=30, resolution=500, bitrate=None):
    if savefigname == None:
        plot.show()
    else:
        myAnimation.save(filename=savefigname, fps=framerate, dpi=resolution, bitrate=bitrate)

# test animation
# to save as mp4 file, you'll need FFmpeg installed and added to your Path:
# install guide for windows10: https://www.wikihow.com/Install-FFmpeg-on-Windows
# link to FFmpeg: https://ffmpeg.zeranoe.com/builds/

#a=animate()
#aniOutput(a)
#aniOutput(a,savefigname="Animations/testanimation.mp4")