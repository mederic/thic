#! /usr/bin/python


import thic_core
import thic_gui
import imp
import os
import sys
import pickle
import shutil


def write_css(index_file):
    index_file.write('<style>\n')
    index_file.write('.ok, .ok a, .ok a:visited { color: green; }\n')
    index_file.write('.ko, .ko a, .ko a:visited  { color: red; }\n')
    index_file.write('table img  { max-height: 192px; }\n')
    index_file.write('</style>\n')


def write_test(file, test_package):
    file.write('<html><head>\n')
    write_css(file)
    file.write('<h1>')
    file.write(test_package.name)
    file.write('</h1>\n<table>')
    for screen_shot in test_package.test.screen_shots:
        if screen_shot.is_the_same:
            file.write('\n<tr class="ok">')
        else:
            file.write('\n<tr class="ko">')

        file.write('<td colspan="2">' + test_package.name + "-" + str(screen_shot.id) + "</td></tr>")

        file.write('\n<tr><td>')
        file.write('\n<div class="context">')
        if not screen_shot.test_context is None:
            file.write(screen_shot.test_context)
        file.write('\n</div></td>')

        file.write('\n<td rowspan="3">')
        file.write('\n<img src="' + os.path.abspath(screen_shot.get_candidate_path()))
        file.write('"/>')
        file.write('\n</td>')
        file.write('\n<td rowspan="3">')
        file.write('\n<img src="' + os.path.abspath(screen_shot.get_reference_path()))
        file.write('"/>')
        file.write('\n</td>')

        file.write('\n<tr><td><div class="test">')
        if not screen_shot.test_test is None:
            file.write(screen_shot.test_test)
        file.write('\n</div></td></tr>')
        file.write('\n<tr><td><div class="expectations">')
        if not screen_shot.test_expectation is None:
            file.write(screen_shot.test_expectation)
        file.write('\n</div>')
        file.write('\n</td></tr>')

    file.write('\n</table></head><body>')


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
                if screen_shot.is_the_same:
                    shutil.copy(candidate_path, reference_path)
                else:
                    test.is_ok = False



        html_result_folder = 'Thic-HTML-Result'
        if os.path.exists(html_result_folder):
            shutil.rmtree(html_result_folder)

        os.makedirs(html_result_folder)
        with open(os.path.join(html_result_folder, 'index.html'), 'w') as index_file:
            index_file.write('<html><head>')
            write_css(index_file)
            index_file.write('</head><body>')

            index_file.write('\n<h1>Test results</h1><ul>')
            for test_package in test_packages:
                test = test_package.test
                if test.is_ok:
                    index_file.write('\n<li class="ok">')
                else:
                    index_file.write('\n<li class="ko">')

                target_file_path = 'result-' + test_package.name + '.html'
                index_file.write('<a href="')
                index_file.write(target_file_path)
                index_file.write('">' + test_package.name + '</a></li>')

                with open(os.path.join(html_result_folder, target_file_path), 'w') as target_file:
                    write_test(target_file, test_package)

            index_file.write('\n</ul></body></html>')

    if os.path.exists(thic_core.TestPackage.PICKLE_FILE):
        os.remove(thic_core.TestPackage.PICKLE_FILE)



if __name__ == "__main__":
    main()
