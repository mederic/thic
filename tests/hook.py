import thic_core

class Hook(thic_core.Hook):

    def before_all(self):
        print 'SuiteHook - before_all'

    def after_all(self):
        print 'SuiteHook - after_all'

    def before(self):
        print 'SuiteHook - before'

    def after(self):
        print 'SuiteHook - after'
