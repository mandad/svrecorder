"""
Time series data plotter for surface sound speed data

Damian Manda
damian.manda@noaa.gov
5 March 2013
"""

import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class SSPData(object):
    def __init__(time_arr, ssp_arr):
        self.time_arr = time_arr
        self.ssp_arr = ssp_arr

def plot_data(SV70_file, digibar_file):
    try:
        sv_data1 = matplotlib.mlab.csv2rec(SV70_file, delimiter=',')
        sv_data2 = matplotlib.mlab.csv2rec(digibar_file)
    except Exception as e:
        print "Input file could not be read: ", e
        raise SystemExit(1)

    #extract what we need
    time1 = sv_data1['time']
    SSP1 = sv_data1['ssp']
    SSP1 = np.ma.masked_outside(SSP1, 1472, 1485)
    time2 = sv_data2['time']
    SSP2 = sv_data2['ssp']
    SSP2 = np.ma.masked_outside(SSP2, 1472, 1485)
    plt.plot(time1, SSP1, label='SV70')
    plt.hold(True)
    plt.plot(time2, SSP2, 'r', label='Digibar')
    plt.ylim([1476,1485])
    plt.ylabel('Sound Speed (m/s)')
    plt.axes().get_yaxis().set_major_formatter(
        matplotlib.ticker.FormatStrFormatter('%i'))
    plt.xlabel('Time (sec since 1/1/1970)')
    plt.title('Comparison of Sound Speed Sensor Readings')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    """Arguments when run from the command line are:
    SV70file.txt DigibarFile.txt
    """
    plot_data(sys.argv[1], sys.argv[2])
