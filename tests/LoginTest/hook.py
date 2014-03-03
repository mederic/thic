import thic_core

class Hook(thic_core.Hook):

    def before_all(self):
        print 'LoginHook - before_all'

    def after_all(self):
        print 'LoginHook - after_all'

    def before(self):
        print 'LoginHook - before'

    def after(self):
        print 'LoginHook - after'
