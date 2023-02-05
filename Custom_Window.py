import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from Web_Scraping_Driver import Web_Scraping_Driver
import os
from shutil import rmtree


class Custom_Window:
    # NOTE a lot of the variables in the screens are class variables, but 
    # i think you only have to use a class variable for the tkinter objects
    # so the data variables could be changed to be local

    def __init__(self, master):
        # connect the window to the root
        self.master = master

        # declare directories to download images and use assets/utilities
        main_path = os.path.dirname(__file__)
        self.img_path = os.path.join(main_path, "img")
        self.assets_path = os.path.join(main_path, "assets")
        adblock_path = os.path.join(main_path, "utils", "ublock_origin-1.44.4.xpi")

        # NOTE change this to create its own thread or smth with multi-threading
        self.driver = Web_Scraping_Driver(adblock_path, False)
        self.main_site = "https://mangabuddy.com/"

        # create folders if they aren't already there
        self.make_dir("manga")
        self.make_dir("covers")
        self.make_dir("temp\covers")
        self.make_dir("temp\manga")

        self.change_screen("main") 
        


    def make_dir(self, folder):
        """
        Creates folders from the window's image path if they don't exist yet

        folder: name of the folder
        """
        if not os.path.exists(fr"{self.img_path}\{folder}"):
            os.makedirs(fr"{self.img_path}\{folder}")

    
    def change_screen(self, new_screen):
        """
        Changes the user's screen to one of the presets based off of the new_screen tag

        new_screen: either 'main', 'reader', 'chapters', or 'downloads'
        #NOTE this function will exit with a message if new_screen is an invalid screen tag
        """
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
            titles = self.driver.find_titles(self.main_site, search_query)
            # external_search(webdriver.Firefox, search_query)

            
            titles_list = list(titles.keys())

            for i in range(len(titles_list)):
                print(titles_list[i])

            search_results(titles_list, list_box, len(titles_list))


        def search_results(items, list_box : tk.Listbox, num_items):
            """
            Adds the search results to the listbox
            """
            if(num_items > 0):
                list_box.delete(0, 'end')

                for i in items:
                    list_box.insert("end", i)

        def select(list_box : tk.Listbox):
            """
            Selection for each item in the listbox
            """
            selection = list_box.curselection()

            # FIXME this works for most titles, but we might want to set it up 
            # so that the link is automatically taken from each title into a
            # dictionary of some sort because some urls are slightly different than
            # just the title appended to the main page url
            self.title = list_box.get(selection).lower().replace(' ', '-')

            if selection:
                self.change_from_main("chapters")

        def quit():
            """
            Exits the program after deleting the temp folder
            """
            rmtree(self.img_path+r"\temp")
            del self.driver

            self.master.quit()
                            

       
        

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

        #input 
        self.input = tk.StringVar(self.master, "Search Manga...")
        self.entry = ctk.CTkEntry(self.left_frame, textvariable=self.input, font=("Comic Sans MS", 15))
        self.entry.bind("<Button-1>", lambda e: self.entry.delete(0, tk.END))
        self.entry.bind("<Return>", lambda e: submit(self.my_listbox))
        self.entry.pack(padx=20, pady=10)
        
        #left frame buttons
        self.search_button = ctk.CTkButton(self.left_frame, command= lambda: submit(self.my_listbox), text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
        self.search_button.pack(pady=10)

        self.read_button = ctk.CTkButton(self.left_frame, command=lambda: self.change_from_main("reader"), text="Reader", anchor= "bottom", font=("Comic Sans MS", 15))
        self.read_button.pack(pady=10)

        self.download_button = ctk.CTkButton(self.left_frame, command=lambda: self.change_from_main("downloads"), text="Downloads", anchor= "bottom", font=("Comic Sans MS", 15))
        self.download_button.pack(pady=10)

        self.quit_button = ctk.CTkButton(self.left_frame, command=quit, text="Quit", anchor= "bottom", font=("Comic Sans MS", 15))
        self.quit_button.pack(pady=10)

        # NOTE: ***TO GET length of listbox: listbox.size()
        # NOTE: get(ANCHOR) would be used for making the search results functional when you click them**
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
        # TODO add an exit button to head back to the main menu / downloads screen
        # TODO allow users to download manga to non-temp storage
        # idk whats the best way to make that look is tho :/
        # FIXME the chapter scraper doesn't get all the chapters if there are too many
        # Kingdom has like 700 chapters and it only loaded the first 12 and the last like 80 for some reason
        # idk i dont get it
        
        # get the url and decide whether to use temporary or non-temp folders
        url = fr"https://mangabuddy.com/{self.title}"
        if os.path.exists(fr"{self.img_path}\manga\{self.title}"):
            path = os.path.join(self.img_path, "covers")
            self.temp = False
        else:
            self.temp = True
            path = os.path.join(self.img_path, "temp", "covers")
            self.driver.get_cover(url, self.title, path)            


        self.chapters_dict = self.driver.load_chapters(url)

        # get the filename of the chapter
        for file in os.listdir(path):
            if file.startswith(self.title):
                cover_filename = file

        
        # TODO add the name of the title above or below the chapter image
        # NOTE this is just straight ripped off of the main menu so it could definitely
        # be changed to look better
        #left frame
        self.left_frame = ctk.CTkFrame(self.master, width=500)# NOTE: corners become square when the corner_radius = 0 
        # left_frame['padding'] = 100
        self.left_frame.pack(side='left', padx=50, expand=True)
        
        # create and display the title image
        title_image = Image.open(os.path.join(path, cover_filename))
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

        # getting the chapter names
        self.chapter_names = list(self.chapters_dict.keys())

        # reversing the order because otherwise chapter 0 is the newest chapter
        self.chapter_names.reverse()

        def select(list_box : tk.Listbox):
            selection = list_box.curselection()
            chapter_name = list_box.get(selection)
            self.chapter_num = self.chapter_names.index(chapter_name)

            self.change_from_chapter("reader")

        self.my_listbox.delete(0, 'end')

        for chapter in self.chapter_names:
            self.my_listbox.insert("end", chapter)

    
    def change_from_chapter(self, new_screen):
        
        
        # delete all elements used in the tkinter window
        self.left_frame.destroy()
        self.right_frame.destroy()
        self.list_scroll.destroy()
        self.my_listbox.destroy()

        self.change_screen(new_screen)



    def reading_screen(self):

        # NOTE a lot of the class variables here could be local
        # TODO save the reader's data when the leave
        

        def download_pages():
            """
            Uses the webdriver to download the manga pages if the directory does
            not exist
            """

            self.chapter_path = os.path.join(path, str(self.chapter_num))
            chapter_name = self.chapter_names[self.chapter_num]
            url = self.chapters_dict[chapter_name]

            # create the directory if not there, and run the webscraper
            if not os.path.exists(self.chapter_path):
                os.makedirs(self.chapter_path)

                # TODO change to multithreading
                self.driver.download_manga(url, self.chapter_path)



            self.num_of_pages = len(os.listdir(self.chapter_path))

            # rename the window
            self.master.title(f"{chapter_name}")
            

        def image_process():
            image = Image.open(os.path.join(self.chapter_path, f"{self.page}.png"))
            width, height = image.size
            h = 903
            ratio = h/height  # making size of images a consistant height
            w = int(width*ratio)

            resized = image.resize((w, h), Image.ANTIALIAS)
            return ImageTk.PhotoImage(resized)

        def page_prev():
            
            self.page -= 1

            if self.page == 0:
                if self.chapter_num == 0:
                    self.page = 1
                else:
                    change_chapters(0)

            reload_page()


        def page_next():
    
            self.page += 1
            if self.page >self.num_of_pages:
                if self.chapter_num+1 == num_of_chapters:
                    self.page = self.num_of_pages
                else:
                    change_chapters(1)
                    
            reload_page()        


        def change_chapters(mode):
            if mode == 1:
                self.chapter_num += 1
                download_pages()
                self.page = 1
            elif mode == 0:
                self.chapter_num -= 1
                download_pages()
                self.page = self.num_of_pages


        def reload_page():
            newImage = image_process()
            self.img_frame.configure(image=newImage)
            self.img_frame.image = newImage
            self.pagelabel.configure(text=f"{self.page}/{self.num_of_pages}")
        
        def toggle_win():
            """
            Sidebar menu toggle
            """

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
                #   self.buttons.append(myButton1)

            buttons(-115, 125,'Main Menu','#0f9d9a','#12c4c0',lambda new_screen="main": clear_and_change(new_screen))
            buttons(-115, 200,'Chapters','#0f9d9a','#12c4c0',lambda new_screen="chapters": clear_and_change(new_screen))
            buttons(-115, 275,'Downloads','#0f9d9a','#12c4c0',lambda new_screen="downloads": clear_and_change(new_screen))

            def retract_win():
                for widget in f1.winfo_children():
                    widget.destroy()
                f1.place_forget()
                f1.destroy()

            def clear_and_change(new_screen):
                # NOTE if we're going to add reader data saving, here would probably be best

                retract_win()
                self.master.nametowidget("menu_button").place_forget()
                self.master.nametowidget("menu_button").destroy()
                self.change_from_reader(new_screen)


            img2_open = Image.open(self.assets_path+r"\close_image.png")
            img2_resize = img2_open.resize((100, 100))
            self.img2 = ImageTk.PhotoImage(img2_resize)

            tk.Button(f1, image=self.img2, command=retract_win, border=0, activebackground='#12c4c0', bg='#12c4c0').place(x=-5, y=-4)
            

        # assign reading information
        # TODO make this use the ADT from julian - idk where it is :/

        num_of_chapters = len(self.chapter_names)

        # set up the path to be in temp or not
        if self.temp:
            path = os.path.join(self.img_path, "temp", "manga", self.title)
            
        else:
            path = os.path.join(self.img_path, "manga", self.title)


        download_pages()
        self.page = 1
        # create instance of image
        img = image_process()

        # page number
        self.pagelabel = ctk.CTkLabel(master=self.master, text=f"{self.page}/{self.num_of_pages}")
        self.pagelabel.pack(pady=3)

        # placement of image onto window
        self.img_frame = tk.Label(image=img)
        self.img_frame.image = img
        self.img_frame.pack(pady=5)

        # FIXME anyone with a NORMAL SCREEN SIZE has the previous button off the screen
        # buttons
        self.prevB = ctk.CTkButton(
            master=self.master, text="<", command=lambda: page_next())
        self.prevB.pack()

        self.nextB = ctk.CTkButton(
            master=self.master, text=">", command=lambda: page_prev())
        self.nextB.pack(pady=5)

        # keybinds
        self.master.bind('<Right>', lambda event: page_prev())
        self.master.bind('<Left>', lambda event: page_next())

        img1_open = Image.open(self.assets_path+r"\hamburger_image.png")
        img1_resize = img1_open.resize((80, 80))
        self.img1 = ImageTk.PhotoImage(img1_resize)

        tk.Button(self.master, image = self.img1, border = 0, command=toggle_win, name="menu_button").place(x=5, y=10)
        
    
    def change_from_reader(self, new_screen):
        
        
        self.pagelabel.destroy()
        self.img_frame.destroy()
        self.prevB.destroy()
        self.nextB.destroy()

        self.change_screen(new_screen)


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

        
        self.chapters_dict = self.web_scraper.load_chapters(url)

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

