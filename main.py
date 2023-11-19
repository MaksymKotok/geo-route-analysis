import tkinter
import customtkinter as ctk


root = tkinter.Tk()
root.title('GeoLocation observer')

def babah():
    print("NUUUUUKE!")

btn = ctk.CTkButton(master=root, corner_radius=10, command=babah)
btn.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root.mainloop()
