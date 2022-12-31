import SPLcli.SPLcli
import unittest
from click.testing import CliRunner


class CliTesting(unittest.TestCase):
    """Testing the main input/output arguments of the program"""
    """From those the program read and writes to files/dirs  """

    def test_cli_readfile_doesntExist(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/acss.log", "./tests/test_files/tt.txt",
                  "mfip"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_cli_missingFile(self):
        runner = CliRunner()
        clitxt = ["/root/access.log",  "mfip"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_cli_readfile_inbaddirectory(self):
        runner = CliRunner()
        clitxt = ["/root/access.log", "./tests/test_files/tt.txt", "mfip"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_cli_writefile_inbaddirectory(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "/root/file.txt",
                  "mfip"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert 'Permission denied' in result.output


class FipTesting(unittest.TestCase):
    """Testing the commands mfip/lfip as they are identical (almost)"""

    def test_fip_topk_negative_k(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-k -2"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_fip_topk_too_large_k(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-k 10000"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_fip_topk_alpha__k(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-k asdf"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_fip_topk_alpha_ah(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-ah asdf"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args
    
    def test_fip_topk_neg_ah(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-ah -10"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args
    
    def test_fip_topk_large_ah(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "mfip", "-ah 3"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args
        

class EpsTesting(unittest.TestCase):
    """Testing the commands eps which returns the events per second"""
    def test_eps_any_arguments(self):  # this commands doestn accept arguments
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "eps", "-ah"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args


class BytesExcTesting(unittest.TestCase):
    """Testing the commands bytesexc which returns the exchanged bytes"""

    def test_bytes_neg_dest(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "bytesexc", "-dest -2"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_bytes_wrong_SPLcli(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "bytesexc", "-SPLcli 10000"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_bytes_alpha_dest(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "bytesexc", "-dest asdf"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_bytes_alpha_SPLcli(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "bytesexc", "-SPLcli asdf"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args

    def test_bytes_wrong_args(self):
        runner = CliRunner()
        clitxt = ["./tests/test_files/access.log", "./tests/test_files/tt.txt",
                  "bytesexc", "-ah 3"]
        result = runner.invoke(SPLcli.SPLcli.cli, clitxt)
        assert result.exit_code == 2  # exitcode 2 : Click package: bad args


if __name__ == '__main__':
    unittest.main()

