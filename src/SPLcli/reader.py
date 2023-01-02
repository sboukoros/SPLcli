import ipaddress
from collections import Counter
import SPLcli.logObject as logObject


class Reader:
    ''' Main class that coordinates program functionalities'''
    def __init__(self, readPath):
        self.readpath = readPath

    '''Return the files provided by the user'''
    def _getFiles(self):  
        files = logObject.FilesList(self.readpath)
        self.files = files.returnFiles()
        return self.files

    ''' Return the most/least common IPs in the counter '''
    def returnFip(self, k=1, ip_type='all', ah=0, mfip=True):
        ipcounter = self._mostcommonIps(ip_type, ah)
        if mfip:
            return ipcounter.most_common(k)
        else:
            return ipcounter.most_common()[:-k-1:-1]

    def _mostcommonIps(self, ip_type, autoheal):

        filesList = self._getFiles()
        ips = []
        for thisFile in filesList:
            with thisFile:
                for line in thisFile:
                    ips.extend(self._getips(ip_type, autoheal, line))
        ipcnt = Counter(ips)
        return ipcnt

    def _getips(self, ip_type, autoheal, line):
        cip = line['cip']
        destip = line['destip']
        returnips = []
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
                returnips.append(cip)
            if destip:
                returnips.append(destip)

        elif ip_type == 'client':
            if cip:
                returnips.append(cip)
        else:
            if destip:
                returnips.append(destip)
        return returnips

    '''Retunrs the sum of all bytes'''
    def sumbytes(self, src, dest, resp_type):
        sumbytes = 0
        filesList = self._getFiles()
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
        filesList = self._getFiles()
        for thisFile in filesList:
            with thisFile:
                for line in thisFile:
                    ts = self._gettimestamp(line)
                    eventTime[ts] = eventTime.get(ts, 0) + 1
        return self._avgeps(eventTime.values(), eventTime.keys())

    def _gettimestamp(self, line):
        try:
            ts = line['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        except AttributeError as e:
            print(e, line)
            exit(2)
        return ts

    def _avgeps(self, vals, keys):
        try:
            res = sum(vals) // len(keys)
        except ZeroDivisionError:
            return 0   # in case of error, return 0 as it wont affect the sum
        return res
