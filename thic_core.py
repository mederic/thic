import os

class Hook(object):

    def __init__(self, device):
        self.device = device

    def before_all(self):
        pass

    def after_all(self):
        pass

    def before(self):
        pass

    def after(self):
        pass


class Test(object):

    def __init__(self, test_package, device, monkey_runner):
        self.test_package = test_package
        self.device = device
        self.monkey_runner = monkey_runner
        self.screen_shot_id = 0
        self.screen_shots = []
        self.device_width = int(device.getProperty('display.width'))
        self.device_height = int(device.getProperty('display.height'))

        self.context = None
        self.test = None
        self.expectation = None

        self.is_ok = True

    def set_context(self, str_value):
        self.context = str_value

    def set_test(self, str_value):
        self.test = str_value

    def set_expectation(self, str_value):
        self.expectation = str_value

    def sleep(self, seconds):
        self.monkey_runner.sleep(seconds)

    def compare_screen(self, acceptance, x = 0, y = 0, w = 0, h = 0):
        image = self.device.takeSnapshot()

        if w == 0:
            w = self.device_width - x
        if h == 0:
            h = self.device_height - y

        image = image.getSubImage((x, y, w, h))

        screen_shot = ScreenShot(self.screen_shot_id, acceptance, self)

        image.writeToFile(screen_shot.get_candidate_path(), 'png')
        self.screen_shots.append(screen_shot)
        self.screen_shot_id += 1


class ScreenShot(object):
    def __init__(self, id, acceptance, test):
        self.id = id
        self.acceptance = acceptance
        self.test = test
        self.test_context = test.context
        self.test_test = test.test
        self.test_expectation = test.expectation

    def get_candidate_path(self):
        picture_folder = self.test.test_package.get_picture_folder()
        return os.path.join(picture_folder, 'tak' + str(self.id) + '.png')

    def get_reference_path(self):
        picture_folder = self.test.test_package.get_picture_folder()
        return os.path.join(picture_folder, 'ref' + str(self.id) + '.png')


class TestPackage(object):

    PICKLE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'result.pickle')

    def __init__(self, path, name):
        self.path = path
        self.name = name
    def get_test_file(self):
        return os.path.join(self.path, self.name + '.py')

    def get_picture_folder(self):
        result = os.path.join(self.path, 'result');
        if not os.path.exists(result):
            os.makedirs(result)

        return result