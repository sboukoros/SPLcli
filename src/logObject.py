import socket
import datetime
import os

"""Main idea for the class constructions in
     https://gist.github.com/ArthurClune/3250419 """


class FilesList():

    def __init__(self, path):
        self.path = path
        self.Files = []
        if os.path.isfile(self.path):
            thisFile = ProxyLogFile(self.path)
            self.Files.append(thisFile)
        elif os.path.isdir(self.path):
            for subdir, dirs, files in os.walk(self.path):
                for file in files:
                    fullFilePath = self.path + '/' + file
                    thisFile = ProxyLogFile(fullFilePath)
                    self.Files.append(thisFile)
        else:
            raise OSError('unknown files')

    def returnFiles(self):
        return self.Files


class ProxyLogFile():
    """ Every Squid log file will be an object of this class"""
    def __init__(self, path):
        """prepare the logfile """
        self.path = path
        self.iterator = 0
        self.errlines = 0  # measure malformed lines in the file

    def open(self):

        if isinstance(self.path, str):
            try:
                os.path.isfile(self.path)
                self.fd = open(self.path, 'r')
                next(self.fd)
            except OSError:
                print(self.path + ' not a file')
                exit()
            except IOError as e:
                print(self.path, e)
                
        else:
            self.fd = self.path
            self.iterator = 1

    def __enter__(self):
        #  self.fd = open(self.path, 'r')
        #  next(self.fd)
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        if not self.iterator:
            self.close()

    def __iter__(self):  # standard iterator
        return self

    """ Returns the next log line as an instance of ProxyLogLine
        Counts the malformed lines to determine if the file is corrupted
        which in that case it exits with an error """
    def __next__(self):  # return the next log line as dictionary
        line = next(self.fd)
        lineDict = ProxyLogLine(line).__dict__
        while lineDict['malformed'] > 5:
            self.errlines += 1
            if self.errlines == 1:
                print("Is this a Squid log file? Parsing the log lines doesnt "
                      "match expected input")
                exit(-1)
            line = next(self.fd)
            lineDict = ProxyLogLine(line).__dict__
        return lineDict

    def close(self):  # close the file
        if not self.iterator:
            self.fd.close()


class ProxyLogLine():
    """Every log line will be mapped to this object"""

    """ Fields help mapping the logfile lines to the respective field.
        It also make the coding easier in case the log files changes format """
    fields = ['timestamp', 'rheader', 'cip', 'respCode', 'respBytes',
              'method', 'url', 'uname', 'typeip', 'resptype',
              'typeAccess', 'destip']
            
    def __init__(self, line):
        self.malformed = 0
        list(map(lambda k, v: setattr(self, k, v),    # map the line args
                 ProxyLogLine.fields, line.split()))  # to the field
        try:
            assert (len(line.split()) + 2) == len(ProxyLogLine.fields)
        except AssertionError:
            self.malformed = 1  # mark the line as malformed
        
        self.typeAccess, self.destip = self.typeip.split('/')

        #  make the time human readable
        try:
            self.timestamp = float(self.timestamp)
            self.timestamp = datetime.datetime.fromtimestamp(self.timestamp)
        except TypeError:
            self.malformed = 1
        #  check the IP's validity
        try:
            socket.inet_aton(self.cip)
        except OSError:
            self.cip = None

        #  make sure we have bytes properly formatted
        try:
            self.respBytes = int(self.respBytes)
        except TypeError as e:
            if self.respBytes is None or self.respBytes < 0:
                self.respBytes = 0
            else:
                raise e

        try:
            self.rheader = int(self.rheader)
        except TypeError as e:
            if self.rheader is None or self.rheader < 0:
                self.rheader = 0
            else:
                raise e

    def __str__(self):
        s = "%s " % self.timestamp
        for k in ProxyLogLine.fields[1:]:
            s += "%s " % getattr(self, k)
        return s


if __name__ == "__main__":
    ss = iter(['1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182 GET http://www.goonernews.com/ badeyek DIRECT/207.58.145.61 text/html'])
    a = ProxyLogFile(ss)
    with a:
        for i in a:
            print(i)
