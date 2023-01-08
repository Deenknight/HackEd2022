import tkinter as tk 
import customtkinter as ctk
# import PIL as pl
# import PIL.Image
# import PIL.ImageTk

from PIL import Image, ImageTk

root = ctk.CTk()

#Test dictionary
dict = {"Chainsawman": "Chainsaw URL", "Demon Slayer": "Demon URL", "Evangelion": "Eva URL", "Jujutsu Kaisen":
 "Jujutsu URL", "MHA (cringe)": "MHA URL", "Naurto": "Naurto URL"}

dict2 = {"ChaCha": "Chainsaw URL", "DeDe": "Demon URL", "EvaEva": "Eva URL", "Juju":
 "Jujutsu URL", "MMMM": "MHA URL", "NARNAR": "Naurto URL"}


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
    else:
        result_list = list(dict.keys())

    for i in range(len(result_list)):
        print(result_list[i])
    
    search_results(result_list, list_box, len(result_list))
    

def search_results(items, list_box, num_items):
    # results = tk.Listbox(right_frame, width=150, height=150, font=("Comic Sans MS", 40))
    # results.pack(side='bottom', padx=100,pady=250)
    if(num_items > 0):
        list_box.delete(0, 'end')

    for i in items:
        list_box.insert("end", i)

#left frame
left_frame = ctk.CTkFrame(root, width=500, corner_radius=0)# corners become square when the corner_radius = 0 
# left_frame['padding'] = 100
left_frame.pack(side='left', padx=5, expand=True)

#right frame
right_frame = ctk.CTkFrame(root, width=500, height=450)
right_frame.pack(side='right', expand=True)


#right frame widgets
my_listbox = tk.Listbox(right_frame, width=150, height=150, font=("Comic Sans MS", 40))
my_listbox.pack(side='bottom', padx=100,pady=50)

#left frame widgets
search_text = ctk.CTkLabel(left_frame, width=200, height=300, text="E-Reader", font=("Comic Sans MS", 30))
search_text.pack(pady=20)

entry = ctk.CTkEntry(left_frame, textvariable=input, placeholder_text="Search Manga...", font=("Comic Sans MS", 15))
#NOTE: for some reason the placeholder text doesn't work when 'textvariable' is set as a parameter
entry.pack(padx=20, pady=10)

search_button = ctk.CTkButton(left_frame, command= lambda: submit(my_listbox), text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
search_button.pack(pady=80)

# ...left_frame, command= lambda: submit(whatever u need to pass, items(?), button(?))



root.mainloop()# end of main loop; all code must be above this line