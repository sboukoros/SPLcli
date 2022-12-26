import json


class Writer():

    def __init__(self, outputFile):
        self.outputFile = outputFile
        
    def write(self, res):
        json_object = json.dumps(res, indent=4)
        with open(self.outputFile, "a") as outfile:
            outfile.write(json_object)

    def _jsonwrite(self):
        pass

    def _csvwrite(self):
        pass
