#! /usr/bin/python

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

import thic_core
import imp
import os
import sys
import pickle


def main():
    tests_path = sys.argv[1]

    test_packages = []
    for test_name in os.listdir(tests_path):
        test_path = os.path.join(tests_path, test_name)
        if os.path.isdir(test_path):
            for sub_test_name in os.listdir(test_path):
                sub_test_path = os.path.join(test_path, sub_test_name)
                if os.path.isdir(sub_test_path):
                    test_package = thic_core.TestPackage(sub_test_path, sub_test_name)
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

    print "Start image auto comparison..."
    for test_package in test_packages:
        test = test_package.test
        test.device = None
        for screen_shot in test.screen_shots:
            candidate_path = screen_shot.get_candidate_path()
            reference_path = screen_shot.get_reference_path()
            if os.path.exists(reference_path):
                screen_shot.is_the_same = compare_images(candidate_path, reference_path, screen_shot.acceptance)
            else:
                screen_shot.is_the_same = False

    out = open(thic_core.TestPackage.PICKLE_FILE, 'w')
    try:
        pickle.dump(test_packages, out)
    finally:
        out.close()


def compare_images(image_path1, image_path2, percent):
    print "Comparison... " + str(percent)
    image1 = MonkeyRunner.loadImageFromFile(image_path1)
    image2 = MonkeyRunner.loadImageFromFile(image_path2)
    return image1.sameAs(image2, percent)


if __name__ == "__main__":
    main()
