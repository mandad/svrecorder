import sys
import numpy as np
import scipy
import matplotlib.pyplot as plt

import plotdata

def show_hist(filename):
    data = np.load(filename)
    plt.hist(data['diffs'], bins = 100, range=(-5,5))
    plt.xlabel('SV71 - Digibar (m/s)')
    plt.show()

def correlate_data():
    """Correlate two datasets that span a common time range but do not have the
    same indicies for corresponding times.  Output arrays of points where times
    match and calculate the difference between the two arrays.  Optionally saves
    to a .npz file for further analysis.

    Command Line Parameters: sv71_file digibar_file [save_file]
    """
    sv71 = plotdata.read_data(sys.argv[1])
    digibar = plotdata.read_data(sys.argv[2])

    sv71_dict = dict(zip(sv71[0], sv71[1]))
    digibar_dict = dict(zip(digibar[0], digibar[1]))

    first_run = True

    # Run through the times and match up records
    for time in sv71_dict:
        if digibar_dict.has_key(time):
            if first_run:
                times = np.array([time])
                sv71_val = np.array([sv71_dict[time]])
                digibar_val = np.array([digibar_dict[time]])
                first_run = False
            else:
                times = np.append(times, time)
                sv71_val = np.append(sv71_val, sv71_dict[time])
                digibar_val = np.append(digibar_val, digibar_dict[time])

    diffs = sv71_val - digibar_val
    print 'Mean Diff: %0.4f\nStDev Diff: %0.4f' % (np.mean(diffs),
        np.std(diffs))

    if len(sys.argv) == 4:
        np.savez(sys.argv[3], times=times, diffs=diffs, sv71=sv71_val,
         digibar=digibar_val)
        print "Data saved to file: " + sys.argv[3]


if __name__ == '__main__':
    if sys.argv[1] == '-g':
        show_hist(sys.argv[2])
    else:
        correlate_data()