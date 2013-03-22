"""
Runs through the whole decimation and correlation process with two raw
recorded sound speed files from the SV70 and Digibar.

run with:
fullprocess.py SV70_file.txt Digibar_file.log output.npz

Damian Manda
damian.manda@noaa.gov
22 March 2013
"""

import sys
import decimatefile
import correlation
import plotdata

def show_all_plots(SV70_file, digibar_file, correlate_file):
    plotdata.plot_data(SV70_file, digibar_file)
    correlation.show_hist(correlate_file)
    correlation.show_diff_timeseries(correlate_file)

def main():
    if len(sys.argv) == 4:
        deci_sv70 = decimatefile.decimate(sys.argv[1])
        deci_digibar = decimatefile.decimate(sys.argv[2])
        correlation.correlate_data(deci_sv70, deci_digibar, sys.argv[3])
        show_all_plots(deci_sv70, deci_digibar, sys.argv[3])

if __name__ == '__main__':
    if len(sys.argv) == 4
        main()
    elif len(sys.argv) == 5:
        show_all_plots(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print 'ERROR - Incorrect number of parameters.'
        print 'Correct arguments are:'
        print 'SV70_file.txt Digibar_file.log output.npz'
        