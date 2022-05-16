import os
"""
Something to create anchors files
not implemented
"""
class createFiles():
    def __init__(self):
        self.path = "SetupData"
        self.dir_list = os.listdir(self.path)

    def touch(self):
        for name in self.dir_list:
            self.filename = "SetupData/" + name[:-3] + "csv"
            with open(self.filename, 'w') as fp:
                pass
        print("Files and directories in '", self.path, "' :")
        print(self.dir_list)


newFiles = createFiles();

newFiles.touch()


