import tkinter
import customtkinter
from PIL import Image, ImageTk
import os


class Custom_Window:

    def __init__(self, master, path, web_scraper):

        self.master = master
        self.path = path
        self.web_scraper = web_scraper
        
        self.make_dir("manga")
        self.make_dir("covers")

        self.downloads_screen()

    def make_dir(self, folder):
        if not os.path.exists(fr"{self.path}\{folder}"):
            os.makedirs(fr"{self.path}\{folder}")


        
    

    def downloads_screen(self):
        # elements on window in a grid format
        images = []
        self.button = []
        # number of columns to be used
        nc = 5

        # indexer to keep track of images for the grid
        i = 0

        for filename in os.listdir(fr"{self.path}\covers"):
            f = os.path.join(self.path,filename)
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
    
    def chapter_screen(self, title):
        
        pass

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

