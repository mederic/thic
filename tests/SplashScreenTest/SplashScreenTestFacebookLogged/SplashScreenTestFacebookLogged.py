import thic_core

class SplashScreenTestFacebookLogged(thic_core.Test):
    def run(self):
        self.compare_screen(0.9, 0, 856, 0, 692)
        print 'run'
