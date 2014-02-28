import thic

class LoginTestFacebook(thic.Test):
    def run(self):
        
        self.set_context('Dans le ')
        self.set_test('')
        self.set_expectation('')
        self.compare_screen(0.8, 0, 56, 0, 0)


        self.set_context('')
        self.set_test('')
        self.set_expectation('')
        self.compare_screen(1)
