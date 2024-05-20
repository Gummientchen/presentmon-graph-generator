import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse
import os
from pathlib import Path

# Defaults
inputFilename = "input.csv"

msg = "Parses a PresentMon log and creates graphs"

parser = argparse.ArgumentParser(description = msg)
parser.add_argument("-i", "--Input", help = "Input File Path", required=True)
parser.add_argument("-o", "--Output", help = "Output File Path (.png). Default generated by log.")
parser.add_argument("-t", "--Title", help = "Graph title shown at the top of generated image.")
parser.add_argument("-b", "--Bins", help = "How many bins should be used for histograms. Default 20", default=20, type=int)
args = parser.parse_args()

if args.Input:
    inputFilename = args.Input

n_bins = args.Bins


def main():
    print("loading input file...")
    logs = pd.read_csv(inputFilename)
    
    applicationName = logs["Application"][0]
    applicationName = applicationName.replace(".exe", "")
    processId = logs["ProcessID"][0]
    
    # auto generate output if not specified
    if args.Output:
        outputFilename = args.Output
    else:
        outputFilename = Path(inputFilename).stem + ".png"
        # outputFilename = applicationName + "_" + str(processId) + ".png"
        inputDir = os.path.dirname(os.path.abspath(inputFilename))
        outputFilename = os.path.join(inputDir, outputFilename)
    
    print("generating graphs...")
    fig = plt.figure(tight_layout=True)
    
    
    fig.set_size_inches(420/25.4, 320/25.4)
    
    if args.Title:
        fig.suptitle(args.Title)
    else:
        fig.suptitle("PresentMon - "+applicationName+" - PID:"+str(processId), fontsize=16)
    
    
    
    fig.canvas.manager.set_window_title('PresentMon - Results')
    
    gs = fig.add_gridspec(5,2, height_ratios=[1.5, 1, 1, 0.5, 0.5])
    
    avgFps = round(1000/logs["FrameTime"].mean(), 1)
    avgFps999 = round(1000/logs["FrameTime"].quantile(0.999).mean(), 1)
    avgFps99 = round(1000/logs["FrameTime"].quantile(0.99).mean(), 1)
    avgFps95 = round(1000/logs["FrameTime"].quantile(0.95).mean(), 1)
    
    axsFrametime = fig.add_subplot(gs[0, :])
    axsFrametime.set_title("FrameTime")
    axsFrametime.set_xlabel("frames")
    axsFrametime.set_ylabel("ms")
    axsFrametime.plot(logs["FrameTime"], linewidth=0.25, label="raw")
    axsFrametime.plot(movingaverage(logs["FrameTime"], 50), linewidth=1, alpha=0.8, label="average")
    axsFrametime.legend(loc='upper right')
    axsFrametime.text(0.01, 0.95,
                      "Average:\n5% lows:\n1% lows:\n0.1% lows:",
                      fontsize=12, horizontalalignment='left', verticalalignment='top', transform=axsFrametime.transAxes)
    axsFrametime.text(0.15, 0.95,
                      str(avgFps)+" fps\n"+str(avgFps95)+" fps\n"+str(avgFps99)+" fps\n"+str(avgFps999)+" fps",
                      fontsize=12, horizontalalignment='right', verticalalignment='top', transform=axsFrametime.transAxes)
    
    axsCPUBusyHistogram = fig.add_subplot(gs[1:3, 0])
    axsCPUBusyHistogram.set_title("CPU/GPU Busy Histogram")
    axsCPUBusyHistogram.set_xlabel("ms")
    axsCPUBusyHistogram.set_ylabel("frames")
    axsCPUBusyHistogram.hist(logs["CPUBusy"], bins=n_bins, rwidth=0.9, label="CPUBusy", log=True)
    axsCPUBusyHistogram.hist(logs["GPUBusy"], bins=n_bins, rwidth=0.9, label="GPUBusy", alpha=0.75, log=True)
    axsCPUBusyHistogram.legend(loc='upper right')
    
    # axsGPUBusyHistogram = fig.add_subplot(gs[2, 0])
    # axsGPUBusyHistogram.set_title("GPUBusy Histogram")
    # axsGPUBusyHistogram.set_xlabel("ms")
    # axsGPUBusyHistogram.set_ylabel("frames")
    # axsGPUBusyHistogram.hist(logs["GPUBusy"], bins=n_bins, rwidth=0.9)
    # axsGPUBusyHistogram.sharex(axsCPUBusyHistogram)
    
    axsFrametimeHistogram = fig.add_subplot(gs[1, 1])
    axsFrametimeHistogram.set_title("FrameTime Histogram")
    axsFrametimeHistogram.set_xlabel("ms")
    axsFrametimeHistogram.set_ylabel("frames")
    axsFrametimeHistogram.hist(logs["FrameTime"], bins=n_bins, rwidth=0.9, log=True)
    
    axsClickToPhoton = fig.add_subplot(gs[2, 1])
    axsClickToPhoton.set_title("Click-to-Photon Latency")
    axsClickToPhoton.set_xlabel("frames")
    axsClickToPhoton.set_ylabel("ms")
    axsClickToPhoton.plot(logs["ClickToPhotonLatency"], "+")
    
    axsClickToPhoton = fig.add_subplot(gs[3, :])
    axsClickToPhoton.set_title("GPUPower/GPUTemperature")
    axsClickToPhoton.set_xlabel("frames")
    axsClickToPhoton.set_ylabel("Watt")
    axsClickToPhoton.plot(logs["GPUPower"], linewidth=1, color="orange", label="Power")
    axsClickToPhoton.legend(loc='upper left')
    
    tempaxs = axsClickToPhoton.twinx()
    tempaxs.set_ylabel("°C")
    tempaxs.plot(logs["GPUTemperature"], linewidth=1, color="red", label="Temperature")
    tempaxs.legend(loc='upper right')
    
    
    axsCpuUtilization = fig.add_subplot(gs[4, :])
    axsCpuUtilization.set_title("CPU/GPU Utilization")
    axsCpuUtilization.set_xlabel("frames")
    axsCpuUtilization.set_ylabel("%")
    axsCpuUtilization.plot(logs["CPUUtilization"], linewidth=1, label="CPU")
    axsCpuUtilization.plot(logs["GPUUtilization"], linewidth=1, label="GPU")
    # axsCpuUtilization.legend(loc='upper center', bbox_to_anchor=(1, 2))
    axsCpuUtilization.legend(loc='upper right')
    
    # add some basic data
    # fig.figte
    
    print("saving graphs...")
    plt.savefig(outputFilename)
            
    plt.show()
    
    # print(logs.columns)
    print("All Done!")
    

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'valid')

if __name__ == "__main__":
    main()