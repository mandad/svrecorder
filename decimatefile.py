import sys
import sv_recorded_process
import numpy as np
import time

_debug = False

def decimate(filename):
    """Reads an SVP71 record file and outputs one mean value for each second
    along with the stdev for that second.  Writes output to 
    inputfilename_dec.txt

    Automatically interprets files ending with .log to be digibar recordings
    otherwise, assumed to be SV71 in svrecorder.py output format
    """
    print 'Decimating file:' + filename

    if filename[-3:] == 'log':
        readfile = sv_recorded_process.DigibarFile(filename)
    else:
        readfile = sv_recorded_process.SV71File(filename)
    try:
        writefile = open(filename[:-4] + '_dec.txt', 'w+')
        writefile.write('Time,SSP,StDev\n')
    except IOError as e:
        print e

    num_in = 0
    num_out = 0
    lastsec = 0
    sv_vals = np.zeros(1)
    for sv_record in readfile:
        sec = int(sv_record.epoch_time // 1)
        if sec == lastsec:
            sv_vals = np.append(sv_vals, sv_record.sv_value)
        else:
            if lastsec != 0:
                if _debug:
                    print ('Sec: %i, SV: %0.2f, Std: %0.2f\n' % (lastsec, 
                        np.mean(sv_vals), np.std(sv_vals)))
                else:
                    writefile.write('{0:d},{1:0.2f},{2:0.2f}\n'.format(lastsec, 
                        np.mean(sv_vals), np.std(sv_vals)))
                num_out += 1
            lastsec = sec
            sv_vals = np.array([sv_record.sv_value])
        num_in += 1
        if _debug:
            if num_in == 10:
                break

    #print last record
    if _debug:
        print ('Sec: %i, SV: %0.2f, Std: %0.2f' % (lastsec, 
            np.mean(sv_vals), np.std(sv_vals)))
        print "Last Record: "
        sv_record.print_info()
    else:
        writefile.write('{0:d},{1:0.2f},{2:0.2f}'.format(lastsec, 
            np.mean(sv_vals), np.std(sv_vals)))
    num_out += 1
    writefile.close()
    print '%i Records Processed, %i Output' % (num_in, num_out) 
    # Return the name of the output file so that other processing can be done
    return filename[:-4] + '_dec.txt'

if __name__ == '__main__':
    """Command Line Parameter: filename_to_process
    """
    decimate(sys.argv[1])
