import tkinter as tk 
import customtkinter as ctk
# import PIL as pl
# import PIL.Image
# import PIL.ImageTk

from PIL import Image, ImageTk

root = ctk.CTk()

#Test dictionary
dict = {"Chainsawman": "Chainsaw URL", "Demon Slayer": "Demon URL", "Evangelion": "Eva URL", "Jujutsu Kaisen":
 "Jujutsu URL", "MHA": "MHA URL", "Naurto": "Naurto URL"}

dict2 = {"ChaCha": "Chainsaw URL", "DeDe": "Demon URL", "EvaEva": "Eva URL", "Juju":
 "Jujutsu URL", "MMMM": "MHA URL", "NARNAR": "Naurto URL"}


input = tk.StringVar(root)

root.geometry("1000x600")#window size 
root.title("E-Reader")#GUI title


def submit():
    print("button clicked!")
    name = input.get()
    print(f"name is: '{name}'")
    # external_search(webdriver.Firefox, name)
    #returns a dict of the external search results
    if name == "pog":
        result_list = list(dict2.keys())
    else:
        result_list = list(dict.keys())

    for i in range(len(result_list)):
        print(result_list[i])
    
    search_results(result_list)
    

def search_results(items):
    results = tk.Listbox(right_frame, width=150, height=150, font=("Comic Sans MS", 40))
    results.pack(side='bottom', padx=100,pady=250)
    for i in items:
        results.insert("end", i)
   

# img = Image.open(r"C:\Users\oscar\Documents\GitHubStuff\Ava.jpg")
# img = img.resize((200,300), Image.ANTIALIAS)
# my_img = ImageTk.PhotoImage(img)
# my_label = tk.Label(image=my_img)
# # my_label.image = my_img
# my_label.pack()


#left frame
# bkg = ImageTk.PhotoImage(file= r"C:\Users\oscar\Documents\GitHubStuff\background.png")
# left_frame = tk.Frame(root, width=350, height=500, bg='green')
# left_frame.pack(side='left', expand=True)
left_frame = ctk.CTkFrame(root, width=500, corner_radius=0)# corners become square when the corner_radius = 0 
# left_frame['padding'] = 100
left_frame.pack(side='left', padx=5, expand=True)

#right frame
right_frame = ctk.CTkFrame(root, width=500, height=450)
right_frame.pack(side='right', expand=True)

#left frame widgets
search_text = ctk.CTkLabel(left_frame, width=200, height=300, text="E-Reader", font=("Comic Sans MS", 30))
search_text.pack(pady=20)

entry = ctk.CTkEntry(left_frame, textvariable=input, placeholder_text="Search Manga...", font=("Comic Sans MS", 15))
#NOTE: for some reason the placeholder text doesn't work when 'textvariable' is set as a parameter
entry.pack(padx=20, pady=10)

search_button = ctk.CTkButton(left_frame, command=submit, text="Submit", anchor= "bottom", font=("Comic Sans MS", 15))
search_button.pack(pady=80)

#right frame widgets
# my_listbox = tk.Listbox(right_frame, width=150, height=150)
# my_listbox.pack(side='bottom', padx=100,pady=50)




root.mainloop()# end of main loop; all code must be above this line