

import customtkinter
from Custom_Window import Custom_Window
import os



path = os.path.dirname(__file__)

root = customtkinter.CTk()
root.geometry("720x1280")
root.state('zoomed')
root.title("test")

Custom_Window(root)

root.mainloop()


    