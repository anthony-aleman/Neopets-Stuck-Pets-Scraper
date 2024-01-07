import tkinter as tk
import subprocess

neopets_list = [
    "nimmo", "scorchio","jubjub","grarrl",
    "skeith","korbat","lenny","wocky",
    "bruce", "kiko","kau","usul",
    "aisha","chia","eyrie","tuskaninny",
    "flotsam","jetsam","kacheek","uni","buzz","lupe",
    "elephante","gelert","mynci","kyrii",
    "peophin","quiggle","shoyru","acara",
    "zafara","blumaroo","techo","moehog",
    "poogle", "kougra", "grundo", "koi",
    "meerca", "chomby", "pteri", "krawk",
    "tonu", "draik", "lxi", "yurble",
    "ruki", "bori", "hissi", "lutari",
    "xweetok", "ogrin", "gnorbu", "vandagyre",
]

root = tk.Tk()
root.title("Neopets Scraper")
root.geometry("700x500")

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def add_selected_pet():
    selection = neopets_listbox.curselection()
    
    if selection:
        selected_pet = neopets_listbox.get(selection[0])
        if selected_pet not in selected_listbox.get(0, tk.END):
            selected_listbox.insert(tk.END, selected_pet)
        else:
            print("Pet already in list")
    else:
        print("No selection")

def remove_selected_pet():
    selection = selected_listbox.curselection()
    
    if selection:
        selected_listbox.delete(selection[0])
    else:
        print("No selection")

def run_scraper():
    # Retrieve selected pets from selected_listbox
    selected_pets = selected_listbox.get(0, tk.END)

    if not selected_pets:
        print("No pets selected")
        return

    # assemble list of pets to feed the scraper
    pets_arguments = " ".join(selected_pets)

    # Run scraper
    subprocess.run(["python", "neopets.py", pets_arguments])


add_button = tk.Button(root, text="Add Neopet", command=add_selected_pet)
add_button.pack(side=tk.LEFT)

remove_button = tk.Button(root, text="Remove Neopet", command=remove_selected_pet)
remove_button.pack(side=tk.RIGHT)


run_scraper_button = tk.Button(root, text="Run Scraper", command=run_scraper)
run_scraper_button.pack(side=tk.BOTTOM)



# create the Neopets neopets_listbox 
neopets_listbox = tk.Listbox(root, width=15, yscrollcommand=scrollbar.set)
for pet in neopets_list:
    neopets_listbox.insert(tk.END, pet)
neopets_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=neopets_listbox.yview)

# Second listbox for selected pets
selected_listbox = tk.Listbox(root, width=15)
selected_listbox.pack(side=tk.RIGHT, fill=tk.BOTH)






def get_neopets_listbox_selection():
    selection = neopets_listbox.curselection()
    
    if selection:
        print(neopets_listbox.get(selection[0]))
    else:
        print("No selection")
    


root.mainloop()