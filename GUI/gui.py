import tkinter
import customtkinter
import os
from tkinter_window import Custom_Window


def run(web_scraper):
    root = customtkinter.CTk()
    root.geometry("720x1280")
    root.state('zoomed')
    root.title("test")

    Custom_Window(root, os.path, web_scraper)
    
    root.mainloop()
