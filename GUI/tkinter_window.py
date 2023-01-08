import tkinter as tk
import customtkinter as ctk
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

        self.change_screen("main") #NOTE change this line to do funky stuff

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
                self.main_screen()
            case "reader":
                self.reading_screen()
            case "chapter":
                self.chapters_screen()
            case "downloads":
                self.downloads_screen()
            case other:
                exit("Something terrible has gone wrong")

    def main_screen(self):

        # Test dictionaries
        dict = {"Chainsawman": "Chainsaw URL", "Demon Slayer": "Demon URL", "Evangelion": "Eva URL", "Jujutsu Kaisen":
        "Jujutsu URL", "MHA": "MHA URL", "Naruto": "Naruto URL"}

        dict2 = {"ChaCha": "Chainsaw URL", "DeDe": "Demon URL", "EvaEva": "Eva URL", "Juju":
        "Jujutsu URL", "MMMM": "MHA URL", "NARNAR": "Naruto URL"}

        dict3 = {}

        input = tk.StringVar(self.master)

        def submit(list_box):
            '''Extracts Manga Titles from the dictionary returned by the
            extneral_search function'''
            print("button clicked!")
            name = input.get()
            print(f"name is: '{name}'")
            # external_search(webdriver.Firefox, name)

            #returns a dict of the external search results
            if(name == "pog"):
                result_list = list(dict2.keys())
            elif(name == "bruh"):
                result_list = list(dict3.keys())
            elif(name == "long"):
                result_list = ["1","2","3","4","5","6","7","8", "9", "10", "12", "13", "14", "15", "16", "17", "18","19","20"]
            else:
                result_list = list(dict.keys())

            for i in range(len(result_list)):
                print(result_list[i])

            search_results(result_list, list_box, len(result_list))


        def search_results(items, list_box, num_items):
            # if(num_items > 0):
            list_box.delete(0, 'end')

            for i in items:
                list_box.insert("end", i)

        #left frame
        self.left_frame = ctk.CTkFrame(self.master, width=500)# NOTE: corners become square when the corner_radius = 0 
        # left_frame['padding'] = 100
        self.left_frame.pack(side='left', padx=5, expand=True)

        #right frame
        self.right_frame = ctk.CTkFrame(self.master, width=500, height=450)
        self.right_frame.pack(side='right', pady=50, expand=True)

        #Stops the right frame from propagating the widget to be shrink or fit
        #right_frame.pack_propagate(False)

        #right frame widgets
        self.list_scroll = tk.Scrollbar(self.right_frame, orient='vertical')

        self.my_listbox = tk.Listbox(self.right_frame, width=150, height=150, font=("Comic Sans MS", 40), yscrollcommand= self.list_scroll.set)

        self.list_scroll.config(command=self.my_listbox.yview)
        self.list_scroll.pack(side='right', fill='y')

        self.my_listbox.pack(side='bottom', padx=100,pady=50)

        #left frame widgets
        self.search_text = ctk.CTkLabel(self.left_frame, width=200, height=300, text="E-Reader", font=("Comic Sans MS", 30))
        self.search_text.pack(pady=15)

        self.entry = ctk.CTkEntry(self.left_frame, textvariable=input, placeholder_text="Search Manga...", font=("Comic Sans MS", 15))
        #NOTE: for some reason the placeholder text doesn't work when 'textvariable' is set as a parameter
        self.entry.pack(padx=20, pady=10)

        self.search_button = ctk.CTkButton(self.left_frame, command= lambda: submit(self.my_listbox), text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
        self.search_button.pack(pady=10)

        self.read_button = ctk.CTkButton(self.left_frame, command=lambda new_screen="reader": self.change_from_main(new_screen), text="Reader", anchor= "bottom", font=("Comic Sans MS", 15))
        self.read_button.pack(pady=10)

        self.download_button = ctk.CTkButton(self.left_frame, command=lambda new_screen="downloads": self.change_from_main(new_screen), text="Downloads", anchor= "bottom", font=("Comic Sans MS", 15))
        self.download_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self.left_frame, command=self.master.quit, text="Quit", anchor= "bottom", font=("Comic Sans MS", 15))
        self.quit_button.pack(pady=10)

        #NOTE: ***TO GET length of listbox: listbox.size()
        #NOTE: get(ANCHOR) would be used for making the search results functional when you click them**
        # ...left_frame, command= lambda: submit(whatever u need to pass, items(?), button(?))

    def change_from_main(self, new_screen):

        self.left_frame.destroy()
        self.right_frame.destroy()
        self.list_scroll.destroy()
        self.my_listbox.destroy()
        self.search_text.destroy()
        self.entry.destroy()
        self.search_button.destroy()
        self.read_button.destroy()
        self.download_button.destroy()
        self.quit_button.destroy()


        self.change_screen(new_screen)

    

    def chapters_screen(self):
        
        
        url = fr"https://mangabuddy.com/{self.title}"

        if os.path.exists(fr"{self.path}\manga\{self.title}"):
            path = self.path
        else:
            path = self.path+r"\temp"

            
            # NOTE could be changed to trevor's multithreading but its kinda necessary to load this 
            # before continuing with the code
            driver = self.web_scraper.create_driver()

            self.web_scraper.get_cover(driver, url, self.title, path+r"\covers")            

            self.web_scraper.delete_driver(driver)

        
        chapters_dict = self.web_scraper.load_chapters(url)

        for file in os.listdir(path+r"\covers"):
            if file.startswith(self.title):
                filename = file

        #FIXME the chapters should be loading as a grid with the chapter image on the right'

        self.title_image = Image.open(os.path.join(self.path, "covers", filename))

        w = 500
        h = 800

        screen_elements = []

        self.title_image = ImageTk.PhotoImage(
            self.resize_with_aspect_ratio(self.title_image, w, h))



        label = tk.Label(self.master, image=self.title_image)
        label.grid(row=0, column=0) 
        label.grid_rowconfigure(0, weight=5)


        i = 0
        nc = 5

        self.num_of_chapters = len(chapters_dict)

        for chapter in chapters_dict:

            screen_elements.append(tk.Button(self.master, text=chapter, fg="#ff0000",
                command=lambda url=chapters_dict[chapter], chapter=chapter:
                self.change_from_chapter(url, chapter)))

            screen_elements[-1].grid(row=1+i//nc, column=1+i%nc)

            i += 1


    def change_from_chapter(self, url, chapter):
        self.url = url
        self.chapter = chapter

        #TODO delete all elements used in the tkinter window
        
        

    
    def downloads_screen(self):

        # elements on window in a grid format
        images = []
        self.buttons = []
        # number of columns to be used
        nc = 5

        # indexer to keep track of images for the grid
        

        self.buttons.append(tk.Button(self.master, command=lambda new_screen="main": self.change_from_downloads(new_screen)))

        i = 0

        for filename in os.listdir(os.path.join(self.path, "covers")):
            f = os.path.join(self.path, "covers", filename)
            if os.path.isfile(f):

                images.append(Image.open(f))

                w = 250
                h = 400
                images[i] = self.resize_with_aspect_ratio(images[i], w, h)

                images[i] = ImageTk.PhotoImage(images[i])

                self.buttons.append(tk.Button(self.master, image=images[i], 
                    command=lambda title=filename.split('.'), new_screen="reader": self.change_from_downloads(new_screen, title[0]), borderwidth=0))
                
                self.buttons[i+1].image = images[i]

                self.buttons[-1].grid(row=1+i//nc, column=i%nc, padx=(100, 0), 
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


    def change_from_downloads(self, new_screen, title = None):

        
        for i in range(len(self.buttons)):
            self.buttons[i].destroy()
        
        self.buttons.clear()
        
        self.title = title

        self.change_screen(new_screen)

        



    def reading_screen(self):

        # assign reading information
        #TODO make this use the ADT from julian
        self.page = 1
        self.chapter_num = 46
        self.chapter = "chapter-46"
       
        dir_path = self.path+fr"\manga\{self.title}\{self.chapter}"
        self.num_of_pages = len(os.listdir(dir_path))

        self.buttons = []
        
        # create instance of image
        img = self.image_process(self.page, self.chapter)

        # page number
        self.pagelabel = ctk.CTkLabel(master=self.master, text=f"{self.page}/{self.num_of_pages}")
        self.pagelabel.pack(pady=3)

        # placement of image onto window
        self.img_frame = tk.Label(image=img)
        self.img_frame.image = img
        self.img_frame.pack(pady=5)

        # buttons
        self.prevB = ctk.CTkButton(
            master=self.master, text="<", command=lambda: self.page_next())
        self.prevB.pack()

        self.nextB = ctk.CTkButton(
            master=self.master, text=">", command=lambda: self.page_prev())
        self.nextB.pack(pady=5)

        # keybinds
        self.master.bind('<Right>', lambda event: self.page_prev())
        self.master.bind('<Left>', lambda event: self.page_next())
        
        
        def toggle_win():
            f1=tk.Frame(self.master, width=300, height=1080, bg='#12c4c0')
            f1.place(x=0, y=0)

            def buttons(x,y,text,bcolor,fcolor,cmd):
            
                def on_entera(e):
                    myButton1['background'] = bcolor #ffcc66
                    myButton1['foreground']= '#262626'  #000d33

                def on_leavea(e):
                    myButton1['background'] = fcolor
                    myButton1['foreground']= '#262626'

                button_font = tk.font.Font(family='Comic Sans MS', size=16, weight='bold')
                myButton1 = tk.Button(f1,text=text, width=40, height=2, fg='#262626', font=button_font, border=0, bg=fcolor, activeforeground='#262626', activebackground=bcolor, command=cmd)
                
                #Adds the hover effect to the buttons when the mouse is over them
                myButton1.bind("<Enter>", on_entera)
                myButton1.bind("<Leave>", on_leavea)

                myButton1.place(x=x,y=y)

            self.buttons.append(buttons(-115, 125,'Main Menu','#0f9d9a','#12c4c0',lambda new_screen="main": self.change_from_reader(new_screen)))
            self.buttons.append(buttons(-115, 200,'Chapters','#0f9d9a','#12c4c0',lambda new_screen="chapter": self.change_from_reader(new_screen)))
            self.buttons.append(buttons(-115, 275,'Downloads','#0f9d9a','#12c4c0',lambda new_screen="downloads": self.change_from_reader(new_screen)))


            def retract_win():
                f1.destroy()

            img2_open = Image.open(self.path+r"\close_image.png")
            img2_resize = img2_open.resize((100, 100))
            self.img2 = ImageTk.PhotoImage(img2_resize)

            self.buttons.append(tk.Button(f1, image=self.img2, command=retract_win, border=0, activebackground='#12c4c0', bg='#12c4c0').place(x=-5, y=-4))


        img1_open = Image.open(self.path+r"\hamburger_image.png")
        img1_resize = img1_open.resize((80, 80))
        self.img1 = ImageTk.PhotoImage(img1_resize)

        self.buttons.append(tk.Button(self.master, image = self.img1, border = 0, command=toggle_win).place(x=5, y=10))
    
    def change_from_reader(self, new_screen):
        # savedata

        for i in range(len(self.buttons)):
            self.buttons[i].destroy()

        self.buttons.clear()
        
        # clearing window elements
        self.pagelabel.destroy()
        self.img_frame.destroy()
        self.prevB.destroy()
        self.nextB.destroy()

        


        # selecting which screen to switch to
        self.change_screen(new_screen)


    def image_process(self, page, chapter):
        image = Image.open(self.path+fr"\manga\{self.title}\{chapter}\{page}.png")
        width, height = image.size
        h = 903
        ratio = h/height  # making size of images a consistant height
        w = int(width*ratio)

        resized = image.resize((w, h), Image.ANTIALIAS)
        return ImageTk.PhotoImage(resized)

    def page_prev(self):
        
        self.page -= 1

        if self.page == 0 and self.chapter_number-1 == 0:
            self.page = 1

        if self.page < 1 and self.chapter_number > 1:
            self.change_chapters(0)

        self.reload_page()


    def page_next(self):
 
        self.page += 1
        if self.page >self.num_of_pages and self.chapter_number+1 > self.num_of_chapter:
            self.page = self.num_of_pages

        if self.page > self.num_of_pages and self.chapter_number < self.num_of_chapters:
            self.change_chapters(1)

        self.reload_page()

    def change_chapters(self,mode):
        if mode == 1:
            self.page = 1
            self.chapter_number += 1
        elif mode == 0:
            self.page = self.num_of_pages
            self.chapter_number -= 1

        dir_path = self.path+fr"\manga\{self.title}\{self.chapter}"
        self.num_of_pages = len(os.listdir(dir_path))


    def reload_page(self):
        self.master.title(f"Chapter {self.chapter}")
        newImage = self.image_process(self.page, self.chapter)
        self.img_frame.configure(image=newImage)
        self.img_frame.image = newImage
        self.pagelabel.configure(text=f"{self.page}/{self.num_of_pages}")




    

    




if __name__ == "__main__":
    # tk elements
    reader = ctk.CTk()
    reader.geometry("720x1280")
    reader.state('zoomed')
    reader.title("test")

    Custom_Window(reader, path = r"C:\Users\Deenk\source\repos\Python\HackEdBeta\MangaApp\WebScraper\manga_covers")

    reader.mainloop()  # always needed at the end

