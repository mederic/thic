import thic

class SplashScreenTestUnlogged(thic.Test):
    def run(self):
        self.compare_screen(1)
        print 'run'
