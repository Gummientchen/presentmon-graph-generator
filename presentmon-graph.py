import matplotlib.pyplot as plt
import matplotlib.backends.backend_cairo
import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path
from matplotlib import use as mpluse

mpluse("Cairo")
pd.options.mode.copy_on_write = True

# Defaults
inputFilename = "input.csv"

msg = "Parses a PresentMon log and creates graphs"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--Input", help = "Input File Path", required=True)
parser.add_argument("-o", "--Output", help = "Output File Path (.png). Default generated by log.")
parser.add_argument("-t", "--Title", help = "Graph title shown at the top of generated image.")
parser.add_argument("-b", "--Bins", help = "How many bins should be used for histograms. Default 20", default=20, type=int)
parser.add_argument("-d", "--Theme", help = "Switch between light and dark mode. Default 'dark'", choices=['dark', 'light'], default="dark")
parser.add_argument("-p", "--Pdf", help = "Exports the graph as a .pdf too", action='store_true')
parser.add_argument("-v", "--Svg", help = "Exports the graph as a .svg too", action='store_true')
args = parser.parse_args()

if args.Input:
    inputFilename = args.Input

n_bins = args.Bins

# Colors
color = {}

if args.Theme and args.Theme == "light":
    # light colors
    color['background'] = '#FFF'
    color['backgroundLegend'] = '#FFF'
    color['text'] = '#000'
    color['lines'] = '#000'
    color['lightplot'] = '#000'
else:
    # dark colors
    color['background'] = '#0d1324'
    color['backgroundLegend'] = '#252e47'
    color['text'] = '#dbebf7'
    color['lines'] = '#89b8ef'
    color['lightplot'] = '#c3d4e2'


