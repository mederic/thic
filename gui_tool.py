#! /usr/bin/python
import sys
from Tkinter import *


def main():
    root = Tk()

    #image = PhotoImage(file="images/pencils.jpg")

    button = Button(root, text="QUIT", fg="red", command=root.quit)
    button.pack(side=LEFT)

    root.mainloop()


if __name__ == "__main__":
    main()
