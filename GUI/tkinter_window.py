import tkinter
import customtkinter
from PIL import Image, ImageTk
import os
from shutil import rmtree


class Custom_Window:

    def __init__(self, master, path, web_scraper):

        self.master = master
        self.path = path
        self.web_scraper = web_scraper
        
        self.make_dir("manga")
        self.make_dir("covers")
        self.make_dir("temp\covers")
        self.make_dir("temp\manga")

        self.drivers = []

        self.downloads_screen()

    # def __del__(self):
    #     rmtree(self.path+r"\temp")
    #     for i in range(len(self.drivers)):
    #         self.web_scraper.delete_driver(self.drivers[i])


    def make_dir(self, folder):
        if not os.path.exists(fr"{self.path}\{folder}"):
            os.makedirs(fr"{self.path}\{folder}")

    
    def change_screen(self, new_screen):
        match new_screen:
            case "main":
                pass
            case "reader":
                pass
            case "chapter":
                pass
            case "downloads":
                pass

    def chapters_screen(self, title):
        
        
        url = fr"https://mangabuddy.com/{title}"

        if os.path.exists(fr"{self.path}\manga\{title}"):
            path = self.path
        else:
            path = self.path+r"\temp"

            
            # NOTE could be changed to trevor's multithreading but its kinda necessary to load this 
            # before continuing with the code
            driver = self.web_scraper.create_driver()

            self.web_scraper.get_cover(driver, url, title, path+r"\covers")            

            self.web_scraper.delete_driver(driver)

        
        chapters_dict = self.web_scraper.load_chapters(url)

        for file in os.listdir(path+r"\covers"):
            if file.startswith(title):
                filename = file


        self.title_image = Image.open(os.path.join(self.path, "covers", filename))

        w = 500
        h = 800

        screen_elements = []

        self.title_image = ImageTk.PhotoImage(
            self.resize_with_aspect_ratio(self.title_image, w, h))



        label = tkinter.Label(self.master, image=self.title_image)
        label.grid(row=0, column=0) 
        label.grid_rowconfigure(0, weight=5)


        i = 0
        nc = 5

        for chapter in chapters_dict:

            screen_elements.append(tkinter.Button(self.master, text=chapter, fg="#ff0000",
                command=lambda url=chapters_dict[chapter], title=title, chapter=chapter:
                self.chapters_to_reading(url, title, chapter)))

            screen_elements[-1].grid(row=1+i//nc, column=1+i%nc)

            i += 1

    def chapters_to_reading(self, url, title, chapter):
        pass


    
    def downloads_screen(self):
        # elements on window in a grid format
        images = []
        self.button = []
        # number of columns to be used
        nc = 5

        # indexer to keep track of images for the grid
        i = 0

        for filename in os.listdir(os.path.join(self.path, "covers")):
            f = os.path.join(self.path, "covers", filename)
            if os.path.isfile(f):

                images.append(Image.open(f))

                w = 250
                h = 400
                images[i] = self.resize_with_aspect_ratio(images[i], w, h)

                images[i] = ImageTk.PhotoImage(images[i])

                self.button.append(tkinter.Button(self.master, image=images[i], 
                    command=lambda title=filename.split('.'), new_screen="reader": self.change_from_downloads(title[0], new_screen), borderwidth=0))
                
                self.button[i].image = images[i]

                self.button[-1].grid(row=i//nc, column=i%nc, padx=(100, 0), 
                    pady=(75, 25))
                i += 1

    def resize_with_aspect_ratio(self, image, max_width, max_height):
        """
        Returns a resized image with the same aspect ratio that fills the boundaries

        image: image to be resized
        max_width: width of the container
        max_height: height of the container
        """


        width, height = image.size

        aspect_ratio = width / height

        height = int(max_width / aspect_ratio)

        if height > max_height:
            width = int(max_height * aspect_ratio)
        else:
            width = max_width

        return image.resize((width, height), Image.ANTIALIAS)


    def change_from_downloads(self, title, new_screen):

        
        for i in range(len(self.button)):
            self.button[i].destroy()
        
        self.button.clear()

        print(title)
        if new_screen == "reader":
            self.reading_screen(title, "chapter-46", 46, 46)
        



    def reading_screen(self, title, chapter, num_of_chapters, chapter_number=1):

        # assign reading information
        self.page = 1
        self.chapter_number = chapter_number
        self.chapter = chapter
        self.num_of_pages = 36
        self.num_of_chapters = num_of_chapters
        self.buttons = []
        
        # create instance of image
        img = self.image_process(self.page, self.chapter, title)

        # page number
        self.pagelabel = customtkinter.CTkLabel(master=self.master, text=f"{self.page}/{self.num_of_pages}")
        self.pagelabel.pack(pady=3)

        # placement of image onto window
        self.img_frame = tkinter.Label(image=img)
        self.img_frame.image = img
        self.img_frame.pack(pady=5)

        # buttons
        self.prevB = customtkinter.CTkButton(
            master=self.master, text="<", command=lambda: self.page_next(title))
        self.prevB.pack()

        self.nextB = customtkinter.CTkButton(
            master=self.master, text=">", command=lambda: self.page_prev(title))
        self.nextB.pack(pady=5)

        # keybinds
        self.master.bind('<Right>', lambda event: self.page_prev(title))
        self.master.bind('<Left>', lambda event: self.page_next(title))
        
        
        def toggle_win():
            f1=tkinter.Frame(self.master, width=300, height=1080, bg='#12c4c0')
            f1.place(x=0, y=0)

            def buttons(x,y,text,bcolor,fcolor,cmd):
            
                def on_entera(e):
                    myButton1['background'] = bcolor #ffcc66
                    myButton1['foreground']= '#262626'  #000d33

                def on_leavea(e):
                    myButton1['background'] = fcolor
                    myButton1['foreground']= '#262626'

                button_font = tkinter.font.Font(family='Comic Sans MS', size=16, weight='bold')
                myButton1 = tkinter.Button(f1,text=text, width=40, height=2, fg='#262626', font=button_font, border=0, bg=fcolor, activeforeground='#262626', activebackground=bcolor, command=cmd)
                
                #Adds the hover effect to the buttons when the mouse is over them
                myButton1.bind("<Enter>", on_entera)
                myButton1.bind("<Leave>", on_leavea)

                myButton1.place(x=x,y=y)

            buttons(-115, 125,'Main Menu','#0f9d9a','#12c4c0',None)
            buttons(-115, 200,'Chapters','#0f9d9a','#12c4c0',None)
            buttons(-115, 275,'Downloads','#0f9d9a','#12c4c0',None)


            def retract_win():
                f1.destroy()

            img2_open = Image.open(self.path+r"\close_image.png")
            img2_resize = img2_open.resize((100, 100))
            self.img2 = ImageTk.PhotoImage(img2_resize)

            self.buttons.append(tkinter.Button(f1, image=self.img2, command=retract_win, border=0, activebackground='#12c4c0', bg='#12c4c0').place(x=-5, y=-4))


        img1_open = Image.open(self.path+r"\hamburger_image.png")
        img1_resize = img1_open.resize((80, 80))
        self.img1 = ImageTk.PhotoImage(img1_resize)

        self.buttons.append(tkinter.Button(self.master, image = self.img1, border = 0, command=toggle_win).place(x=5, y=10))
    
    def change_from_reader(self, new_screen):
        # savedata

        # clearing window elements
        self.pagelabel.destroy()
        self.img_frame.destroy()
        self.prevB.destroy()
        self.nextB.destroy()

        self.img1.destroy()
        self.img2.destroy()

        for i in range(len(self.buttons)):
            self.buttons[i].destroy()

        self.buttons.clear()


        # selecting which screen to switch to
        self.change_screen(new_screen)


    def image_process(self, page, chapter, title):
        image = Image.open(self.path+fr"\manga\{title}\{chapter}\{page}.png")
        width, height = image.size
        h = 903
        ratio = h/height  # making size of images a consistant height
        w = int(width*ratio)

        resized = image.resize((w, h), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized)

    def page_prev(self, title):
        
        self.page -= 1

        if self.page == 0 and self.chapter_number-1 == 0:
            self.page = 1

        if self.page < 1 and self.chapter_number > 1:
            self.change_chapters(0, title)

        self.reload_page(title)


    def page_next(self, title):
 
        self.page += 1
        if self.page >self.num_of_pages and self.chapter_number+1 > self.num_of_chapter:
            self.page = self.num_of_pages

        if self.page > self.num_of_pages and self.chapter_number < self.num_of_chapters:
            self.change_chapters(1, title)

        self.reload_page(title)

    def change_chapters(self,mode, title):
        if mode == 1:
            self.page = 1
            self.chapter_number += 1
        elif mode == 0:
            self.page = self.num_of_pages
            self.chapter_number -= 1

        dir_path = self.path+fr"\manga\{title}\{self.chapter}"
        self.num_of_pages = len(os.listdir(dir_path))


    def reload_page(self, title):
        self.master.title(f"Chapter {self.chapter}")
        newImage = self.image_process(self.page, self.chapter, title)
        self.img_frame.configure(image=newImage)
        self.img_frame.image = newImage
        self.pagelabel.configure(text=f"{self.page}/{self.num_of_pages}")



    def reading_to_downloads(self):
        self.button.destroy()
        
        self.downloads_screen()







    

    




if __name__ == "__main__":
    # tk elements
    reader = customtkinter.CTk()
    reader.geometry("720x1280")
    reader.state('zoomed')
    reader.title("test")

    Custom_Window(reader, path = r"C:\Users\Deenk\source\repos\Python\HackEdBeta\MangaApp\WebScraper\manga_covers")

    reader.mainloop()  # always needed at the end

