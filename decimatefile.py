import sys
import sv_recorded_process
import numpy as np

_debug = True

def main():
    """Reads an SVP71 record file and outputs one mean value for each second
    along with the stdev for that second.  Writes output to 
    inputfilename_dec.txt
    """
    if sys.argv[1][-3:] == 'log':
        readfile = sv_recorded_process.DigibarFile(sys.argv[1])
    else:
        readfile = sv_recorded_process.SV71File(sys.argv[1])
    try:
        writefile = open(sys.argv[1][:-4] + '_dec.txt', 'w+')
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
                    print ('Sec: %i, SV: %0.2f, Std: %0.2f' % (lastsec, 
                        np.mean(sv_vals), np.std(sv_vals)))
                else:
                    writefile.write('{0:d},{1:0.2f},{2:0.2f}\n'.format(lastsec, 
                        np.mean(sv_vals), np.std(sv_vals)))
                num_out += 1
            lastsec = sec
            sv_vals = np.array([sv_record.sv_value])
        num_in += 1
        if _debug:
            if i == 50:
                break

    #print last record
    if _debug:
        print ('Sec: %i, SV: %0.2f, Std: %0.2f' % (lastsec, 
            np.mean(sv_vals), np.std(sv_vals)))
    writefile.write('{0:d},{1:0.2f},{2:0.2f}'.format(lastsec, 
        np.mean(sv_vals), np.std(sv_vals)))
    writefile.close()
    print '%i Records Processed, %i Output' % (num_in, num_out)

if __name__ == '__main__':
    main()