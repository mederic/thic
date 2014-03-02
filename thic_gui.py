import Tkinter

class ThicComparator(Tkinter.Tk):

    def __init__(self, parent, test_packages):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.test_packages = test_packages
        self.initialize()

    def initialize(self):
        pass

