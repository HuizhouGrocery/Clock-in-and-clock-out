import tkinter as tk
import ttkbootstrap as ttk
from tkinter import  messagebox,PhotoImage,filedialog,simpledialog
from ttkbootstrap import Style
import sqlite3
from time import strftime
from cv2 import VideoCapture,imshow,imwrite,waitKey,destroyWindow


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Huizhou Grocery Clock-in and Clock-out System")
        self.root.geometry("1000x600")
        self.root.style = Style('darkly')
        self.root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(file=r"Your working directory\logo.png"))
        self.PASSWORD = "12345"

        #Create time label
        self.digital_clock = ttk.Label(root, font=('calibri', 26, 'bold'), background='green', foreground='white')
        self.digital_clock.pack(anchor='center')
        self.digital_clock.place(x=480, y=255,width = 450,height=65)

        self.time()
        
        # Create a database or connect to an existing one
        self.conn = sqlite3.connect(r"Your database working directory\clock-in.db")
        self.cursor = self.conn.cursor()

        # # # Create five tables if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clockIn_records (id INTEGER PRIMARY KEY, name TEXT, clockIn_photo BLOB, time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS startBreak_records (id INTEGER PRIMARY KEY, name TEXT, startBreak_photo BLOB, time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS beginWork_records (id INTEGER PRIMARY KEY, name TEXT, beginWork_photo BLOB, time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clockOut_records (id INTEGER PRIMARY KEY, name TEXT, clockOut_photo BLOB, time TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employee_info (id INTEGER PRIMARY KEY, employee_name TEXT, employee_photo BLOB, register_time TEXT)''')


        # Put logo image into GUI

        self.image = PhotoImage(file=r"Your working directory\logo.png")
        self.image_label = ttk.Label(root, image=self.image)
        self.image_label.place(x=430, y=30, width=110, height=127)


        # Create a label for the employee name
        self.employee_name_label = ttk.Label(root, text="Employee Name:",font=("Arial", 10))
        self.employee_name_label.pack()
        self.employee_name_label.place(x=150, y=275)

        # Create an entry box for the employee name
        self.employee_name_entry = ttk.Entry(root, state="normal",bootstyle="secondary")
        self.employee_name_entry.pack(pady=10)
        self.employee_name_entry.place(x=260, y=270)


        # Create five buttons
        self.clock_in_button = ttk.Button(root, bootstyle="light-outline", text="Clock In",command=self.clock_in) 
        self.clock_in_button.pack(pady=10)
        self.clock_in_button.place(x=200, y=450,width = 120,height=45)

        self.start_break_button = ttk.Button(root, bootstyle="warning-outline", text="Start Break",command=self.start_break)
        self.start_break_button.pack(pady=10)
        self.start_break_button.place(x=400, y=450,width = 130,height=45)

        self.begin_work_button = ttk.Button(root, bootstyle="light-outline", text="Begin Work",command=self.begin_work) 
        self.begin_work_button.pack(pady=10)
        self.begin_work_button.place(x=600, y=450,width = 120,height=45)

        self.clock_out_button = ttk.Button(root,bootstyle="success-outline", text="Clock Out",command=self.clock_out)
        self.clock_out_button.pack(pady=10)
        self.clock_out_button.place(x=800, y=450,width = 120,height=45)

        self.register_employee_button = ttk.Button(root,bootstyle="light-outline", text="Register Employee",command= self.open_secondary_window)
        self.register_employee_button.pack(pady=10)
        self.register_employee_button.place(x=200, y=520,width = 120,height=45)


    def time(self):
           string = strftime('%Y-%m-%d %H:%M:%S %p %a')
           self.digital_clock.config(text=string)
           self.digital_clock.after(1000, self.time)
           

    def convertToBinaryData(self,filename):
      # Convert digital data to binary format
        with open(filename, 'rb') as file:
           blobData = file.read()
        return blobData
    
    
    def check_password(self):
        self.root = tk.Tk() 
        self.root.withdraw() # Hide the main window 
        attempt = simpledialog.askstring("Password Required ", "Please enter password if you want to continue:", show='*') 
        if attempt == self.PASSWORD:
              messagebox.showinfo("Access Granted", "Password accepted! Performing sensitive command...")
              return True
        else:
              messagebox.showerror("Access Denied", "Incorrect password.")

        self.root.destroy()


    def open_secondary_window(self):
     if self.check_password() == True:
            
            self.secondary_window = tk.Toplevel()
            self.secondary_window.tk.call("wm", "iconphoto", self.secondary_window._w, tk.PhotoImage(file=r"Your working directory\logo.png"))
            self.secondary_window.title("Register new employee")
            self.secondary_window.config(width=800, height=600)

            self.employee_name_label = ttk.Label(self.secondary_window, text="Employee Name:",font=("Arial", 9))
            self.employee_name_label.pack()
            self.employee_name_label.place(x=270, y=278,width=100,height=70)

            self.employee_name_entry = ttk.Entry(self.secondary_window, state="normal",bootstyle="secondary")
            self.employee_name_entry.pack()
            self.employee_name_entry.place(x=420, y=300)

            self.date_label = ttk.Label(self.secondary_window, text="Date:",font=("Arial", 10))
            self.date_label.pack()
            self.date_label.place(x=270, y=320,width=100,height=80)

            self.date_entry = ttk.Entry(self.secondary_window, state="normal",bootstyle="secondary")
            self.date_entry.pack()
            self.date_entry.place(x=420, y=345)

            self.employee_register_button = ttk.Button(self.secondary_window, text="Upload ID Info", command = self.employee_register)
            self.employee_register_button.place(x=240,y=420,width=150,height=40)

            self.button_close = ttk.Button(self.secondary_window, text="Close Window", command = self.secondary_window.destroy)
            self.button_close.place(x=450,y=420,width=150,height=40)

            self.secondary_window.focus()
            self.secondary_window.grab_set()
   
     else:
      messagebox.showwarning('error', 'Something went wrong!')

   
    def employee_register(self):
    

      name = self.employee_name_entry.get()
      date = self.date_entry.get()
      row = self.cursor.execute("SELECT * FROM employee_info WHERE employee_name = ?" , (name,)).fetchall()

      if row == [] and date != '' and name != '':
            photo = self.convertToBinaryData(filedialog.askopenfilename())
            self.cursor.execute("INSERT INTO employee_info (employee_name, employee_photo, register_time) VALUES (?,?,?)", (name,photo,date))
            self.conn.commit()

            messagebox.showinfo('Response', f'{name} has registered ')
      else:

            messagebox.showinfo('Response', 'You must input name and date or employee already exists')


    def clock_in(self):
     try:
            
            cam_port = 0
            cam = VideoCapture(cam_port) 
      
            # reading the input using the camera 
            result, image = cam.read() 
      
            # If image will detected without any error, and show result 
          
            if result: 
      
                  name = self.employee_name_entry.get()
                  row = self.cursor.execute("SELECT * FROM employee_info WHERE employee_name = ?" , (name,)).fetchall()

      
                  if  name != '' and row != []:
                        # it will show image result in your desktop and function have been realized
                        imshow("Camera", image) 
                              
                        # saving image in local storage 
                        imwrite(r"Your working directory\Self-Portrait.png", image)

                        convertedPhoto = self.convertToBinaryData(r"Your current working directory\Self-Portrait.png")
                        time = strftime('%Y-%m-%d %H:%M:%S %p %a')

                        self.cursor.execute("INSERT INTO clockIn_records (name, clockIn_photo,time) VALUES (?,?,?)", (name,convertedPhoto,time))

                        self.conn.commit()

                        messagebox.showinfo('Response', 'You have clocked in and press any button to continue')
                        cam.release()

                  else:
                        messagebox.showinfo('Response', 'Camera does not capture and save photo, or you must input correct employee name')
                        cam.release()

                  # If keyboard interrupt occurs, destroy image  
                  # window will be closed after 5000 milliseconds(5 seconds)
                  waitKey(5000) 
                  destroyWindow("Camera") 
                  cam.release()
      
            else: 
                  messagebox.showinfo('Response', 'You need to set up your default camera first ! ')


     except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)


    def start_break(self):
     try:
            
            cam_port = 0
            cam = VideoCapture(cam_port) 
      
            # reading the input using the camera 
            result, image = cam.read() 
      
            # If image will detected without any error, and show result 
          
            if result: 
      
                  name = self.employee_name_entry.get()
                  row = self.cursor.execute("SELECT * FROM employee_info WHERE employee_name = ?" , (name,)).fetchall()

      
                  if  name != '' and row != []:
                        # it will show image result in your desktop and function have been realized
                        imshow("Camera", image) 
                              
                        # saving image in local storage 
                        imwrite(r"Your working directory\Self-Portrait.png", image)

                        convertedPhoto = self.convertToBinaryData(r"Your working directory\Self-Portrait.png")
                        time = strftime('%Y-%m-%d %H:%M:%S %p %a')

                        self.cursor.execute("INSERT INTO startBreak_records (name, startBreak_photo,time) VALUES (?,?,?)", (name,convertedPhoto,time))

                        self.conn.commit()

                        messagebox.showinfo('Response', 'You have started your break time')
                        cam.release()

                  else:
                        messagebox.showinfo('Response', 'Camera does not capture and save photo, or you must input correct employee name')
                        cam.release()

                  # If keyboard interrupt occurs, destroy image  
                  # window will be closed after 5000 milliseconds(5 seconds)
                  waitKey(5000) 
                  destroyWindow("Camera") 
                  cam.release()
      
            else: 
                  messagebox.showinfo('Response', 'You need to set up your default camera first ! ')


     except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)


    def begin_work(self):
     try:
            
            cam_port = 0
            cam = VideoCapture(cam_port) 
      
            # reading the input using the camera 
            result, image = cam.read() 
      
            # If image will detected without any error, and show result 
          
            if result: 
      
                  name = self.employee_name_entry.get()
                  row = self.cursor.execute("SELECT * FROM employee_info WHERE employee_name = ?" , (name,)).fetchall()

      
                  if  name != '' and row != []:
                        # it will show image result in your desktop and function have been realized
                        imshow("Camera", image) 
                              
                        # saving image in local storage 
                        imwrite(r"Your working directory\Self-Portrait.png", image)

                        convertedPhoto = self.convertToBinaryData(r"Your current working directory\Self-Portrait.png")
                        time = strftime('%Y-%m-%d %H:%M:%S %p %a')

                        self.cursor.execute("INSERT INTO beginWork_records (name, beginWork_photo,time) VALUES (?,?,?)", (name,convertedPhoto,time))

                        self.conn.commit()

                        messagebox.showinfo('Response', 'You will begin to work after break time')
                        cam.release()

                  else:
                        messagebox.showinfo('Response', 'Camera does not capture and save photo, or you must input correct employee name')
                        cam.release()

                  # If keyboard interrupt occurs, destroy image  
                  # window will be closed after 5000 milliseconds(5 seconds)
                  waitKey(5000) 
                  destroyWindow("Camera") 
                  cam.release()
      
            else: 
                  messagebox.showinfo('Response', 'You need to set up your default camera first ! ')


     except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)


    def clock_out(self):
     try:
            
            cam_port = 0
            cam = VideoCapture(cam_port) 
      
            # reading the input using the camera 
            result, image = cam.read() 
      
            # If image will detect without any error, and show result 
          
            if result: 
      
                  name = self.employee_name_entry.get()
                  row = self.cursor.execute("SELECT * FROM employee_info WHERE employee_name = ?" , (name,)).fetchall()
      
                  if  name != '' and row != []:
                        # it will show image result in your desktop and function have been realized
                        imshow("Camera", image) 
                              
                        # saving image in local storage 
                        imwrite(r"Your working directory\Self-Portrait.png", image)

                        convertedPhoto = self.convertToBinaryData(r"Your working directory\Self-Portrait.png")
                        time = strftime('%Y-%m-%d %H:%M:%S %p %a')

                        self.cursor.execute("INSERT INTO clockOut_records (name, clockOut_photo,time) VALUES (?,?,?)", (name,convertedPhoto,time))

                        self.conn.commit()

                        messagebox.showinfo('Response', 'You have clocked out and press any button to continue')
                        cam.release()

                  else:
                        messagebox.showinfo('Response', 'Camera does not capture and save photo, or you must input your name')
                        cam.release()

                  # If keyboard interrupt occurs, destroy image  
                  # window will be closed after 5000 milliseconds(5 seconds)
                  waitKey(5000) 
                  destroyWindow("Camera") 
                  cam.release()
      
            else: 
                  messagebox.showinfo('Response', 'You need to set up your default camera first ! ')


     except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
