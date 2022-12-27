import json
import sys


class Writer():

    def __init__(self, outputFile):
        self.outputFile = outputFile
        self._checkWritable()

    def write(self, txt):
        self._jsonwrite(txt)

    def _checkWritable(self):
        try:
            with open(self.outputFile, 'a'):
                pass
        except IOError as e:
            print(e)
            sys.exit(2)  # force the exit code 2.
# This is Clicks bad arguments code

    def _jsonwrite(self, txt):
        json_object = json.dumps(txt, indent=4)
        with open(self.outputFile, "a") as outfile:
            outfile.write(json_object)

    def _csvwrite(self):
        """Not implemented"""
        pass
