import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from Web_Scraping_Driver import Web_Scraping_Driver
import os
from shutil import rmtree


class Custom_Window:

    def __init__(self, master):
        
        self.master = master

        main_path = os.path.dirname(__file__)
        self.img_path = os.path.join(main_path, "img")
        self.assets_path = os.path.join(main_path, "assets")
        adblock_path = os.path.join(main_path, "utils", "ublock_origin-1.44.4.xpi")

        self.driver = Web_Scraping_Driver(adblock_path, False)
        self.main_site = "https://mangabuddy.com/"

        self.make_dir("manga")
        self.make_dir("covers")
        self.make_dir("temp\covers")
        self.make_dir("temp\manga")

        self.change_screen("main") #NOTE change this line to do funky stuff
        
    # TODO check if this works, and if not make it delete the temp folder
    def __del__(self):
        rmtree(self.img_path+r"\temp")
        del self.driver


    def make_dir(self, folder):
        if not os.path.exists(fr"{self.img_path}\{folder}"):
            os.makedirs(fr"{self.img_path}\{folder}")

    
    def change_screen(self, new_screen):
        match new_screen:
            case "main":
                self.main_screen()
            case "reader":
                self.reading_screen()
            case "chapters": 
                self.chapters_screen()
            case "downloads":
                self.downloads_screen()
            case other:
                exit("Something terrible has gone wrong")

    def main_screen(self):

        def submit(list_box : tk.Listbox):
            '''Extracts Manga Titles from the dictionary returned by the
            extneral_search function'''
            print("button clicked!")
            search_query = self.input.get()
            self.titles = self.driver.find_titles(self.main_site, search_query)
            # external_search(webdriver.Firefox, search_query)

            
            result_list = list(self.titles.keys())

            for i in range(len(result_list)):
                print(result_list[i])

            search_results(result_list, list_box, len(result_list))


        def search_results(items, list_box : tk.Listbox, num_items):
            if(num_items > 0):
                list_box.delete(0, 'end')

                for i in items:
                    list_box.insert("end", i)

        def select(list_box : tk.Listbox):
            selection = list_box.curselection()

            # FIXME this works for most titles, but we might want to set it up 
            # so that the link is automatically taken from each title into a
            # dictionary of some sort
            self.title = list_box.get(selection).lower().replace(' ', '-')

            if selection:
                self.change_from_main("chapters")
                            


        self.input = tk.StringVar(self.master, "Search Manga...")
        

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
        self.my_listbox.bind('<Double-1>', lambda e: select(self.my_listbox))


        self.list_scroll.config(command=self.my_listbox.yview)
        self.list_scroll.pack(side='right', fill='y')

        
        self.my_listbox.pack(side='bottom', padx=100,pady=50)

        #left frame widgets
        self.search_text = ctk.CTkLabel(self.left_frame, width=200, height=300, text="E-Reader", font=("Comic Sans MS", 30))
        self.search_text.pack(pady=15)

        self.entry = ctk.CTkEntry(self.left_frame, textvariable=self.input, font=("Comic Sans MS", 15))
        self.entry.bind("<Button-1>", lambda e: self.entry.delete(0, tk.END))
        
        self.entry.pack(padx=20, pady=10)

        # TODO set it up so clicking ENTER on the search button searches
        self.search_button = ctk.CTkButton(self.left_frame, command= lambda: submit(self.my_listbox), text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
        self.search_button.pack(pady=10)

        self.read_button = ctk.CTkButton(self.left_frame, command=lambda new_screen="reader": self.change_from_main("reader"), text="Reader", anchor= "bottom", font=("Comic Sans MS", 15))
        self.read_button.pack(pady=10)

        self.download_button = ctk.CTkButton(self.left_frame, command=lambda new_screen="downloads": self.change_from_main("downloads"), text="Downloads", anchor= "bottom", font=("Comic Sans MS", 15))
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

        # TODO allow users to download manga to non-temp storage, which will need 
        
        
        url = fr"https://mangabuddy.com/{self.title}"

        if os.path.exists(fr"{self.img_path}\manga\{self.title}"):
            path = os.path.join(self.img_path, "covers")
        else:
            path = os.path.join(self.img_path, "temp", "covers")
            self.driver.get_cover(url, self.title, path)            


        chapters_dict = self.driver.load_chapters(url)

        for file in os.listdir(path):
            if file.startswith(self.title):
                filename = file

        
        # TODO add the name of the title above or below the chapter image
        # TODO add an exit button to head back to the main menu
        #left frame
        self.left_frame = ctk.CTkFrame(self.master, width=500)# NOTE: corners become square when the corner_radius = 0 
        # left_frame['padding'] = 100
        self.left_frame.pack(side='left', padx=50, expand=True)
        
        # create and display the title image
        title_image = Image.open(os.path.join(path, filename))
        title_image = ImageTk.PhotoImage(title_image.resize((225, 337), Image.ANTIALIAS))
        self.title_image_label = ctk.CTkLabel(self.left_frame, image=title_image, text="")
        self.title_image_label.pack()

        

        #right frame
        self.right_frame = ctk.CTkFrame(self.master, width=500, height=450)
        self.right_frame.pack(side='right', pady=50, expand=True)

        #Stops the right frame from propagating the widget to be shrink or fit
        #right_frame.pack_propagate(False)

        #right frame widgets
        self.list_scroll = tk.Scrollbar(self.right_frame, orient='vertical')

        self.my_listbox = tk.Listbox(self.right_frame, width=150, height=150, font=("Comic Sans MS", 40), yscrollcommand= self.list_scroll.set)
        self.my_listbox.bind('<Double-1>', lambda e: select(self.my_listbox))

        self.list_scroll.config(command=self.my_listbox.yview)
        self.list_scroll.pack(side='right', fill='y')

        self.my_listbox.pack(side='bottom', padx=100,pady=50)

        self.num_of_chapters = len(chapters_dict)

        self.chapter_names = list(chapters_dict.keys())

        def select(list_box : tk.Listbox):
            selection = list_box.curselection()

            # FIXME this works for most titles, but we might want to set it up 
            # so that the link is automatically taken from each title into a
            # dictionary of some sort

            chapter_name = list_box.get(selection)

            url = chapters_dict[chapter_name]

            self.change_from_chapter("reader", url, chapter_name)

        self.my_listbox.delete(0, 'end')

        for chapter in self.chapter_names:
            self.my_listbox.insert("end", chapter)

    
    def change_from_chapter(self, new_screen, url, chapter_name):
        self.url = url
        self.chapter_name = chapter_name
        
        # delete all elements used in the tkinter window
        self.left_frame.destroy()
        self.title_image_label.destroy()
        self.right_frame.destroy()
        self.list_scroll.destroy()
        self.my_listbox.destroy()

        self.change_screen(new_screen)



    def reading_screen(self):

        # assign reading information
        # TODO make this use the ADT from julian

        self.page = 1
        self.chapter_num = 46
        self.self.chapter_name = "chapter-46"
       
        dir_path = self.img_path+fr"\manga\{self.title}\{self.self.chapter_name}"
        self.num_of_pages = len(os.listdir(dir_path))

        self.buttons = []
        
        # create instance of image
        img = self.image_process(self.page, self.self.chapter_name)

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

            img2_open = Image.open(self.assets_path+r"\close_image.png")
            img2_resize = img2_open.resize((100, 100))
            self.img2 = ImageTk.PhotoImage(img2_resize)

            self.buttons.append(tk.Button(f1, image=self.img2, command=retract_win, border=0, activebackground='#12c4c0', bg='#12c4c0').place(x=-5, y=-4))


        img1_open = Image.open(self.assets_path+r"\hamburger_image.png")
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


    # TODO refactor this so that it is local to the reader

    def image_process(self, page, chapter):
        image = Image.open(self.img_path+fr"\manga\{self.title}\{chapter}\{page}.png")
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

        dir_path = self.img_path+fr"\manga\{self.title}\{self.self.chapter_name}"
        self.num_of_pages = len(os.listdir(dir_path))


    def reload_page(self):
        self.master.title(f"Chapter {self.self.chapter_name}")
        newImage = self.image_process(self.page, self.self.chapter_name)
        self.img_frame.configure(image=newImage)
        self.img_frame.image = newImage
        self.pagelabel.configure(text=f"{self.page}/{self.num_of_pages}")



    def downloads_screen(self):

        # elements on window in a grid format
        images = []
        self.buttons = []
        # number of columns to be used
        nc = 5

        url = fr"https://mangabuddy.com/kingdom/vol-1-chapter-1-the-unknown-boy"

        if os.path.exists(fr"{self.img_path}\manga\kingdom\1"):
            path = self.img_path
        else:
            path = self.img_path+r"\temp"

            
            # NOTE could be changed to trevor's multithreading but its kinda necessary to load this 
            # before continuing with the code
            driver = Web_Scraping_Driver(self.img_path)

            driver.download_manga(driver, url, "kingdom", 1, path)            

        
        chapters_dict = self.web_scraper.load_chapters(url)

        # indexer to keep track of images for the grid
        

        self.buttons.append(tk.Button(self.master, command=lambda new_screen="main": self.change_from_downloads(new_screen)))

        i = 0

        for filename in os.listdir(os.path.join(self.img_path, "covers")):
            f = os.path.join(self.img_path, "covers", filename)
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


    

    




if __name__ == "__main__":
    # tk elements
    reader = ctk.CTk()
    reader.geometry("720x1280")
    reader.state('zoomed')
    reader.title("test")

    Custom_Window(reader, path = r"C:\Users\Deenk\source\repos\Python\HackEdBeta\MangaApp\WebScraper\manga_covers")

    reader.mainloop()  # always needed at the end

