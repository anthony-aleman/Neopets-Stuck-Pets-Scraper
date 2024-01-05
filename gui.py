from tkinter import *

root = Tk()
root.geometry("500x500")
root.title("Neopets Scraper")
root.configure(bg="white")

def print_something(*args):
    print("Button Clicked")
    print("Hello World")

btn = Button(root, text="Click Me", command=print_something)
btn.place(relx=0.5, rely=0.5, anchor=CENTER)

root.mainloop()