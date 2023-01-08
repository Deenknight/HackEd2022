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

        self.chapters_screen("chainsaw-man")

    # def __del__(self):
    #     rmtree(self.path+r"\temp")
    #     for i in range(len(self.drivers)):
    #         self.web_scraper.delete_driver(self.drivers[i])


    def make_dir(self, folder):
        if not os.path.exists(fr"{self.path}\{folder}"):
            os.makedirs(fr"{self.path}\{folder}")

    
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
                    command=lambda title=filename.split('.'): self.downloads_to_reading(title[0]), borderwidth=0))
                
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

    def downloads_to_reading(self, title):

        
        for i in range(len(self.button)):
            self.button[i].destroy()
        
        self.button.clear()

        print(title)

        self.reading_screen()



    def reading_screen(self):
        self.button = tkinter.Button(self.master, text="Click me to go back", 
                    command=self.reading_to_downloads, borderwidth=0)
        self.button.pack()

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