def main():
    print("loading input file...")
    logs = pd.read_csv(inputFilename, usecols=['Application','ProcessID','FrameTime','CPUBusy','GPUBusy','ClickToPhotonLatency','GPUTemperature','GPUUtilization','CPUUtilization','GPUPower'])
    
    applicationName = logs["Application"][0]
    applicationName = applicationName.replace(".exe", "")
    processId = logs["ProcessID"][0]
    
    
    # auto generate output if not specified
    if args.Output:
        outputFilename = args.Output
        outputDir = os.path.dirname(os.path.abspath(outputFilename))
    else:
        outputFilename = Path(inputFilename).stem + ".png"
        outputDir = os.path.dirname(os.path.abspath(inputFilename))
        
        
    outputFilenamePdf = Path(outputFilename).stem + ".pdf"
    outputFilenameSvg = Path(outputFilename).stem + ".svg"
    outputFilenamePdf = os.path.join(outputDir, outputFilenamePdf)
    outputFilenameSvg = os.path.join(outputDir, outputFilenameSvg)
    outputFilename = os.path.join(outputDir, outputFilename)
    
    
    # start graph generation
    print("generating graphs...")
    fig = plt.figure(tight_layout=True)
    
    fig.patch.set_facecolor(color["background"])
    fig.set_size_inches(420/25.4, 280/25.4)
    
    # Set colors
    plt.rcParams['axes.facecolor'] = color['background']
    plt.rcParams['text.color'] = color['text']
    plt.rcParams['axes.labelcolor'] = color['text']
    plt.rcParams['xtick.color'] = color['lines']
    plt.rcParams['ytick.color'] = color['lines']
    plt.rcParams['lines.color'] = color['lines']
    plt.rcParams['axes.edgecolor'] = color['lines']
    plt.rcParams['legend.facecolor'] = color['backgroundLegend']
    plt.rcParams['axes.titleweight'] = 500
    
    # Set title
    if args.Title:
        suptitle = args.Title
    else:
        suptitle = "PresentMon - "+applicationName+" - PID:"+str(processId)
        
    fig.suptitle(suptitle, fontsize=16, horizontalalignment="left", x=0.0435)
    
    fig.canvas.manager.set_window_title('PresentMon - Results')
    
    gs = fig.add_gridspec(6,2, height_ratios=[0.5, 1.5, 1, 1, 0.5, 0.5])
    
    # calculate stats
    numberOfFrames = len(logs.index)
    smoothness = getSmoothness(logs)
    maxFps = getMaxFps(logs)
    minFps = getMinFps(logs)
    avgFps = round(1000/logs["FrameTime"].mean(), 1)
    avgFps999 = round(1000/logs["FrameTime"].quantile(0.999).mean(), 1)
    avgFps99 = round(1000/logs["FrameTime"].quantile(0.99).mean(), 1)
    avgFps95 = round(1000/logs["FrameTime"].quantile(0.95).mean(), 1)
    gpuMaxPower = getMaxPower(logs)
    gpuMinPower = getMinPower(logs)
    gpuAveragePower = getAveragePower(logs)
    
    # Special empty fig for some general statistics in text form
    axsInformation = fig.add_subplot(gs[0, :])
    axsInformation.axis('off')
    axsInformation.set_title("\nInformation", loc='left')
    
    statsOffset = -0.055
    axsInformation.text(0.0, 0.95,
                      "Frames:\nSmoothness:\nMax FPS:\nMin FPS:",
                      fontsize=10, horizontalalignment='left', verticalalignment='top', transform=axsInformation.transAxes)
    axsInformation.text(0.1975+statsOffset, 0.95,
                      str("{:1.0f}".format(numberOfFrames))+" frames",
                      fontsize=10, horizontalalignment='right', verticalalignment='top', transform=axsInformation.transAxes)
    axsInformation.text(0.1625+statsOffset, 0.95,
                      "\n"+str("{:1.1f}".format(smoothness)),
                      fontsize=10, horizontalalignment='right', verticalalignment='top', transform=axsInformation.transAxes)
    axsInformation.text(0.179+statsOffset, 0.95,
                      "\n\n"+str("{:1.1f}".format(maxFps))+" fps\n"+str("{:1.1f}".format(minFps))+" fps",
                      fontsize=10, horizontalalignment='right', verticalalignment='top', transform=axsInformation.transAxes)
    
    statsOffset = -0.03
    axsInformation.text(0.25+statsOffset, 0.95,
                      "Average:\n5% lows:\n1% lows:\n0.1% lows:",
                      fontsize=10, horizontalalignment='left', verticalalignment='top', transform=axsInformation.transAxes)
    statsOffset = -0.06
    axsInformation.text(0.4+statsOffset, 0.95,
                      str("{:4.1f}".format(avgFps))+" fps\n"+str("{:4.1f}".format(avgFps95))+" fps\n"+str("{:4.1f}".format(avgFps99))+" fps\n"+str("{:4.1f}".format(avgFps999))+" fps",
                      fontsize=10, horizontalalignment='right', verticalalignment='top', transform=axsInformation.transAxes)
    
    statsOffset = 0
    axsInformation.text(0.42+statsOffset, 0.95,
                      "GPU Max Power:\nGPU Min Power:\nGPU Average Power:",
                      fontsize=10, horizontalalignment='left', verticalalignment='top', transform=axsInformation.transAxes)
    statsOffset = 0
    axsInformation.text(0.57+statsOffset, 0.95,
                      str("{:4.1f}".format(gpuMaxPower))+" W\n"+str("{:4.1f}".format(gpuMinPower))+" W\n"+str("{:4.1f}".format(gpuAveragePower))+" W",
                      fontsize=10, horizontalalignment='right', verticalalignment='top', transform=axsInformation.transAxes)
    
    # create graphs
    axsFrametime = fig.add_subplot(gs[1, :])
    axsFrametime.set_title("FrameTime", loc='left')
    axsFrametime.set_xlabel("frames")
    axsFrametime.set_ylabel("ms")
    axsFrametime.plot(logs["FrameTime"], linewidth=0.25, label="raw")
    axsFrametime.plot(movingaverage(logs["FrameTime"], 50), linewidth=1, alpha=0.8, label="average")
    axsFrametime.legend(loc='upper right')
    
    axsCPUBusyHistogram = fig.add_subplot(gs[2:4, 0])
    axsCPUBusyHistogram.set_title("CPU/GPU Busy Histogram", loc='left')
    axsCPUBusyHistogram.set_xlabel("ms")
    axsCPUBusyHistogram.set_ylabel("frames")
    axsCPUBusyHistogram.hist(logs["CPUBusy"], bins=n_bins, rwidth=0.9, label="CPUBusy", log=True)
    axsCPUBusyHistogram.hist(logs["GPUBusy"], bins=n_bins, rwidth=0.9, label="GPUBusy", alpha=0.75, log=True)
    axsCPUBusyHistogram.legend(loc='upper right')
    
    axsFrametimeHistogram = fig.add_subplot(gs[2, 1])
    axsFrametimeHistogram.set_title("FrameTime Histogram", loc='left')
    axsFrametimeHistogram.set_xlabel("ms")
    axsFrametimeHistogram.set_ylabel("frames")
    axsFrametimeHistogram.hist(logs["FrameTime"], bins=n_bins, rwidth=0.9, log=True)
    
    axsClickToPhoton = fig.add_subplot(gs[3, 1])
    axsClickToPhoton.set_title("Click-to-Photon Latency", loc='left')
    axsClickToPhoton.set_xlabel("frames")
    axsClickToPhoton.set_ylabel("ms")
    axsClickToPhoton.plot(logs["ClickToPhotonLatency"], "+", color=color['lightplot'])
    
    axsGPUPower = fig.add_subplot(gs[4, :])
    axsGPUPower.set_title("GPUPower/GPUTemperature", loc='left')
    axsGPUPower.set_xlabel("frames")
    axsGPUPower.set_ylabel("Watt")
    axsGPUPower.plot(logs["GPUPower"], linewidth=1, color="orange", label="Power")
    axsGPUPower.legend(loc='upper left')
    tempaxs = axsGPUPower.twinx()
    tempaxs.set_ylabel("°C")
    tempaxs.plot(logs["GPUTemperature"], linewidth=1, color="red", label="Temperature")
    tempaxs.legend(loc='upper right')
    
    axsCpuUtilization = fig.add_subplot(gs[5, :])
    axsCpuUtilization.set_title("CPU/GPU Utilization", loc='left')
    axsCpuUtilization.set_xlabel("frames")
    axsCpuUtilization.set_ylabel("%")
    axsCpuUtilization.plot(logs["CPUUtilization"], linewidth=1, label="CPU")
    axsCpuUtilization.plot(logs["GPUUtilization"], linewidth=1, label="GPU")
    axsCpuUtilization.legend(loc='upper right')
    
    # save
    print("saving graphs...")
    plt.savefig(outputFilename)
    
    if args.Pdf:
        plt.savefig(outputFilenamePdf)
    
    if args.Svg:   
        plt.savefig(outputFilenameSvg)
          
    print("All Done!")
    
    
def getMaxFps(log):
    return 1000/log["FrameTime"].min()


def getMinFps(log):
    return 1000/log["FrameTime"].max()


def getMaxPower(log):
    return log["GPUPower"].max()

def getMinPower(log):
    return log["GPUPower"].min()

def getAveragePower(log):
    return log.loc[:, "GPUPower"].mean()


# calculates the smoothness factor
def getSmoothness(log):
    print("calculating smoothness factor...")
    log = log.reset_index()
    framecount = len(log.index)
    
    log['difference'] = log["FrameTime"]/log["FrameTime"].shift(1, fill_value=-1)
    log.loc[0, "difference"] = 0
    log['abs_difference'] = log.apply(calcAbsDifference, axis=1)
    log.loc[0, "abs_difference"] = 0
    
    differences = log['abs_difference'].sum()
    
    smoothness = (1 - differences / framecount)*100
    return smoothness
    
    
# pandas apply function to get absolute difference between two frames
def calcAbsDifference(row):
    if row["difference"] < 1:
        abs_difference = 1-row["difference"]
    else:
        abs_difference = row["difference"]-1
    
    return abs_difference


# calculcate moving avarage for frametime
def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'valid')


if __name__ == "__main__":
    main()