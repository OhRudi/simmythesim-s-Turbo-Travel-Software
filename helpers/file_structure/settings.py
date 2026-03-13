class Settings:
    def __init__(self):
        self.file = ""

    def create(self, paths):
        for path in paths:
            self.file += "{}\n".format(path)

    def write(self, name):
        with open("{}.settings".format(name), "w") as file:
            file.write(self.file)