import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class SSPData(object):
    def __init__(time_arr, ssp_arr):
        self.time_arr = time_arr
        self.ssp_arr = ssp_arr


def read_data(filename):
    try:
        data = matplotlib.mlab.csv2rec(filename)
    except Exception as e:
        print "Input file could not be read: ", e
        raise SystemExit(1)
    return (data['time'], data['ssp'])


def main():
    try:
        sv_data1 = matplotlib.mlab.csv2rec(sys.argv[1], delimiter=',')
        sv_data2 = matplotlib.mlab.csv2rec(sys.argv[2])
    except Exception as e:
        print "Input file could not be read: ", e
        raise SystemExit(1)

    #extract what we need
    time1 = sv_data1['time']
    SSP1 = sv_data1['ssp']
    SSP1 = np.ma.masked_outside(SSP1, 1470, 1485)
    time2 = sv_data2['time']
    SSP2 = sv_data2['ssp']
    SSP2 = np.ma.masked_outside(SSP2, 1470, 1485)
    plt.plot(time1, SSP1, label='SV71')
    plt.hold(True)
    plt.plot(time2, SSP2, 'r', label='Digibar')
    plt.ylim([1470,1485])
    plt.ylabel('Sound Speed (m/s)')
    plt.xlabel('Time (sec since 1/1/1970)')
    plt.title('Comparison of Sound Speed Sensor Readings')
    plt.legend()
    plt.show()

if __name__ == '__main__':
	main()