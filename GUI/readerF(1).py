import tkinter
import os
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import customtkinter
# im expecting that down the road page, chapter, and path will be given to this file
path = "C:\\Users\\Julian\\hacked\\Citrus\\"

page = 1
chapter = 1

num_of_page = 36
num_of_chapter = 2


def page_prev():
    global page
    page -= 1
    if page == 0 and chapter-1 == 0:
        page = 1

    if page < 1 and chapter > 1:
        change_chapters(0)

    reload_page()


def page_next():
    global page
    page += 1
    if page > num_of_page and chapter+1 > num_of_chapter:
        page = num_of_page

    if page > num_of_page and chapter < num_of_chapter:
        change_chapters(1)

    reload_page()


def change_chapters(mode):
    global path
    global page
    global chapter
    global num_of_page

    if mode == 1:
        page = 1
        chapter += 1
    elif mode == 0:
        page = num_of_page
        chapter -= 1

    dir_path = path+f"chapter{chapter}"
    num_of_page = len([entry for entry in os.listdir(
        dir_path) if os.path.isfile(os.path.join(dir_path, entry))])


def reload_page():
    app.title(f"Chapter {chapter}")
    newImage = image_process(page)
    img_frame.configure(image=newImage)
    img_frame.image = newImage
    pagelabel.configure(text=f"{page}/{num_of_page}")


def image_process(page=page):
    image = Image.open(path+f"chapter{chapter}\\{page}.jpg")
    width, height = image.size
    h = 903
    ratio = h/height  # making size of images a consistant height
    w = int(width*ratio)

    resized = image.resize((w, h), Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized)



# create instance of image
img = image_process()

# page number
pagelabel = customtkinter.CTkLabel(master=app, text=f"{page}/{num_of_page}")
pagelabel.pack(pady=3)

# placement of image onto window
img_frame = tkinter.Label(image=img)
img_frame.image = img
img_frame.pack(pady=5)

# buttons
prevB = customtkinter.CTkButton(
    master=app, text="<", command=lambda: page_next())
prevB.pack()

nextB = customtkinter.CTkButton(
    master=app, text=">", command=lambda: page_prev())
nextB.pack(pady=5)

# keybinds
app.bind('<Right>', lambda event: page_prev().focus())
app.bind('<Left>', lambda event: page_next().focus())

def toggle_win():
    f1=Frame(app, width=300, height=1080, bg='#12c4c0')
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

Button(app, image = img1, border = 0, command=toggle_win).place(x=5, y=10)