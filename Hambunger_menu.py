from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

window = customtkinter.CTk()
window.geometry("1920x1080+0+0")
window.title("Hambruhger menu")
window.configure(bg='white')
window.state('zoomed')

def toggle_win():
    f1=Frame(window, width=300, height=1080, bg='#12c4c0')
    f1.place(x=0, y=0)

    def buttons(x,y,text,bcolor,fcolor,cmd):
     
        def on_entera(e):
            myButton1['background'] = bcolor #ffcc66
            myButton1['foreground']= '#262626'  #000d33

        def on_leavea(e):
            myButton1['background'] = fcolor
            myButton1['foreground']= '#262626'

        button_font = font.Font(family='Comic Sans MS', size=16, weight='bold')
        myButton1 = Button(f1,text=text, width=40, height=2, fg='#262626', font=button_font, border=0, bg=fcolor, activeforeground='#262626', activebackground=bcolor, command=cmd)
        
        #Adds the hover effect to the buttons when the mouse is over them
        myButton1.bind("<Enter>", on_entera)
        myButton1.bind("<Leave>", on_leavea)

        myButton1.place(x=x,y=y)

    buttons(-115, 125,'Main Menu','#0f9d9a','#12c4c0',None)
    buttons(-115, 200,'Chapters','#0f9d9a','#12c4c0',None)
    buttons(-115, 275,'Downloads','#0f9d9a','#12c4c0',None)


    def retract_win():
        f1.destroy()

    global img2
    img2_open = Image.open("GUI\close_image.png")
    img2_resize = img2_open.resize((100, 100))
    img2 = ImageTk.PhotoImage(img2_resize)

    Button(f1, image=img2, command=retract_win, border=0, activebackground='#12c4c0', bg='#12c4c0').place(x=-5, y=-4)


img1_open = Image.open("GUI\hamburger_image.png")
img1_resize = img1_open.resize((80, 80))
img1 = ImageTk.PhotoImage(img1_resize)

Button(window, image = img1, border = 0, command=toggle_win).place(x=5, y=10)


window.mainloop()