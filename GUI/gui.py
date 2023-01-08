import tkinter
import customtkinter
import os
from .tkinter_window import Custom_Window


def run(web_scraper, path):
    root = customtkinter.CTk()
    root.geometry("720x1280")
    root.state('zoomed')
    root.title("test")

    Custom_Window(root, path+r"\img", web_scraper)
    
    root.mainloop()
