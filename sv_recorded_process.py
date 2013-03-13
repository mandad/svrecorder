import os
import time
import datetime


class SerialFile(object):
    """Class used for reading serial svp record files, inheriting classes
    implement actual decoding details
    """
    def __init__(self, filename):
        try:
            self.file = open(filename, 'r')
        except IOError:
            print 'Error reading file: ' + filename

    def __del__(self):
        if not self.file.closed:
            self.file.close()

class SV71File(SerialFile):
    """Reads a serial file written by the svrecorder.py script, uses a general
    form for compatibility with other formats.
    """
    def __init__(self, filename):
        super(SV71File, self).__init__(filename)
        #skip the line with the header, could use this to verify file too
        self.file.readline()

    def __del__(self):
        super(SV71File, self).__del__()

    def __iter__(self):
        return self

    def next(self):
        """Return a SVPInfo object representing the next record read from the 
        file.
        """
        if not self.file.closed:
            #Keep trying until a valid line is read or EOF reached
            while True:
                line_text = self.file.readline()
                parts = line_text.split(',')
                if len(parts) == 3:
                    try:
                        return SVPInfo(float(parts[1]), float(parts[2]))
                    except:
                        #Incomplete line that can't be converted to float
                        print "Invalid Record Skipped: " + line_text[:-1]
                else:
                    self.file.close()
                    raise StopIteration
        else:
            raise StopIteration

class DigibarFile(SerialFile):
    """Reads a file of raw strings from a digibar, uses same interface as SV71
    reader for compatibility.
    """
    def __init__(self, filename):
        super(DigibarFile, self).__init__(filename)
        #first 3 lines are a header
        for i in range(3):
            self.file.readline()

    def __del__(self):
        super(DigibarFile, self).__del__()

    def __iter__(self):
        return self

    def next(self):
        if not self.file.closed:
            line_text = self.file.readline()
            parts = line_text.split(',')
            if len(parts) == 5:
                fulltime = ' '.join(parts[0:2])
                localtime = time.strptime(fulltime, r'%m/%d/%y %H:%M:%S')
                epochtime = time.mktime(time.strptime(fulltime, 
                    r'%m/%d/%y %H:%M:%S'))
                # if time set incorrectly
                # epochtime += 3600 * 10
                # print time.localtime(epochtime)
                try:
                    return SVPInfo(float(epochtime), float(parts[2]))
                except:
                    raise StopIteration
            else:
                self.file.close()
                raise StopIteration
        else:
            raise StopIteration

class SVPInfo(object):
    """Class for storing SVP records, keeps track of time of the record and the
    sound speed value.
    """
    def __init__(self, time_rec, sv_value):
        #time_rec is expecteed to be in UTC, seconds since epoch
        self.epoch_time = time_rec
        self.sv_value = sv_value

    @property
    def year(self):
        return time.strftime('%Y', time.gmtime(self.epoch_time))
    @property
    def utc_datetime(self):
        return datetime.datetime.utcfromtimestamp(self.epoch_time)

    def print_info(self):
        print (time.strftime('%Y %j %H %M %S', time.gmtime(self.epoch_time)) 
            + ', %0.2f' % self.sv_value)
