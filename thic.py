#! /usr/bin/python

from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice, MonkeyImage

#import argparse
import os
import imp
import sys


class Test(object):
    def __init__(self, device):
        self.device = device


#parser = argparse.ArgumentParser(description='THIC - Test by Human Image Comparison')
#parser.add_argument('-tp', '--tests-path', action="store", dest="tests_path", default=".", help='path to the folder containing the thic tests')
#args = parser.parse_args()

tests_path = sys.argv[1]

class TestPackage(object):
    def __init__(self, path, name):
        self.path = path
        self.name = name

    def get_test_file(self):
        return os.path.join(self.path, self.name + ".py")


def main():
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


    print "Test file detected count: " + str(len(test_packages))
    for test_package in test_packages:
        imp.load_source(test_package.name, test_package.get_test_file())


def phase2():
    for m in [MonkeyRunner, MonkeyDevice, MonkeyImage]:
        print "%s:\n   %s\n" % (m.__name__, dir(m))
    print "TODO"

if __name__ == "__main__":
    #main()
    phase2()
