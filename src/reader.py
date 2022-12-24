import os
import csv
import heapq
from collections import Counter


class Reader:

    def __init__(self, readPath, outputPath):
        self.readPath = readPath
        self.outputPath = outputPath
        self.excbytes = False
        self.eps = False

    #return the most common IPs in the counter
    def returnMfip(self, k=1):
        ipcounter = self._mostcommonIps()
        print(ipcounter.most_common(k)) 

    # return the least common IPs 
    def returnLfip(self, k=1):
        ipcounter = self._mostcommonIps()
        print(ipcounter.most_common()[:-k-1:-1]) # firnthe most common ones and return from the counter in reverse

    def _mostcommonIps(self):
        request = "IPs"
        ips = self._read_file(request)
        ipcnt = Counter(ips)
        return ipcnt

    def _read_file(self, *args):
        readPath = self.readPath
        outputPath = self.outputPath
        request = args[0]
        
        if request == 'IPs':
            clientIPs = []
            remoteIps = []

        if os.path.isfile(readPath):
            with open(readPath, 'r') as file:
                 csvreader = csv.reader(file)
                 for row in csvreader:
                    if row == []:
                        continue
                    if request == 'IPs':
                        #print(row)
                        clientIPs.append(row[0].split()[2])
        return clientIPs

         #   print(row)
    

    def main():
        pass


    def heap():
        pass


    def eps():
        pass

    def sumbytes():
        pass