import tkinter as tk
from tkinter import simpledialog, messagebox
import os
if not os.path.exists("notes"):
    os.makedirs("notes")

# Create the main window
window = tk.Tk()
window.title("My Personal Notes App")
window.geometry("600x400")


# Entry widget for the note title
title_var = tk.StringVar()

#rename note
def rename_note(): 
    selected = note_listbox.curselection()
    if selected:
        old_filename = note_listbox.get(selected[0])
        old_path = f"notes/{old_filename}"
        # Prompt for new name
        new_title = simpledialog.askstring("Rename Note", "Enter new note title:", initialvalue=old_filename[:-4])
        if new_title and new_title.strip():
            new_filename = f"{new_title.strip()}.txt"
            new_path = f"notes/{new_filename}"
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                load_notes_list()
                # Optionally, select the renamed note
                for i in range(note_listbox.size()):
                    if note_listbox.get(i) == new_filename:
                        note_listbox.selection_set(i)
                        note_listbox.activate(i)
                        break
                title_var.set(new_title.strip())
            else:
                messagebox.showerror("Error", "A note with that title already exists.")
# Save function 
def save_note():
    title = title_var.get().strip()
    if not title:
        return  # Optionally, show a warning that title is required
    filename = f"notes/{title}.txt"
    content = text_area.get("1.0", "end").strip()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    load_notes_list()

#load a note
def load_note(event):
    selected = note_listbox.curselection()
    if selected:
        filename = note_listbox.get(selected[0])
        title_var.set(filename[:-4])  # Remove '.txt' for the title entry
        with open(f"notes/{filename}", "r", encoding="utf-8") as f:
            content = f.read()
        text_area.delete("1.0", "end")
        text_area.insert("1.0", content)

def load_notes_list():
    note_listbox.delete(0, "end")
    for file in os.listdir("notes"):
        if file.endswith(".txt"):
            note_listbox.insert("end", file)

#delete notes
def delete_note():
    selected = note_listbox.curselection()
    if selected:
        filename = note_listbox.get(selected[0])
        os.remove(f"notes/{filename}")
        note_listbox.delete(selected[0])
        title_var.set("")
        text_area.delete("1.0", "end")
        load_notes_list()

# new note
def new_note():
    title_var.set("")
    text_area.delete("1.0", "end")


# Toolbar at the top of the window
toolbar = tk.Frame(window, bd=1, relief="raised")
toolbar.pack(side="top", fill="x")

new_button = tk.Button(toolbar, text="New Note", command=lambda: [title_var.set(""), text_area.delete("1.0", "end")])
new_button.pack(side="left", padx=2, pady=2)

#delete note
save_toolbar_button= tk.Button(toolbar, text="Delete", command=delete_note)
save_toolbar_button.pack(side="left", padx=2, pady=2)

#rename note
new_button = tk.Button(toolbar, text="Rename", command=rename_note)
new_button.pack(side="left", padx=2, pady=2)

# Main horizontal frame to hold the listbox and the right side
main_frame = tk.Frame(window)
main_frame.pack(fill="both", expand=True)

# Listbox on the left, fills vertically
note_listbox = tk.Listbox(
    main_frame,
    font=("Calibri", 12),     # Change font family and size here
    width=17        # Increase width (number of characters)
)
note_listbox.pack(side="left", fill="y", padx=5, pady=16)
note_listbox.bind("<<ListboxSelect>>", load_note)

# Right frame for title and text area
right_frame = tk.Frame(main_frame)
right_frame.pack(side="left", fill="both", expand=True)

# Title and save button at the top of the right frame
title_frame = tk.Frame(right_frame)
title_frame.pack(fill="x", padx=1, pady=(10, 5))

title_entry = tk.Entry(title_frame, textvariable=title_var, font=("Calibri", 12, "bold"))
title_entry.pack(side="left", fill="x", expand=True)

save_button = tk.Button(
    title_frame,
    text="Save Note",
    command=save_note,
    bg="#83CC86",
    fg="white",
    font=("Calibri", 12, "bold"),
    bd=3,
    relief="raised",
    padx=7,
    pady=3,
    width=7,
    height=1
)
save_button.pack(side="right", padx=(10, 0))

# Text area fills the rest of the right frame
text_area = tk.Text(right_frame, wrap="word", font=("Calibri", 12))
text_area.pack(expand=True, fill="both")


load_notes_list()


def rename_note():
    selected = note_listbox.curselection()
    if selected:
        old_filename = note_listbox.get(selected[0])
        old_path = f"notes/{old_filename}"
        # Prompt for new name
        new_title = tk.simpledialog.askstring("Rename Note", "Enter new note title:", initialvalue=old_filename[:-4])
        if new_title and new_title.strip():
            new_filename = f"{new_title.strip()}.txt"
            new_path = f"notes/{new_filename}"
            if not os.path.exists(new_path):
                os.rename(old_path, new_path)
                load_notes_list()
                # Optionally, select the renamed note
                for i in range(note_listbox.size()):
                    if note_listbox.get(i) == new_filename:
                        note_listbox.selection_set(i)
                        note_listbox.activate(i)
                        break
                title_var.set(new_title.strip())
            else:
                tk.messagebox.showerror("Error", "A note with that title already exists.")


def show_note_menu(event):
    # Select the item under the mouse
    try:
        index = note_listbox.nearest(event.y)
        note_listbox.selection_clear(0, tk.END)
        note_listbox.selection_set(index)
        note_listbox.activate(index)
        note_menu.tk_popup(event.x_root, event.y_root)
    finally:
        note_menu.grab_release()

#deleting notes
note_menu = tk.Menu(window, tearoff=0)
note_menu.add_command(label="Delete Note", command=delete_note)
note_menu.add_command(label="Rename Note", command=rename_note)
note_menu.add_command(label="New Note", command=new_note)

note_listbox.bind("<Button-3>", show_note_menu)  # For Windows

# Run the window
window.mainloop()