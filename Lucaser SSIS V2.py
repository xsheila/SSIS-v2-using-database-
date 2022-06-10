from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
import tkinter.messagebox
import os
import sqlite3
from turtle import bgcolor

class sis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        all_frame = tk.Frame(self)
        all_frame.pack(side="top", fill="both", expand = True)
        all_frame.rowconfigure(0, weight=1)
        all_frame.columnconfigure(0, weight=1)
        self.frames = {}
        for F in (Students, Home, Courses):
            frame = F(all_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show(Home)
    def show(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

def iExit():
            iExit = tkinter.messagebox.askyesno("Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
class Home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent) 
        label = tk.Label(self, text="Student Information system \nUsing Database",borderwidth=8, font=("Courier", 40), bg=("DARK BLUE"), fg=("white"))
        label.place(x=0,y=5,width=1250,height=500)

        label = tk.Label(self, text="Sheila Mae Lucaser",borderwidth=8, font=("Courier", 15), bg=("DARK BLUE"), fg=("white"))
        label.place(x=0,y=5,width=1250,height=50)

        course = tk.Button(self, text="COLLEGE COURSES",font=("Courier",20),bd=5, width = 16, height = 1, fg="white",bg="DARK BLUE", command=lambda: controller.show(Courses))
        course.place(x=100,y=520)
        course.config(cursor= "hand2")
        
        students = tk.Button(self, text="STUDENT",font=("Courier",20),bd=5, width = 13 , height = 1, fg="white",bg="DARK BLUE", command=lambda: controller.show(Students))
        students.place(x=500,y=520)
        students.config(cursor= "hand2")

        students = tk.Button(self, text="EXIT",font=("Courier",20),bd=5, width = 13, height = 1, fg="white",bg="DARK BLUE", command=iExit)
        students.place(x=900,y=520)
        students.config(cursor= "hand2")
        
class Courses(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        Course_Code = StringVar()
        Course_Name = StringVar()
        SearchBar_Var = StringVar()
        
        def tablec():
            conn = sqlite3.connect("sdm.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS courses ( \
                        Course_Code TEXT PRIMARY KEY, \
                        Course_Name TEXT)") 
            conn.commit() 
            conn.close()
            
        def add_course():
            if Course_Code.get() == "" or Course_Name.get() == "" : 
                tkinter.messagebox.showinfo("Error", "Input information")
            else:
                conn = sqlite3.connect("sdm.db")
                c = conn.cursor()         
                c.execute("INSERT INTO courses(Course_Code,Course_Name) VALUES (?,?)",(Course_Code.get(),Course_Name.get()))        
                conn.commit()           
                conn.close()
                Course_Code.set('')
                Course_Name.set('') 
                tkinter.messagebox.showinfo("Success", "Course added successfully!")
                display_course()
              
        def display_course():
            self.course_list.delete(*self.course_list.get_children())
            conn = sqlite3.connect("sdm.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
        
        def update_course():
            for selected in self.course_list.selection():
                conn = sqlite3.connect("sdm.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE courses SET Course_Code=?, Course_Name=? WHERE Course_Code=?", (Course_Code.get(),Course_Name.get(), self.course_list.set(selected, '#1')))  
                conn.commit()
                tkinter.messagebox.showinfo("Success", "Record updated successfully!")
                display_course()
                clear()
                conn.close()
                
        def edit_course():
            x = self.course_list.focus()
            if x == "":
                tkinter.messagebox.showerror("Error", "Select a course!")
                return
            values = self.course_list.item(x, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1])
                    
        def delete_course(): 
            try:
                messageDelete = tkinter.messagebox.askyesno("Warning", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sdm.db")
                    cur = con.cursor()
                    x = self.course_list.selection()[0]
                    id_no = self.course_list.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("DELETE FROM courses WHERE Course_Code = ?",(id_no,))                   
                    con.commit()
                    self.course_list.delete(x)
                    tkinter.messagebox.showinfo("Success", "Record deleted successfully!")
                    display_course()
                    con.close()                    
            except:
                tkinter.messagebox.showerror("Warning", "This course has students!")
                
        def search_course():
            Course_Code = SearchBar_Var.get()                
            con = sqlite3.connect("sdm.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE Course_Code = ?",(Course_Code,))
            con.commit()
            self.course_list.delete(*self.course_list.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.course_list.insert("", tk.END, text=row[0], values=row[0:])
            con.close()

        def iExit():
            iExit = tkinter.messagebox.askyesno("Student Information System","Confirm if you want to exit")
            if iExit > 0:
                root.destroy()
                return
        def clear():
            Course_Code.set('')
            Course_Name.set('') 
            
        def OnDoubleclick(event):
            item = self.course_list.selection()[0]
            values = self.course_list.item(item, "values")
            Course_Code.set(values[0])
            Course_Name.set(values[1]) 

        home = tk.Button(self, text="BACK",font=("Times New Roman",13,"bold"),bd=0, width = 17, bg="#eb906e", fg="white", command=lambda: controller.show(Home))
        home.place(x=14,y=20, height=35)
        home.config(cursor= "hand2")

        students = tk.Button(self, text="STUDENT DETAILS",font=("Times New Roman",13,"bold"),bd=0, width = 17 , fg="white",bg="#eb906e",command=lambda: controller.show(Students))
        students.place(x=1090,y=20, height=35)
        students.config(cursor= "hand2")

        label = tk.Label(self, bg=("NAVY BLUE"))
        label.place(x=10,y=60,width=180,height=670)
        
        label = tk.Label(self, bg=("NAVY BLUE"))
        label.place(x=1090,y=60,width=180,height=670)

        label = tk.Label(self, text="COURSES", font=("Times New Roman", 40),bg=("NAVY BLUE"))
        label.place(x=200,y=20,width=880,height=700)
       
        self.lblccode = Label(self, font=("Times New Roman", 30, "bold"),bd=5,bg=("#eb906e"),fg=("white"),text="COURSE DETAILS", padx=2, pady=4)
        self.lblccode.place(x=200,y=20,width=880)

        self.lblccode = Label(self, font=("Times New Roman", 12, "bold"),bg=("NAVY BLUE"),fg=("#eb906e"),text="COURSE CODE:", padx=4, pady=4)
        self.lblccode.place(x=200,y=150)
        self.txtccode = Entry(self, font=("Times New Romane", 12, "bold"), textvariable=Course_Code,bd=0, bg="light gray", width=25)
        self.txtccode.place(x=330,y=150, height=25) 

        self.lblccode = Label(self, font=("Times New Roman", 12, "bold"),bg=("NAVY BLUE"),fg=("#eb906e"),text="COURSE CODE:", padx=4, pady=4)
        self.lblccode.place(x=350,y=100)

        self.lblcname = Label(self, font=("Times New Roman", 12,"bold"),bg=("NAVY BLUE"),fg=("#eb906e"), text=" COURSE NAME:", padx=4, pady=4)
        self.lblcname.place(x=700,y=150)
    
        self.txtcname = Entry(self, font=("Times New Roman", 12, "bold"), textvariable=Course_Name,bd=0,bg="light gray", width=25)
        self.txtcname.place(x=850,y=150, height=25)
        
        self.SearchBar = Entry(self, font=("Times New Roman", 12), textvariable=SearchBar_Var, bd=0,bg="light gray",width=27)
        self.SearchBar.place(x=540,y=100, height=25)

        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=963,y=250,height=430)

        self.course_list = ttk.Treeview(self, columns=("Course Code","Course Name"), height = 20, yscrollcommand=scrollbar.set)

        self.course_list.heading("Course Code", text="Course Code", anchor=W)
        self.course_list.heading("Course Name", text="Course Name",anchor=W)
        self.course_list['show'] = 'headings'

        self.course_list.column("Course Code",width=200, anchor=W, stretch=False)
        self.course_list.column("Course Name",width=430, stretch=False)
        
        self.course_list.bind("<Double-1> ", OnDoubleclick)

        self.course_list.place(x=330,y=250)
        scrollbar.config(command=self.course_list.yview)

        self.adds = Button(self, text="ADD", font=('Courier New', 16, 'bold'), height=1, width=10,bg="#eb906e", fg="white",command=add_course)
        self.adds.place(x=25,y=350)
        self.adds.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=('Courier New', 16, 'bold'), height=1, width=10, bg="#eb906e", fg="white", command=clear)
        self.clear.place(x=25,y=430)
        self.clear.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Courier New', 9, 'bold'), height=1, width=12, bg= "#eb906e", fg="darkslategray", command=search_course)
        self.search.place(x=820,y=98)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Courier New', 16, 'bold'), height=1, width=10, bg="#eb906e", fg="white", command=display_course)
        self.display.place(x=25,y=510)
        self.display.config(cursor= "hand2")
    
        self.delete = Button(self, text="DELETE", font=('Courier New', 16, 'bold'), height=1, width=10, bg="#eb906e", fg="white", command=delete_course)
        self.delete.place(x=1110,y=350)
        self.delete.config(cursor= "hand2")

        self.edit = Button(self, text="EDIT", font=('Courier New', 16, 'bold'), height=1, width=10, bg="#eb906e", fg="white", command=edit_course)
        self.edit.place(x=1110,y=430)
        self.edit.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Courier New', 16, 'bold'), height=1, width=10, bg="#eb906e", fg="white", command=update_course) 
        self.update.place(x=1110,y=510)
        self.update.config(cursor= "hand2")
        
        tablec()
        display_course()

class Students(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        label = tk.Label(self, text="COURSES", font=("Times New Roman", 40),bg=("NAVY BLUE"),fg=("#eb906e"))
        label.place(x=0,y=10,width=1280,height=650)

        label = tk.Label(self, bg=("NAVY BLUE"))
        label.place(x=10,y=60,width=180,height=670)
        
        label = tk.Label(self, bg=("NAVY BLUE"))
        label.place(x=1090,y=60,width=180,height=670)

        self.lblccode = Label(self, font=("Times New Roman", 30, "bold"),bd=5,bg=("#eb906e"),fg=("white"),text="STUDENT INFORMATION", padx=2, pady=4)
        self.lblccode.place(x=200,y=20,width=880)

        course = tk.Button(self, text="COURSES",font=("Times New Roman",13,"bold"),bd=0, width = 17, fg="white",bg="#eb906e", command=lambda: controller.show(Courses))
        course.place(x=14,y=20,height=35)
        course.config(cursor= "hand2")

        home = tk.Button(self, text="BACK",font=("Times New Roman",13,"bold"),bd=0, width = 17, bg="#eb906e", fg="white", command=lambda: controller.show(Home))
        home.place(x=1090,y=20, height=35)
        home.config(cursor= "hand2")
   
        Student_ID = StringVar()
        Student_Name = StringVar()       
        Student_YearLevel = StringVar()
        Student_Gender = StringVar()
        Course_Code = StringVar()
        SearchBar_Var = StringVar()
        

        def tables():
            conn = sqlite3.connect("sdm.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (\
                        Student_ID TEXT PRIMARY KEY, \
                        Student_Name TEXT, \
                        Course_Code TEXT, \
                        Student_YearLevel TEXT, \
                        Student_Gender TEXT, \
                        FOREIGN KEY(Course_Code) REFERENCES courses(Course_Code) ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()    
        
        def add_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Eror", "Fill in the box")
            else:  
                ID = Student_ID.get()
                ID_list = []
                for i in ID:
                    ID_list.append(i)
                a = ID.split("-")
                if len(a[0]) == 4:        
                    if "-" in ID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("SIS", "ID Format:YYYY-NNNN")
                        else:
                            x = ID.split("-")  
                            year = x[0]
                            number = x[1]
                            if year.isdigit()==False or number.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Error", "Invalid ID")
                                except:
                                    pass
                            elif year==" " or number==" ":
                                try:
                                    tkinter.messagebox.showerror("Error", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("sdm.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                              
                                    c.execute("INSERT INTO students(Student_ID,Student_Name,Course_Code,Student_YearLevel,Student_Gender) VALUES (?,?,?,?,?)",\
                                                          (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get()))                                       
                                                                       
                                    tkinter.messagebox.showinfo("Success", "Student added successfully!")
                                    conn.commit() 
                                    clear()
                                    display_stud()
                                    conn.close()
                                except:
                                    ids=[]
                                    conn = sqlite3.connect("sdm.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        ids.append(row[0])
                                    if ID in ids:
                                       tkinter.messagebox.showerror("Error", "ID already exists")
                                    else: 
                                       tkinter.messagebox.showerror("Error", "Course Unavailable")
                                   
                    else:
                        tkinter.messagebox.showerror("Error", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("Error", "Invalid ID")
                 
        def update_stud():
            if Student_ID.get() == "" or Student_Name.get() == "" or Course_Code.get() == "" or Student_YearLevel.get() == "" or Student_Gender.get() == "": 
                tkinter.messagebox.showinfo("Error", "Select a student")
            else:
                for selected in self.studentlist.selection():
                    conn = sqlite3.connect("sdm.db")
                    cur = conn.cursor()
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute("UPDATE students SET Student_ID=?, Student_Name=?, Course_Code=?, Student_YearLevel=?,Student_Gender=?\
                          WHERE Student_ID=?", (Student_ID.get(),Student_Name.get(),Course_Code.get(),Student_YearLevel.get(), Student_Gender.get(),\
                              self.studentlist.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("Success", "Record updated successfully!")
                    display_stud()
                    clear()
                    conn.close()
        
        def delete_stud():   
            try:
                messageDelete = tkinter.messagebox.askyesno("Warning!", "Are you sure you want to delete this record?")
                if messageDelete > 0:   
                    con = sqlite3.connect("sdm.db")
                    cur = con.cursor()
                    x = self.studentlist.selection()[0]
                    id_no = self.studentlist.item(x)["values"][0]
                    cur.execute("DELETE FROM students WHERE Student_ID = ?",(id_no,))                   
                    con.commit()
                    self.studentlist.delete(x)
                    tkinter.messagebox.showinfo("Success", "Record successfully deleted!")
                    display_stud()
                    clear()
                    con.close()                    
            except Exception as e:
                print(e)
                
        def search_stud():
            Student_ID = SearchBar_Var.get()
            try:  
                con = sqlite3.connect("sdm.db")
                cur = con.cursor()
                cur .execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                con.commit()
                self.studentlist.delete(*self.studentlist.get_children())
                rows = cur.fetchall()
                for row in rows:
                    if row[0].startswith(Student_ID):
                        self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
                con.close()
            except:
                tkinter.messagebox.showerror("Error", "Invalid ID")           
                
        def display_stud():
            self.studentlist.delete(*self.studentlist.get_children())
            conn = sqlite3.connect("sdm.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                self.studentlist.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
                            
        def edit_stud():
            x = self.studentlist.focus()
            if x == "":
                tkinter.messagebox.showerror("Error", "Select record")
                return
            values = self.studentlist.item(x, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        
        def clear():
            Student_ID.set('')
            Student_Name.set('') 
            Student_YearLevel.set('')
            Student_Gender.set('')
            Course_Code.set('')
            
        def OnDoubleClick(event):
            item = self.studentlist.selection()[0]
            values = self.studentlist.item(item, "values")
            Student_ID.set(values[0])
            Student_Name.set(values[1])
            Course_Code.set(values[2])
            Student_YearLevel.set(values[3])
            Student_Gender.set(values[4])
        

        self.lblid = Label(self, font=("Courier New", 12,"bold"),bg="NAVY BLUE",fg="#eb906e", text="ID Number:", padx=4, pady=4)
        self.lblid.place(x=220,y=250)
        self.txtid = Entry(self, font=("Courier New", 13), textvariable=Student_ID, width=16, bd=0, bg="lightgray")
        self.txtid.place(x=220,y=300,height=25)

        self.lblname = Label(self, font=("Courier New", 12,"bold"),bg="NAVY BLUE",fg="#eb906e", text="Student Name:", padx=4, pady=4)
        self.lblname.place(x=350,y=150)
        self.txtname = Entry(self, font=("Courier New", 12), textvariable=Student_Name, width=25, bd=0, bg="lightgray")
        self.txtname.place(x=559,y=150,height=25)
        
        self.lblc = Label(self, font=("Courier New", 12,"bold"),bg="NAVY BLUE",fg="#eb906e", text="Course Code:", padx=4, pady=4)
        self.lblc.place(x=220,y=350)
        self.txtyear = Entry(self, font=("Courier New", 12), textvariable=Course_Code, width=15,bd=0, bg="lightgray")
        self.txtyear.place(x=220,y=400,height=25)
        

        self.lblyear = Label(self, font=("Courier New", 12,"bold"),bg="NAVY BLUE",fg="#eb906e", text="Year Level:", padx=4, pady=4)
        self.lblyear.place(x=220,y=450)
        self.txtyear = Entry(self, font=("Courier New", 13), textvariable=Student_YearLevel, width=16, bd=0, bg="lightgray")
        self.txtyear.place(x=220,y=500,height=25)
        
        self.lblgender = Label(self, font=("Courier New", 13,"bold"),bg="NAVY BLUE",fg="#eb906e", text="Gender:", padx=4, pady=4)
        self.lblgender.place(x=220,y=550)
        self.txtgender = Entry(self, font=("Courier New", 13), textvariable=Student_Gender, width=15, bd=0, bg="lightgray")
        self.txtgender.place(x=220,y=600,height=25)

        self.SearchBar = Entry(self, font=("Courier New", 12), textvariable=SearchBar_Var, bd=0,bg="lightgray", width=25)
        self.SearchBar.place(x=560,y=100, height=25)

        self.lblccode = Label(self, font=("Courier New", 12, "bold"),bg=("NAVY BLUE"),fg=("#eb906e"),text=" Student ID Number:", padx=4, pady=4)
        self.lblccode.place(x=340,y=100)
        
        scrollbar = Scrollbar(self, orient=VERTICAL)
        scrollbar.place(x=1031,y=250,height=390)

        self.studentlist = ttk.Treeview(self, columns=("ID No", "Name", "Course Code", "Year Level", "Gender"), height = 18, yscrollcommand=scrollbar.set)

        self.studentlist.heading("ID No", text="ID No", anchor=W)
        self.studentlist.heading("Name", text="Name",anchor=W)
        self.studentlist.heading("Course Code", text="Course Code",anchor=W)
        self.studentlist.heading("Year Level", text="Year Level",anchor=W)
        self.studentlist.heading("Gender", text="Gender",anchor=W)
        self.studentlist['show'] = 'headings'

        self.studentlist.column("ID No", width=100, anchor=W, stretch=False)
        self.studentlist.column("Name", width=200, stretch=False)
        self.studentlist.column("Course Code", width=130, anchor=W, stretch=False)
        self.studentlist.column("Year Level", width=100, anchor=W, stretch=False)
        self.studentlist.column("Gender", width=100, anchor=W, stretch=False)
        
        self.studentlist.bind("<Double-1>",OnDoubleClick)

        self.studentlist.place(x=400,y=250)
        scrollbar.config(command=self.studentlist.yview)
        
        self.add = Button(self, text="ADD", font=('Courier', 16,'bold'), height=1, width=10, bd=1,  bg="#eb906e", fg="white",command=add_stud)
        self.add.place(x=25,y=190)
        self.add.config(cursor= "hand2")

        self.update = Button(self, text="UPDATE", font=('Courier', 16,'bold'), height=1, width=10, bd=1, bg="#eb906e", fg="white", command=update_stud)
        self.update.place(x=430,y=190)
        self.update.config(cursor= "hand2")

        self.clear = Button(self, text="CLEAR", font=('Courier', 16,'bold'), height=1, width=10, bd=1, bg="#eb906e", fg="white", command=clear)
        self.clear.place(x=1070,y=190)
        self.clear.config(cursor= "hand2")

        self.delete = Button(self, text="DELETE", font=('Courier', 16,'bold'), height=1, width=10, bd=1, bg="#eb906e", fg="white", command=delete_stud)
        self.delete.place(x=650,y=190)
        self.delete.config(cursor= "hand2")

        self.search = Button(self, text="SEARCH", font=('Courier', 9, 'bold'),bd=2,height=1, width=12, bg= '#eb906e', fg="white", command=search_stud)
        self.search.place(x=820,y=98)
        self.search.config(cursor= "hand2")

        self.display = Button(self, text="DISPLAY", font=('Courier', 16, 'bold'), height=1, width=10,bd=1,  bg="#eb906e", fg="white",command = display_stud)
        self.display.place(x=870,y=190)
        self.display.config(cursor= "hand2")

        self.edit = Button(self, text="EDIT", font=('Courier', 16, 'bold'),bd=1, height=1, width=10, bg="#eb906e", fg="white", command= edit_stud)
        self.edit.place(x=230,y=190)
        self.edit.config(cursor= "hand2")

        tables()
        display_stud()

root = sis()
root.geometry("1260x650")

root.mainloop()
