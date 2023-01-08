import tkinter as tk 
import customtkinter as ctk
# import PIL as pl
# import PIL.Image
# import PIL.ImageTk
#from title_finder import *

from PIL import Image, ImageTk

root = ctk.CTk()

#Test dictionaries
dict = {"Chainsawman": "Chainsaw URL", "Demon Slayer": "Demon URL", "Evangelion": "Eva URL", "Jujutsu Kaisen":
 "Jujutsu URL", "MHA": "MHA URL", "Naruto": "Naruto URL"}

dict2 = {"ChaCha": "Chainsaw URL", "DeDe": "Demon URL", "EvaEva": "Eva URL", "Juju":
 "Jujutsu URL", "MMMM": "MHA URL", "NARNAR": "Naruto URL"}

dict3 = {}

input = tk.StringVar(root)

root.geometry("1000x600")#window size 
root.title("E-Reader")#GUI title
root.state('zoomed')

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

#temporary func
def downloads():
    print("Lol you tickled the download button")
#temporary func
def reader():
    print("Time to get reading!")

def search_results(items, list_box, num_items):
    # if(num_items > 0):
    list_box.delete(0, 'end')

    for i in items:
        list_box.insert("end", i)


#MAIN MENU **************************************
def main_menu():
    #left frame
    left_frame = ctk.CTkFrame(root, width=500)# NOTE: corners become square when the corner_radius = 0 
    # left_frame['padding'] = 100
    left_frame.pack(side='left', padx=5, expand=True)

    #right frame
    right_frame = ctk.CTkFrame(root, width=500, height=450)
    right_frame.pack(side='right', pady=50, expand=True)

    #Stops the right frame from propagating the widget to be shrink or fit
    #right_frame.pack_propagate(False)

    #right frame widgets
    list_scroll = tk.Scrollbar(right_frame, orient='vertical')

    my_listbox = tk.Listbox(right_frame, width=150, height=150, font=("Comic Sans MS", 40), yscrollcommand= list_scroll.set)

    list_scroll.config(command=my_listbox.yview)
    list_scroll.pack(side='right', fill='y')

    my_listbox.pack(side='bottom', padx=100,pady=50)

    #left frame widgets
    search_text = ctk.CTkLabel(left_frame, width=200, height=300, text="E-Reader", font=("Comic Sans MS", 30))
    search_text.pack(pady=15)

    entry = ctk.CTkEntry(left_frame, textvariable=input, placeholder_text="Search Manga...", font=("Comic Sans MS", 15))
    #NOTE: for some reason the placeholder text doesn't work when 'textvariable' is set as a parameter
    entry.pack(padx=20, pady=10)

    search_button = ctk.CTkButton(left_frame, command= lambda: submit(my_listbox), text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
    search_button.pack(pady=10)

    read_button = ctk.CTkButton(left_frame, command=reader, text="Reader", anchor= "bottom", font=("Comic Sans MS", 15))
    read_button.pack(pady=10)

    download_button = ctk.CTkButton(left_frame, command=downloads, text="Downloads", anchor= "bottom", font=("Comic Sans MS", 15))
    download_button.pack(pady=10)

    quit_button = ctk.CTkButton(left_frame, command=root.quit, text="Quit", anchor= "bottom", font=("Comic Sans MS", 15))
    quit_button.pack(pady=10)

    #NOTE: ***TO GET length of listbox: listbox.size()
    #NOTE: get(ANCHOR) would be used for making the search results functional when you click them**
    # ...left_frame, command= lambda: submit(whatever u need to pass, items(?), button(?))

main_menu()
root.mainloop()# end of main loop; all code must be above this line