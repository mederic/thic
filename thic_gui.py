import Tkinter
import tkFont
import Image, ImageTk
import os

class ThicComparator(Tkinter.Tk):

    def __init__(self, parent, test_packages):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.test_packages = test_packages

        self.screen_to_compare = []
        for test_package in test_packages:
            for screen_shot in test_package.test.screen_shots:
                if not screen_shot.is_the_same:
                    self.screen_to_compare.append(screen_shot)

        self.screen_to_compare_count = len(self.screen_to_compare)
        self.initialize()
        self.compare_next()

        self.left_img = None
        self.right_img = None

    def initialize(self):
        font = tkFont.Font(family="Helvetica", size=18, weight='bold')
        self.test_name_variable = Tkinter.StringVar()
        self.test_name_label = Tkinter.Label(self, textvariable=self.test_name_variable, anchor='w', font=font)
        self.test_name_label.grid(column=0, row=0, sticky='NSEW')

        self.status_variable = Tkinter.StringVar()
        self.status_label = Tkinter.Label(self, textvariable=self.status_variable, anchor='e', font=font)
        self.status_label.grid(column=1, row=0, sticky='NSEW')

        # Infos
        self.context_variable = Tkinter.StringVar()
        self.context_label = Tkinter.Label(self, textvariable=self.context_variable, anchor='nw')
        self.context_label.grid(column=0, row=1, columnspan=2, sticky='NSEW')

        self.test_variable = Tkinter.StringVar()
        self.test_label = Tkinter.Label(self, textvariable=self.test_variable, anchor='nw')
        self.test_label.grid(column=0, row=2, columnspan=2, sticky='NSEW')

        self.expectation_variable = Tkinter.StringVar()
        self.expectation_label = Tkinter.Label(self, textvariable=self.expectation_variable, anchor='nw')
        self.expectation_label.grid(column=0, row=3, columnspan=2, sticky='NSEW')

        # buttons
        self.ok_button = Tkinter.Button(self, text=u"It's the same !", command=self.ok_action)
        self.ok_button.grid(column=0, row=4, sticky='NS')

        self.ko_button = Tkinter.Button(self, text=u"This is not what I expected...", command=self.ko_action)
        self.ko_button.grid(column=1, row=4, sticky='NS')

        # images
        self.left_img_widget = Tkinter.Canvas(self, bg='grey')
        self.left_img_widget.grid(column=0, row=5, sticky='NSEW')

        self.right_img_widget = Tkinter.Canvas(self, bg='grey')
        self.right_img_widget.grid(column=1, row=5, sticky='NSEW')

        # grid config
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(5, weight=1)

        # bind events
        self.left_img_widget.bind('<Configure>', self.resize)

    def ok_action(self):
        screen_shot = self.screen_to_compare.pop(0)
        screen_shot.is_the_same = True
        self.compare_next()
        pass

    def ko_action(self):
        screen_shot = self.screen_to_compare.pop(0)
        screen_shot.is_the_same = False
        self.compare_next()
        pass

    def compare_next(self):
        if not self.screen_to_compare:
            self.quit()
        else:
            screen_shot = self.screen_to_compare[0]

            self.test_name_variable.set(screen_shot.test.test_package.name + " - " + str(screen_shot.id))
            self.status_variable.set(str(self.screen_to_compare_count - len(self.screen_to_compare) + 1) + '/' + str(self.screen_to_compare_count))

            self.context_variable.set(screen_shot.test_context)
            self.test_variable.set(screen_shot.test_test)
            self.expectation_variable.set(screen_shot.test_expectation)
            self.resize_images(self.left_img_widget.winfo_width(), self.left_img_widget.winfo_height())

    def resize(self, event):
        self.resize_images(event.width, event.height)

    def resize_images(self, max_width, max_height):
        if not self.screen_to_compare:
            self.quit()
        else:
            screen_shot = self.screen_to_compare[0]
            reference_path = screen_shot.get_reference_path()
            candidate_path = screen_shot.get_candidate_path()


            img = Image.open(candidate_path)

            width = max_width
            height = max_width * img.size[1] / img.size[0]
            if height > max_height:
                height = max_height
                width = max_height * img.size[0] / img.size[1]

            x_offset = max_width / 2
            y_offset = max_height / 2

            img = img.resize((width, height), Image.ANTIALIAS)
            self.right_img = ImageTk.PhotoImage(img)
            self.right_img_widget.create_image((x_offset, y_offset), image=self.right_img)

            if not os.path.exists(reference_path):
                self.left_img = None
            else:
                img = Image.open(reference_path)
                img = img.resize((width, height), Image.ANTIALIAS)
                self.left_img = ImageTk.PhotoImage(img)
                self.left_img_widget.create_image((x_offset, y_offset), image=self.left_img)



