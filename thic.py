#! /usr/bin/python

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

#import argparse
import os
import imp
import sys, Tkinter
sys.modules['tkinter'] = Tkinter


class Test(object):

    def __init__(self, test_package, device):
        self.test_package = test_package
        self.device = device
        self.screen_shot_id = 0
        self.screen_shots = []
        self.device_width = int(device.getProperty('display.width'))
        self.device_height = int(device.getProperty('display.height'))

        self.context = None
        self.test = None
        self.expectation = None

    def set_context(self, str_value):
        self.context = str_value

    def set_test(self, str_value):
        self.test = str_value

    def set_expectation(self, str_value):
        self.expectation = str_value

    def compare_screen(self, acceptance, x = 0, y = 0, w = 0, h = 0):
        image = self.device.takeSnapshot()

        if (w == 0):
            w = self.device_width - x
        if (h == 0):
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

def main():
    tests_path = sys.argv[1]

    test_packages = []
    for test_name in os.listdir(tests_path):
        test_path = os.path.join(tests_path, test_name)
        if os.path.isdir(test_path):
            for sub_test_name in os.listdir(test_path):
                sub_test_path = os.path.join(test_path, sub_test_name)
                if os.path.isdir(sub_test_path):
                    test_package = TestPackage(sub_test_path, sub_test_name)
                    if os.path.exists(test_package.get_test_file()):
                        test_packages.append(test_package)

    device = MonkeyRunner.waitForConnection()

    print "Test file detected count: " + str(len(test_packages))
    for test_package in test_packages:
        module = imp.load_source(test_package.name, test_package.get_test_file())
        loaded_class = getattr(module, test_package.name)
        test_package.test = loaded_class(test_package, device)


    print "Test is running..."
    for test_package in test_packages:
        test_package.test.run()


    print "Start image comparison..."
    for test_package in test_packages:
        test = test_package.test
        print test_package.name + " ---------------------"
        for screen_shot in test.screen_shots:
            candidate_path = screen_shot.get_candidate_path()
            reference_path = screen_shot.get_reference_path()

            must_manually_compare = True
            screen_shot.is_the_same = True
            if os.path.exists(reference_path):
                must_manually_compare = not compare_images(candidate_path, reference_path, screen_shot.acceptance)
            if must_manually_compare:
                screen_shot.is_the_same = compare_humanly(reference_path, candidate_path)


def compare_humanly(image_path1, image_path2):
    root = Tkinter()
    frame = Frame(root)
    frame.pack()

    root.button = Button(
        frame, text="QUIT", fg="red", command=frame.quit
        )
    root.button.pack(side=LEFT)

    root.hi_there = Button(frame, text="Hello", command=root.say_hi)
    root.hi_there.pack(side=LEFT)
    return True


def phase2():
    image_path1 = sys.argv[2]
    image_path2 = sys.argv[3]
    percent = float(sys.argv[4])
    print("true" if compare_images(image_path1, image_path2, percent) else "false")


def compare_images(image_path1, image_path2, percent):
    print "Comparing images: %s / %s  : %.2f" % (image_path1, image_path2, percent)
    image1 = MonkeyRunner.loadImageFromFile(image_path1)
    image2 = MonkeyRunner.loadImageFromFile(image_path2)
    return image1.sameAs(image2, percent)




if __name__ == "__main__":
    main()
    #phase2()
