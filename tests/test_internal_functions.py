import unittest
import SPLcli.logObject
import SPLcli.reader


class ReaderTesting(unittest.TestCase):
    """Testing internal functions of the Bytesexc operation"""
    def test_reader_string_passing(self):
        test = '1157689320.327   2864 10.105.21.199 TCP_MISS/200 10182'
        a = SPLcli.reader.Reader(test)
        self.assertRaises(OSError, a._getFiles)

    def test_reader_num_passing(self):
        test = '10182'
        a = SPLcli.reader.Reader(test)
        self.assertRaises(OSError, a._getFiles)

    def test_reader_correct_passing_one_file(self):
        test = './tests/test_files/access.log'
        a = SPLcli.reader.Reader(test)
        files = a._getFiles()
        assert len(files) == 1
        assert isinstance(files[0], SPLcli.logObject.ProxyLogFile)

    def test_reader_correct_passing_many_file(self):
        test = './tests/test_files/correct_data'
        a = SPLcli.reader.Reader(test)
        files = a._getFiles()
        assert len(files) == 3
        assert isinstance(files[2], SPLcli.logObject.ProxyLogFile)
        
    def test_reader_getips_iptype(self):
        line = {'cip': '127.0.0.1',
                'destip': '192.168.1.1'}
        ah = 0
        ip_type = 'all'
        a = SPLcli.reader.Reader('')
        ss = a._getips(ip_type, ah, line)
        assert len(ss) == 2

        ss = a._getips('client', ah, line)
        assert len(ss) == 1
        assert ss[0] == '127.0.0.1'

        ss = a._getips('remote', ah, line)
        assert len(ss) == 1
        assert ss[0] == '192.168.1.1'

    def test_reader_getips_badip(self):
        line = {'cip': '127sdf.0.0sssss.1',
                'destip': '192sdf.168sdf.1.1'}
        ip_type = 'all'
        a = SPLcli.reader.Reader('')
        ss = a._getips(ip_type, 0, line)  # autoheal on
        assert len(ss) == 2
        assert ss[0] == '127sdf.0.0sssss.1'

        ss = a._getips(ip_type, 1, line)  # autoheal off
        assert len(ss) == 0
        assert ss == []

    def test_avg_eps(self):
        vals = [5, 5, 5, 5, 5]
        keys = [10, 10, 10, 10, 10]
        a = SPLcli.reader.Reader('')
        res = a._avgeps(vals, keys)
        assert res == 5

    def test_zerodiv_eps(self):
        vals = [5, 5, 5, 5, 5]
        keys = []
        a = SPLcli.reader.Reader('')
        res = a._avgeps(vals, keys)
        assert res == 0  #  instead of a raise returns 0

    def test_fip_correct_Data(self):
        test = './tests/test_files/correct_data'
        a = SPLcli.reader.Reader(test)
        ips = a.returnFip(k=1, ip_type='all', ah=1, mfip=True)
        assert len(ips) == 1
        print(ips)
        assert ips[0][0] == '10.105.21.199'

if __name__ == '__main__':
    unittest.main()

