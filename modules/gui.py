import tkinter as tk
from tkinter import ttk

class Gui():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('SleepWell - Trivselsinitiativ')
        self.root.geometry('1280x720')

        self.style()

        self.display_page_layout()
        
        skiplogin = False # Debug: Change to true to skip the log in screen

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

    
    # LOGIN SCREEN
    def display_login(self):
        self.body.update()

        r_width = self.body.winfo_width()
        r_height = self.body.winfo_height()

        login_frame = ttk.Frame(self.body, width = r_width, height = r_height, style ='TFrame')
        login_frame.pack_propagate(False)
        login_frame.pack(expand = True)

        login_content_frame = ttk.Frame(login_frame)
        login_content_frame.place(relx=0.5, rely=0.5, anchor='center')

        login_label = ttk.Label(login_content_frame, text = "Login with ID")
        login_label.pack()

        self.login_entry = ttk.Entry(login_content_frame)
        self.login_entry.pack()
        login_button = ttk.Button(login_content_frame, text='Login', command= lambda: self.login(login_frame))
        login_button.pack()

    
    # Login authentication (currently only checks if there is something in the entry)
    def login(self, login_frame):
        login=self.login_entry.get()
        if login:
            self.destroy_frame(login_frame)
            self.display_dashboard()
            

    # DASHBOARD SCREEN
    def display_dashboard(self):
        self.root.update()

        r_width = self.root.winfo_width()
        r_height = self.root.winfo_height()

        dash_frame = ttk.Frame(self.body, width = r_width, height = r_height, style ='TFrame')
        dash_frame.pack_propagate(False)
        dash_frame.pack(expand = True)


        ocupation_frame = ttk.Frame(dash_frame, style='o.TFrame', width = r_width/8, height=r_height) # The dashbord is seperated into 2 columns, occupation and data
        data_frame = ttk.Frame(dash_frame, style='d.TFrame', width = r_width - r_width/8, height=r_height)
        ocupation_frame.pack_propagate(0)
        data_frame.pack_propagate(0)

        
        ocupation_frame.grid(row=0, column=0, sticky="nsew")
        data_frame.grid(row=0, column=1, sticky="nsew")

        dash_frame.grid_columnconfigure(0, weight=1)
        dash_frame.grid_columnconfigure(1, weight=8)


        ocupation_text = ttk.Label(ocupation_frame, text = "ocupation")
        #ocupation_text.pack()

        self.data_text = ttk.Label(data_frame, text = "Data_placeholder_title", justify="left", style='H2.TLabel')
        self.data_text.pack(anchor='nw', padx=10, pady=10)


        occupation_temp = sorted(['Doctor','Software E', 'Sales Repr', 'Teacher', 'Nurse', 'Engineer', 'Accountant', 'Scientist', 'Lawyer', 'Salesperson'])
        self.build_buttons(ocupation_frame, occupation_temp, 0, 5)



        # Treeview -- needs to be moved to own method
        self.data_table = ttk.Treeview(data_frame)
        self.data_table['show'] = 'headings'
        self.data_table['columns'] = ('ID', 'gender', 'age', 'occupation', 'sleep_duration', 'sleep_quality', 'physical_activity_level', 'stress_level', 'bmi_category', 'blood_pressure', 'heart_rate', 'daily_steps', 'sleep_disorder')
        
        # Assing width and minwidth and anchor to respective columns
        self.data_table.column('ID', width=20, minwidth=20, anchor = tk.CENTER)
        self.data_table.column('gender', width=50, minwidth=50, anchor = tk.CENTER)
        self.data_table.column('age', width=50, minwidth=50, anchor = tk.CENTER)
        self.data_table.column('occupation', width=70, minwidth=70, anchor = tk.CENTER)
        self.data_table.column('sleep_duration', width=90, minwidth=90, anchor = tk.CENTER)
        self.data_table.column('sleep_quality', width=90, minwidth=90, anchor = tk.CENTER)
        self.data_table.column('physical_activity_level', width=130, minwidth=130, anchor = tk.CENTER)
        self.data_table.column('stress_level', width=100, minwidth=100, anchor = tk.CENTER)
        self.data_table.column('bmi_category', width=100, minwidth=100, anchor = tk.CENTER)
        self.data_table.column('blood_pressure', width=100, minwidth=100, anchor = tk.CENTER)
        self.data_table.column('heart_rate', width=100, minwidth=100, anchor = tk.CENTER)
        self.data_table.column('daily_steps', width=100, minwidth=100, anchor = tk.CENTER)
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

        self.data_table.grid(row=1, column=0, padx=10, pady=(50, 0))




        # Temp data inserts -- needs to be removed
        self.data_table.insert(parent='', index = 'end', values = [1, 'male', 32, 'Doctor', 7.5, 6, 5, 7, 'Normal', '125/80', 70, 10000, 'None'])
        self.data_table.insert(parent='', index = 'end', values = [2, 'female', 32, 'Teacher', 7.5, 6, 5, 7, 'Normal', '125/80', 70, 10000, 'None'])
        self.data_table.insert(parent='', index = 'end', values = [3, 'male', 32, 'Scientist', 7.5, 6, 5, 7, 'Normal', '125/80', 70, 10000, 'None'])


        # Add new rows to database and treeview -- not working currently
        data_add_frame = ttk.Frame(data_frame, style='o.TFrame', width = r_width - r_width/8, height=100)
        data_add_frame.pack_propagate(0)
        data_add_frame.grid(row=2, column=0)

        inputs = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Sleep Quality', 'Physical Activity Level', 'Stress Level', 'BMI Category', 'Blood Pressure', 'Heart Rate', 'Daily Steps', 'Sleep Disorder']

        self.build_data_input(data_add_frame, inputs, 'left', 6, 'TLabel')



        # Options for data handling -- add new data has no funcionality only delete works
        data_options_frame = ttk.Frame(data_frame, style='TFrame', width = r_width - r_width/8, height=r_height)
        data_options_frame.pack_propagate(0)
        data_options_frame.grid(row=3, column=0)


        delete_btn = ttk.Button(data_options_frame, text = 'Delete', command=self.delete)
        delete_btn.pack(side='left', anchor='nw', padx=10, pady=10)
        
        add_btn = ttk.Button(data_options_frame, text = 'Add')
        add_btn.pack(side='left', anchor='nw', padx=10, pady=10)
    
    # Generates all labels and entries to insert new data
    def build_data_input(self, frame, input_list, justify, maxCol, style):
        row = 0
        col = 0

        for input in input_list:
            print(f'input_label row:{row}, col:{col}')
            label = ttk.Label(frame, text = input, justify = justify, style = style)
            label.grid(row=row, column=col)

            col += 1

            print(f'input_entry row:{row}, col:{col}')
            entry = ttk.Entry(frame)
            entry.grid(row=row, column=col)
            
            col += 1
            if col == maxCol:
                col = 0
                row += 1        


    # When occupation buttons is clicked
    def button_events(self, event):
        clicked_button = event.widget.cget('text')
        self.get_occupations(clicked_button)


    # Change what data is being shown -- currently only changes self.data_text
    def get_occupations(self, occupation):
        self.data_text.config(text = occupation)



    # Read DB
    def read(self):
        pass
    
    # Delete data from treeview and DB
    def delete(self):
        selected_items = self.data_table.selection()

        if selected_items:
            id_list = []

            for i in selected_items:
                current_item = self.data_table.item(i)
                
                current_id = current_item.get('values')[0]
                id_list.append(current_id)
            
            print(id_list)
            #data.deleteByID('test_table', id_list)

            for record in selected_items:
                self.data_table.delete(record)


    # Updata DB
    def update_DB(self):
        pass

    # Removes frame, for when new screen has to be shown
    def destroy_frame(self, frame):
        frame.destroy()
    
    # Generates buttons
    def build_buttons(self, frame, btn_list, padx, pady):
        for btn_text in btn_list:
            btn = ttk.Button(frame, text = btn_text )
            btn.bind('<Button-1>', self.button_events)
            btn.pack(padx=padx, pady=pady)

    # Build treeview
    def build_treeview(self, frame):
        pass

        # SCROLLBAR
        # scollbar_table = ttk.Scrollbar(self.history_frame, orient='vertical', command = self.history_table.yview, style='arrowless.Vertical.TScrollbar')
        # self.history_table.configure(yscrollcommand = scollbar_table.set)
        # scollbar_table.place(relx = 1, rely = 0, relheight = 1, anchor = 'ne')




    # For styling the elements
    def style(self):
        style = ttk.Style()


        # Create style used by default for all Frames
        style.configure('TFrame', background='#303030') #All frames have this color as default
        style.configure('o.TFrame', background='#404040') # Temp -- ocupation frame
        style.configure('d.TFrame', background='#303030') # Temp -- data frame

        style.configure('H2.TLabel', # Headings style
            font=(None, 12),
            background = '#303030',
            foreground = 'white'
        )

if __name__ == "__main__":
    Gui()