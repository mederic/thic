#! /usr/bin/python


import thic_core
import thic_gui
import imp
import os
import sys
import pickle
import shutil

def main():

    tests_path = sys.argv[1]
    test_packages = None

    for test_name in os.listdir(tests_path):
        test_path = os.path.join(tests_path, test_name)
        if os.path.isdir(test_path):
            for sub_test_name in os.listdir(test_path):
                sub_test_path = os.path.join(test_path, sub_test_name)
                if os.path.isdir(sub_test_path):
                    test_package = thic_core.TestPackage(sub_test_path, sub_test_name)
                    if os.path.exists(test_package.get_test_file()):
                        imp.load_source(sub_test_name, os.path.join(sub_test_path, sub_test_name + '.py'))

    with open(thic_core.TestPackage.PICKLE_FILE, "r") as input_file:
        test_packages = pickle.load(input_file)

    if test_packages is None:
        print "Error retrieving saved file..."
    else:
        app = thic_gui.ThicComparator(None, test_packages)
        app.title('THIC - Tests by Human Image Comparison')
        app.mainloop()

        for test_package in test_packages:
            test = test_package.test
            for screen_shot in test.screen_shots:
                candidate_path = screen_shot.get_candidate_path()
                reference_path = screen_shot.get_reference_path()
                if not screen_shot.is_the_same:
                    screen_shot.is_the_same = compare_humanly(reference_path, candidate_path);

                if screen_shot.is_the_same:
                    shutil.copy(candidate_path, reference_path)
                else:
                    test.is_ok = False



        for test_package in test_packages:
            test = test_package.test
            if test.is_ok:
                print "[OK] " + test_package.name
            else:
                print "[KO] " + test_package.name + " ======================="

    if os.path.exists(thic_core.TestPackage.PICKLE_FILE):
        os.remove(thic_core.TestPackage.PICKLE_FILE)

def compare_humanly(image_path1, image_path2):
    return False


if __name__ == "__main__":
    main()
