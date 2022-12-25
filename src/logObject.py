import socket
import datetime


class ProxyLogFile():

    def __init__(self, path):
        """open a squid logfile, optionally gziped"""
        try:
            self.f = open(path, 'r')
            next(self.f)
        except IOError as e:
            print(path, e)

    def __iter__(self):  # standard iterator
        return self

    def __next__(self):  # return the next log line
        line = next(self.f)
        return ProxyLogLine(line).__dict__

    def close(self):  # close the file
        self.f.close()


class ProxyLogLine():
    fields = ['timestamp', 'rheader', 'cip', 'respCode', 'respBytes',
              'method', 'url', 'uname', 'typeip', 'resptype',
              'typeAccess', 'destip']

    def __init__(self, line):
        list(map(lambda k, v: setattr(self, k, v),
                 ProxyLogLine.fields, line.split()))
        self.typeAccess, self.destip = self.typeip.split('/')
        try:
            self.timestamp = float(self.timestamp)
            self.timestamp = datetime.datetime.fromtimestamp(self.timestamp)
        except TypeError as e:
            if self.timestamp is None:
                pass
            else:
                raise e

        try:
            socket.inet_aton(self.cip)
        except OSError:
            self.cip = None

        try:
            self.respBytes = int(self.respBytes)
        except TypeError as e:
            if self.respBytes is None:
                self.respBytes = 0
            else:
                raise e

        try:
            self.rheader = int(self.rheader)
        except TypeError as e:
            if self.rheader is None:
                self.rheader = 0
            else:
                raise e

    def __str__(self):
        s = "%s " % self.timestamp
        for k in ProxyLogLine.fields[1:]:
            s += "%s " % getattr(self, k)
        return s


if __name__ == "__main__":
    s = ProxyLogFile('/home/coder/Downloads/access.log')
    for line in s:
        print(line['timestamp'])
        pass
