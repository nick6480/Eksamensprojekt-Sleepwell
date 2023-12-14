import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import pandas as pd

from modules.data import Data

class Gui():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('SleepWell - Trivselsinitiativ')
        self.root.geometry('1280x900')

        self.data = Data()

        self.current_occupation = 'All'

        self.style()

        self.display_page_layout()

        skiplogin = False # Debug: Set to true to skip the login screen

        if skiplogin:
            self.display_dashboard()
        else: 
            self.display_login()

        self.root.mainloop()


     # Page layout (currently only a body, but header could be added)
    def display_page_layout(self): 
        self.root.update()

        r_width = self.root.winfo_width()
        r_height = self.root.winfo_height()

        self.body = ttk.Frame(self.root, width = r_width, height = r_height, style ='TFrame')
        self.body.pack_propagate(False)
        self.body.pack(expand = True)


    # ---- LOGIN SCREEN ----
    def display_login(self):
        self.body.update()

        r_width = self.body.winfo_width()
        r_height = self.body.winfo_height()
        
        # Login wrap frame
        login_frame = ttk.Frame(self.body, width = r_width, height = r_height, style ='TFrame')
        login_frame.pack_propagate(False)
        login_frame.pack(expand = True)

        # Login page content
        login_content_frame = ttk.Frame(login_frame)
        login_content_frame.place(relx=0.5, rely=0.5, anchor='center')

        login_label = ttk.Label(login_content_frame, text = "Login with ID", style = 'login_text.TLabel')
        login_label.pack(pady = 10)
        
        # Login Inputs
        self.login_entry=ttk.Entry(login_content_frame)
        self.login_entry.pack()
        
        login_button = ttk.Button(login_content_frame, text='Login', command= lambda: self.login(login_frame))
        login_button.pack(pady = 10)

        # Error Message label
        self.error_msg_label = ttk.Label(login_content_frame, text = "", style = 'error_msg.TLabel') 
        self.error_msg_label.pack()

    
    # ---- LOGIN AUTHENTICATION ----
    def login(self, login_frame):
        id=self.login_entry.get()

        try:  # Validate if input is int, and if it exitsts in the database
            int(id)
            if self.data.authenticate_user(id):
                self.destroy_frame(login_frame)
                self.display_dashboard()
            else: 
                self.error_msg_label.config(text = 'The entered id was not found')

        except ValueError:
            self.error_msg_label.config(text = 'The entered id is not valid')


    # ---- DASHBOARD SCREEN ----
    def display_dashboard(self):
        self.body.update()

        r_width = self.body.winfo_width()
        r_height = self.body.winfo_height()


        # Dashboard wrap frame 
        dash_frame = ttk.Frame(self.body, width = r_width, height = r_height, style ='TFrame')
        dash_frame.pack_propagate(False)
        dash_frame.pack(expand = True)

        # The dashbord is seperated into 2 columns, occupation and data
        ocupation_frame = ttk.Frame(dash_frame, style='o.TFrame', width = r_width/9, height=r_height) 
        

        
        self.data_frame = ttk.Frame(dash_frame, style='d.TFrame', width = r_width - r_width/9, height=r_height)

        ocupation_frame.pack_propagate(0)
        self.data_frame.pack_propagate(0)

        ocupation_frame.grid(pady = 0, row=0, column=0, sticky="nsew")
        self.data_frame.grid(row=0, column=1, sticky="nsew")
    
        dash_frame.grid_columnconfigure(0, weight=1)
        dash_frame.grid_columnconfigure(1, weight=9)

        self.data_text = ttk.Label(self.data_frame, text = self.current_occupation, justify="left", style='H2.TLabel') # Header that displays the currently selected occupation
        self.data_text.pack(anchor='nw', padx=10, pady=10)

        ocupation_btn_frame = ttk.Frame(ocupation_frame, style='o.TFrame')
        ocupation_btn_frame.pack(fill=tk.BOTH, expand=True, pady = 15)

        occupation_list = ['All', 'Accountant', 'Doctor', 'Engineer', 'Lawyer', 'Nurse', 'Sales Representative', 'Salesperson', 'Scientist', 'Software Engineer', 'Teacher']

        self.build_buttons(ocupation_btn_frame, occupation_list, 0, 10, 100, 'left') # Creates all the buttons that are used to change selected occupation
        
        # Scrollable frame
        test_frame = ttk.Frame(self.data_frame, style="TFrame")
        test_frame.pack(fill = 'both', expand=1)

        data_frame_canvas = tk.Canvas(test_frame)     
        data_frame_canvas.pack(side = 'left', fill = 'both', expand = 1)

        scrollbar = ttk.Scrollbar(test_frame, orient = 'vertical', command=data_frame_canvas.yview, style='arrowless.Vertical.TScrollbar')
        scrollbar.pack(side='right', fill='y')

        data_frame_canvas.configure(yscrollcommand=scrollbar.set)
        data_frame_canvas.bind('<Configure>', lambda e: data_frame_canvas.configure(scrollregion=data_frame_canvas.bbox('all')))

        data_frame_scoll = ttk.Frame(data_frame_canvas)

        data_frame_canvas.create_window((0,0), window=data_frame_scoll, anchor='nw')

        self.data_table_frame = ttk.Frame(data_frame_scoll, style='TFrame', width = r_width - r_width/9, height=210)
        self.data_table_frame.pack_propagate(0)
        self.data_table_frame.grid(sticky ='nw', row=1, column=0, padx=(10, 20), pady=(0, 0))
       

        # Treeview -- needs to be moved to own method
        self.data_table = ttk.Treeview(self.data_table_frame)
        self.data_table['show'] = 'headings'
        self.data_table['columns'] = ('ID', 'gender', 'age', 'occupation', 'sleep_duration', 'sleep_quality', 'physical_activity_level', 'stress_level', 'bmi_category', 'blood_pressure', 'heart_rate', 'daily_steps', 'sleep_disorder')

        # Assign width and minwidth and anchor to respective columns
        self.data_table.column('ID', width=40, minwidth=40, anchor = tk.CENTER)
        self.data_table.column('gender', width=60, minwidth=60, anchor = tk.CENTER)
        self.data_table.column('age', width=30, minwidth=30, anchor = tk.CENTER)
        self.data_table.column('occupation', width=140, minwidth=140, anchor = tk.CENTER)
        self.data_table.column('sleep_duration', width=90, minwidth=90, anchor = tk.CENTER)
        self.data_table.column('sleep_quality', width=90, minwidth=90, anchor = tk.CENTER)
        self.data_table.column('physical_activity_level', width=125, minwidth=125, anchor = tk.CENTER)
        self.data_table.column('stress_level', width=70, minwidth=70, anchor = tk.CENTER)
        self.data_table.column('bmi_category', width=115, minwidth=115, anchor = tk.CENTER)
        self.data_table.column('blood_pressure', width=90, minwidth=90, anchor = tk.CENTER)
        self.data_table.column('heart_rate', width=70, minwidth=70, anchor = tk.CENTER)
        self.data_table.column('daily_steps', width=70, minwidth=70, anchor = tk.CENTER)
        self.data_table.column('sleep_disorder', width=100, minwidth=100, anchor = tk.CENTER)

        # Assign the heading names to the respective columns
        self.data_table.heading('ID', text = 'ID', anchor = tk.CENTER)
        self.data_table.heading('gender', text = 'Gender', anchor = tk.CENTER)
        self.data_table.heading('age', text = 'Age', anchor = tk.CENTER)
        self.data_table.heading('occupation', text = 'Occupation', anchor = tk.CENTER)
        self.data_table.heading('sleep_duration', text = 'Sleep Duration', anchor = tk.CENTER)
        self.data_table.heading('sleep_quality', text = 'Sleep Quality', anchor = tk.CENTER)
        self.data_table.heading('physical_activity_level', text = 'Physical Activity Level', anchor = tk.CENTER)
        self.data_table.heading('stress_level', text = 'Stress Level', anchor = tk.CENTER)
        self.data_table.heading('bmi_category', text = 'Bmi Category', anchor = tk.CENTER)
        self.data_table.heading('blood_pressure', text = 'Blood Pressure', anchor = tk.CENTER)
        self.data_table.heading('heart_rate', text = 'Heart Rate', anchor = tk.CENTER)
        self.data_table.heading('daily_steps', text = 'Daily Steps', anchor = tk.CENTER)
        self.data_table.heading('sleep_disorder', text = 'Sleep Disorder', anchor = tk.CENTER)

        self.data_table.grid(sticky ='nwse', row=1, column=0, padx=0, pady = (20,0))

        # Treeview Scrollbar
        scollbar_table = ttk.Scrollbar(self.data_table_frame, orient='vertical', command = self.data_table.yview, style='arrowless.Vertical.TScrollbar')
        self.data_table.configure(yscrollcommand = scollbar_table.set)
        scollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')

        # Options for data handling (Add, delete)
        data_options_frame = ttk.Frame(data_frame_scoll, style='TFrame', width = r_width - r_width/9, height=45)
        data_options_frame.pack_propagate(0)
        data_options_frame.grid(row=2, column=0)

        # Delete selected 
        delete_btn = ttk.Button(data_options_frame, text = 'Delete', command=self.delete)
        delete_btn.pack(side='left', anchor='nw', padx=10, pady=10)
        
        # Upload csv file
        upload_csv_btn = ttk.Button(data_options_frame, text='Add CSV', command=self.upload_csv, takefocus=0)
        upload_csv_btn.pack(side='left', anchor='nw', padx=10, pady=10)

        #self.frame_graph = customtkinter.CTkScrollableFrame(self.data_frame, width = r_width - r_width/9, height=r_height)
        self.frame_graph = ttk.Frame(data_frame_scoll, style='TFrame', width = r_width - r_width/9, height=r_height)
        self.frame_graph.pack_propagate(0)
        self.frame_graph.grid(sticky ='nwse', row=3, column=0, padx=0, pady=(0, 0))
        

        self.get_occupations(self.current_occupation)



     # ---- CHANGE SELECTED OCCUPATION ----
    def get_occupations(self, occupation):
        self.current_occupation = occupation # Change selected occupation 
        self.data_text.config(text = self.current_occupation) # Change heading

        data_dict = { # What table and columns to retrive
                'employees' : ['person_id', 'gender', 'age', 'occupation'],
                'health' : ['stress_level', 'bmi_category', 'blood_pressure', 'heart_rate'],
                'activity' : ['activity_level', 'daily_steps'],
                'sleep' : ['sleep_duration', 'quality_of_sleep', 'sleep_disorder']
        }  

        if self.current_occupation == 'All': # If display all else only display the selected occupation
            data = self.data.read(data_dict, (False, '', '', ''))
        else: 
            data = self.data.read(data_dict, (True, 'employees', 'occupation', self.current_occupation))
        

        self.display_treeview_data(data)
        self.display_graph(data)
       
    def display_graph(self, data):
        for widget in self.frame_graph.winfo_children(): # Clear the previeus graphs
            widget.destroy()

        df = pd.DataFrame.from_dict(data)

        # Plotting histograms
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 6), facecolor = '#303030')

        sns.histplot(df["quality_of_sleep"], kde=True, ax=axes[0, 0])
        axes[0, 0].set_title("Quality of Sleep")

        sns.histplot(df["activity_level"], kde=True, ax=axes[0, 1])
        axes[0, 1].set_title("Physical Activity Level")

        sns.lineplot(x=df["quality_of_sleep"], y=df["stress_level"], color="red", ax=axes[1, 0])
        axes[1, 0].set_title("Quality of Sleep vs. Stress Level")

        sns.lineplot(x=df["daily_steps"], y=df["activity_level"], color="green", ax=axes[1, 1])
        axes[1, 1].set_title("Daily Steps vs. Physical Activity Level")

        plt.tight_layout()

        # Embed the plot in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graph)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


    # ---- RETRIVE AND DISPLAY DATA IN TREEVIEW ---- 
    def display_treeview_data(self, data):
        self.data_table.delete(*self.data_table.get_children()) # Clears the treeview
        
        for value in data: # Change treeview values
            self.data_table.insert(parent='', index = 'end', values = [
                value['person_id'], 
                value['gender'],
                value['age'], 
                value['occupation'], 
                value['sleep_duration'],
                value['quality_of_sleep'],
                value['activity_level'],
                value['stress_level'],
                value['bmi_category'],
                value['blood_pressure'],
                value['heart_rate'],
                value['daily_steps'],
                value['sleep_disorder'],
            ])
            

    # ---- UPLOAD CSV FILE ----
    def upload_csv(self):
        filename = filedialog.askopenfilename()
        data_dict = { 
            'employees' : ['person_id', 'gender', 'age', 'occupation'],
            'health' : ['stress_level', 'bmi_category', 'blood_pressure', 'heart_rate'],
            'activity' : ['activity_level', 'daily_steps'],
            'sleep' : ['sleep_duration', 'quality_of_sleep', 'sleep_disorder']
        }  

        self.data.csv_to_DB(filename, data_dict)
        self.display_treeview_data((True, 'employees', 'occupation', self.current_occupation)) # Update Treeview


    # ---- GET CLICKED OCCUPATION ----
    def button_events(self, event):
        clicked_button = event.widget.cget('text')
        self.get_occupations(clicked_button)

    
    # ---- DELETE DATA FROM DB AND TREEVIEW ----
    def delete(self):
        selected_items = self.data_table.selection() # Get tree view selections
        
        if selected_items:
            id_list = []
            for i in selected_items:
                current_item = self.data_table.item(i)
                current_id = current_item.get('values')[0]
                id_list.append(current_id)
            
            self.data.delete('employees','person_id' ,id_list)

            for record in selected_items:
                self.data_table.delete(record)


    #  ---- DESTROY FRAME ----
    def destroy_frame(self, frame):
        frame.destroy()
    

    # ---- CREATE BUTTONS ----
    def build_buttons(self, frame, btn_list, ipadx, ipady, width, alignment):
        for btn_text in btn_list:
            btn = ttk.Button(frame, text = btn_text, width = width, compound  =alignment)
            btn.bind('<Button-1>', self.button_events)
            btn.pack(anchor='nw',ipadx=ipadx, ipady=ipady)
            

    # ---- STYLING -----
    def style(self):
        font_color = '#d4d4d4'
        background_dark = '#303030'
        background_light = '#3a3e40'
        selection_color = '#324d80'
        error_msg_color = '#a13030'

        style = ttk.Style()
        style.theme_use('default')
        style.configure('test.TFrame', background='red') #All frames have this color as default
        self.root.configure(background=background_dark) # Root
        style.configure('TFrame', background=background_dark) #All frames have this color as default
        style.configure('o.TFrame', background=background_light) # Ocupation frame
        style.configure('d.TFrame', background=background_dark) # Data frame

        style.configure('H2.TLabel', # Heading H2 style
            font=(None, 24),
            background = background_dark,
            foreground = font_color
        )

        style.configure('error_msg.TLabel', # Error Messages
            font=(None, 12),
            background = background_dark,
            foreground = error_msg_color
        )

        style.configure('login_text.TLabel', # Login Text
            font=(None, 12),
            background = background_dark,
            foreground = font_color
        )

        style.map('TButton', background=[('focus',selection_color)]) # Buttons
        style.configure('TButton', 
            background=background_light,
            foreground = font_color,
            borderwidth=0
        )
        
        style.configure('TSeparator', # Seperator 
            background=background_light,
            borderwidth=0  
        )
    
        # Matplotlib
        plt.rcParams.update({
            'text.color': font_color,
            'axes.labelcolor': font_color,
            'xtick.color':font_color,
            'ytick.color':font_color,
        })

        # TREEVIEW
        style.configure('Treeview',
            background = background_light, 
            foreground = font_color,
            fieldbackground = background_light,
            rowheigt = 25,
            font = (None, 11),
            borderwidth = 0 
        )

        
        style.map('Treeview', background = [('selected' , selection_color)]) 
        style.configure('Vertical.TScrollbar', 
            background = font_color,
            troughcolor = background_light,
            borderwidth = 0
  
        )


        style.configure("Treeview.Heading", 
            background='#1f1f1f', 
            foreground=font_color,
            borderwidth = 0

        )        

        
        style.layout('arrowless.Vertical.TScrollbar', # Scrollbar
             [('Vertical.Scrollbar.trough',
               {'children': [('Vertical.Scrollbar.thumb', 
                              {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'})])




if __name__ == "__main__":
    Gui()