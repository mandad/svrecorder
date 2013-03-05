"""
Serial Data Recorder for SVP71
Records data to a file and timestamps it using UTC time.

Damian Manda
damian.manda@noaa.gov
26 Feb 2013
"""


import sys
import os
import time
import serial

class SSPSerial:
    def __init__(self, filename='svrecord.txt'):
        """Open a file for output and set up the serial port but don't open it.
        """
        print 'Opening Serial Port'
        self.ser = serial.Serial()
        self.ser.port = 'COM1'
        self.ser.timeout = 5
        print os.getcwd()
        self.write_append = os.path.exists(filename)
        try:
            if self.write_append:
                self.outfile = open(filename, 'a+')
            else:
                self.outfile = open(filename, 'w')
                self.outfile.write('Time,Seconds,SSP\n')
        except Exception:
            print 'Error opening file %s' % filename

    def start_read(self):
        """Start the reading cycle""" 
        try:
            self.ser.open()
            while True:
                try:
                    line = self.ser.readline()
                    print 'SV= ' + line[1:8]
                    curtime = time.time() # + time.timezone
                    i, f = divmod(curtime,i 1)
                    ftime = '%0.2f' %  f
                    self.outfile.write(time.strftime('%Y %j %H %M %S', 
                        time.gmtime(curtime)) + ftime[1:] + ',' + 
                        '%0.2f' % curtime + ',' + line[1:8] + '\n')
                    self.outfile.flush()
                except serial.SerialTimeoutException:
                    print 'No serial communication detected'
                    self.stop_read()
                    break
                except KeyboardInterrupt:
                    self.stop_read()
                    break
                except IOError:
                    print 'Error writing to file'
                    self.stop_read()
                    break
                except Exception:
                    pass
        except serial.SerialException:
            print 'Serial Port could not be opened'   

    def stop_read(self):
        self.outfile.close()
        if self.ser.isOpen():
            self.ser.close()

def main():
    if len(sys.argv) > 1:
        ssp = SSPSerial(sys.argv[1])
    else:
        ssp = SSPSerial()
    if ssp.outfile is not None:
        ssp.start_read()

if __name__ == '__main__':
    main()