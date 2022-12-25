from collections import Counter
import src.logObject as logObject
import socket


class Reader:

    def __init__(self, readPath):
        self.readPath = readPath
        self.excbytes = False
        self.eps = False

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
            for line in thisFile:
                cip = line['cip']
                destip = line['destip']
                if autoheal:
                    try:
                        socket.inet_aton(line['cip'])
                    except OSError:
                        cip = None
                        
                    try:
                        socket.inet_aton(line['destip'])
                    except OSError:
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
        readPath = self.readPath
        thisFile = logObject.ProxyLogFile(readPath)
        return [thisFile]

    def sumbytes(self, src, dest, resp_type):
        sumbytes = 0
        filesList = self._read_file()
        for thisFile in filesList:
            for line in thisFile:
                if src and src != line['cip']:
                    continue
                if dest and dest != line['destip']:
                    continue
                if resp_type == 'all':
                    sumbytes = sumbytes + line['rheader'] + line['respBytes']
                elif resp_type == 'header':
                    sumbytes += line['rheader']
                else:
                    sumbytes += line['respBytes']
        print(sumbytes)

    def eventsPerSecond(self):
        eventTime = {}
        filesList = self._read_file()
        for thisFile in filesList:
            for line in thisFile:
                ts = line['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                #  print(ts, line['timestamp'])
                eventTime[ts] = eventTime.get(ts, 0) + 1
                if ts == 0:
                    print('whoooops')
        print(sum(eventTime.values())//len(eventTime.keys()))
