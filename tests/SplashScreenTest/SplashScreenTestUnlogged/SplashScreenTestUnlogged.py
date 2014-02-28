import thic_core

class SplashScreenTestUnlogged(thic_core.Test):
    def run(self):
        self.compare_screen(1)
        print 'run'
