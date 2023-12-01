import tkinter
from tkinter import messagebox
import customtkinter as ctk
from db_utils import df_from_db
from graph import render_route, render_heatmap
import pandas as pd
from threading import Thread
from tkcalendar import Calendar
import datetime


class PickStartDateWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_attributes('-topmost', True)
        self.title('Pick Start Date')
        self.geometry('200x200')

        self.cal = Calendar(self, selectmode='day', date_pattern='dd/mm/y', year=2023, month=10, day=1)
        self.cal.pack()

        self.cal.bind('<<CalendarSelected>>', self.set_date)

    def set_date(self, event):
        global start_date
        start_date.set(self.cal.get_date())


class PickEndDateWindow(ctk.CTkToplevel):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_attributes('-topmost', True)
        self.title('Pick End Date')
        self.geometry('200x200')

        self.cal = Calendar(self, selectmode='day', date_pattern='dd/mm/y', year=2023, month=10, day=1)
        self.cal.pack()

        self.cal.bind('<<CalendarSelected>>', self.set_date)

    def set_date(self, event):
        global end_date
        end_date.set(self.cal.get_date())


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        global start_date
        global end_date

        super().__init__(*args, **kwargs)

        start_date = ctk.StringVar(value='01/10/2023')
        end_date = ctk.StringVar(value='30/10/2023')

        self.title('GeoLocation')
        self.geometry('460x180')

        self.cbox_lb = ctk.CTkLabel(self, text='Application:', anchor='w')
        self.cbox_lb.grid(row=0, column=0, padx=20, pady=20)

        self.cbox_val = ctk.StringVar(value='Bolt')
        self.cbox = ctk.CTkComboBox(self, values=['Bolt', 'Uklon', 'Glovo'], variable=self.cbox_val)
        self.cbox.grid(row=0, column=1, padx=20, pady=20)

        self.start_date_lb = ctk.CTkLabel(self, text='Start Date:', anchor='w')
        self.start_date_lb.grid(row=1, column=0)

        self.start_date_entry = ctk.CTkEntry(self, state='disabled')
        self.start_date_entry.configure(textvariable=start_date)
        self.start_date_entry.bind('<1>', command=self.pick_start_date)
        self.start_date_entry.grid(row=1, column=1)

        self.end_date_lb = ctk.CTkLabel(self, text='End Date:', anchor='w')
        self.end_date_lb.grid(row=2, column=0, pady=20)

        self.end_date = ctk.StringVar(value='30/10/2023')

        self.end_date_entry = ctk.CTkEntry(self, state='disabled')
        self.end_date_entry.configure(textvariable=end_date)
        self.end_date_entry.bind('<1>', command=self.pick_end_date)
        self.end_date_entry.grid(row=2, column=1)

        self.btn_heatmap = ctk.CTkButton(master=self, text='Generate HeatMap', corner_radius=10, command=lambda: self.get_heatmap())
        self.btn_heatmap.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.btn_heatmap.grid(row=1, column=2)


        self.btn_route = ctk.CTkButton(master=self, text='Generate Route', corner_radius=10, command=lambda: self.get_route())
        self.btn_route.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.btn_route.grid(row=2, column=2)

        self.toplevel = None

    def get_heatmap(self) -> None:
        global start_date
        global end_date

        start = datetime.datetime.strptime(start_date.get(), '%d/%m/%Y')
        end = datetime.datetime.strptime(end_date.get(), '%d/%m/%Y')

        if start > end:
            messagebox.showwarning('Warning', 'Start date should be equal or less than End date!')
        else:
            self.btn_heatmap.configure(state='disabled')
            df = df_from_db(f'db/{self.cbox_val.get().lower()}.db')
            df = df.loc[start.strftime('%Y-%m-%d') : end.strftime('%Y-%m-%d')]
            render_heatmap(df)
            self.btn_heatmap.configure(state='normal')

    def get_route(self) -> None:
        global start_date
        global end_date

        start = datetime.datetime.strptime(start_date.get(), '%d/%m/%Y')
        end = datetime.datetime.strptime(end_date.get(), '%d/%m/%Y')

        if start > end:
            messagebox.showwarning('Warning', 'Start date should be equal or less than End date!')
        else:
            self.btn_route.configure(state='disabled')
            df = df_from_db(f'db/{self.cbox_val.get().lower()}.db')
            df = df.loc[start.strftime('%Y-%m-%d') : end.strftime('%Y-%m-%d')]
            if len(df) < 2:
                messagebox.showwarning('Warning', 'Not enough nodes to construct route!')
            else:
                render_route(df)
                self.btn_route.configure(state='normal')

    def pick_start_date(self, event):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = PickStartDateWindow(self)
        else:
            self.toplevel.focus()

    def pick_end_date(self, event):
        if self.toplevel is None or not self.toplevel.winfo_exists():
            self.toplevel = PickEndDateWindow(self)
        else:
            self.toplevel.focus()


app = App()
app.mainloop()
