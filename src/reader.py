import ipaddress
import os
from collections import Counter
import src.logObject as logObject


class Reader:

    def __init__(self, readPath):
        self.readPath = readPath

    # return the most/least common IPs in the counter
    def returnFip(self, k=1, ip_type='all', ah=0, mfip=True):
        ipcounter = self._mostcommonIps(ip_type, ah)
        if mfip:
            return ipcounter.most_common(k)
        else:
            return ipcounter.most_common()[:-k-1:-1]

    def _mostcommonIps(self, ip_type, autoheal):

        filesList = self._read_file()
        ips = []
        for thisFile in filesList:
            with thisFile:
                for line in thisFile:
                    cip = line['cip']
                    destip = line['destip']
                    if autoheal:
                        try:
                            ipaddress.ip_address(line['cip'])
                        except ValueError:
                            cip = None

                        try:
                            ipaddress.ip_address(line['destip'])
                        except ValueError:
                            destip = None

                    if ip_type == 'all':
                        if cip:
                            ips.append(cip)
                        if destip:
                            ips.append(destip)

                    elif ip_type == 'client':
                        if cip:
                            ips.append(cip)
                    else:
                        if destip:
                            destip.append(destip)

        ipcnt = Counter(ips)
        return ipcnt

    def _read_file(self):
        returnFiles = []
        if os.path.isfile(self.readPath):
            thisFile = logObject.ProxyLogFile(self.readPath)
            returnFiles.append(thisFile)
        elif os.path.isdir(self.readPath):
            for subdir, dirs, files in os.walk(self.readPath):
                for file in files:
                    fullFilePath = self.readPath + '/' + file
                    thisFile = logObject.ProxyLogFile(fullFilePath)
                    returnFiles.append(thisFile)
        else:
            raise OSError('unknown files')
        return returnFiles

    def sumbytes(self, src, dest, resp_type):
        sumbytes = 0
        filesList = self._read_file()
        for thisFile in filesList:
            with thisFile:
                for line in thisFile:
                    sumbytes += self._returnBytes(src, dest, resp_type, line)
        return sumbytes

    def _returnBytes(self, src, dest, resp_type, line):
        if src and src != line['cip']:
            return 0
        if dest and dest != line['destip']:
            return 0
        if resp_type == 'all':
            return line['rheader'] + line['respBytes']
        elif resp_type == 'header':
            return line['rheader']
        else:
            return line['respBytes']

    def eventsPerSecond(self):
        eventTime = {}
        filesList = self._read_file()
        for thisFile in filesList:
            with thisFile:
                for line in thisFile:
                    try:
                        ts = line['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                    except AttributeError:
                        print(line)
                        exit(2)
                    #  print(ts, line['timestamp'])
                    eventTime[ts] = eventTime.get(ts, 0) + 1
                    if ts == 0:
                        print('whoooops')
        return self._avgeps(eventTime.values(), eventTime.keys())

    def _avgeps(self, vals, keys):
        try:
            res = sum(vals) // len(keys)
        except ZeroDivisionError:
            return 0
        return res
