#Authour: Dickson Makale

#Dependencies
from datetime import datetime
from time import gmtime, strftime
import time
import sys
import sqlite3
import tkinter as TK

#SQLite DataTables

TABLES=sqlite3.connect('Classes_Students.db')
curs=TABLES.cursor()

#Student Table
def student_table():
    curs.execute('CREATE TABLE IF NOT EXISTS students(Student_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Name TEXT NOT NULL)')
student_table()

#Class Table
def class_table():
    curs.execute("CREATE TABLE IF NOT EXISTS classes(Class_ID INTEGER PRIMARY KEY AUTOINCREMENT,\
                Class_Name TEXT NOT NULL, Time TEXT, Satatus TEXT NOT NULL)")
#class_table()


#Add student into the database
def student_add():
    print("---Student Add Portal---")
    print('')
    print("This portal helps new students get Student_ID")
    print('')
    print("Please Enter Your Names")
    names=input("Full Names: ")
    curs.execute('INSERT INTO students(Student_ID, Name)VALUES(null,?)', (names,))
    TABLES.commit()

    time.sleep(1)
    curs.execute("SELECT*FROM students WHERE Name=?", (names,))
    N_=[(curs.fetchone())]
    N_dict=dict(N_)
    for key in N_dict.keys():
        print(names,", You've been Added into the register")
        print("")
        print("Your student ID is ", key)
#student_add()


#Check in a student
def check_in_student():
    print("")
    print("---|Sign in before selecting a class|---")
    curs.execute("SELECT*FROM students")
    students_dict=dict([(row) for row in curs.fetchall()])
    student_ID_names=students_dict
    login_student_ID = int(input("    Please enter your Student ID.\n    "))
    login_student_names = str(input("    Please enter your Names.\n    "))
    #strip any whitespace from the ends of the input
    login_student_names=login_student_names.strip()
    #authenticate logins
    if login_student_ID in student_ID_names and login_student_names == student_ID_names[login_student_ID]:
        print("Logged in")

        #Return list of classes frm class_table
        def class_list():
            input("---|Press ENTER to view available classes|---")
            curs.execute("SELECT DISTINCT Class_ID, Class_Name FROM classes")
            print("_______________________________")
            print("Class_ID: ", "Class_Name")
            print("--------:----------------------")
            cls=[(row) for row in curs.fetchall()]
            dcls=dict(cls)
            d=""
            for i in dcls:
                a=i
                b=dcls
                c="|"+str(a)+"      :  "+dcls[i]
                d=d+c+'\n'
            print(d)
            print("--------------------------------")
            print("")

            #Select Class with Class_ID
            class_id=input("Select A Class - Enter Class_ID: ")
            var_class_id=int(class_id)
            print("")
            curs.execute("SELECT Class_Name FROM classes WHERE Class_ID=?", (var_class_id,))
            selected_class=curs.fetchall()
            for i in selected_class:
                print("---|You have selected: ", ''.join(i),"|---")
                print("")

            #Start Class
            accepts=input("If you wish to start your class now enter 'YES' : ")
            if accepts=="YES":
                print('')
        
            tim=(datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
            curs.execute("UPDATE classes SET Satatus='In Session' WHERE Class_ID=?", (var_class_id,))
            curs.execute("UPDATE classes SET Time=? WHERE Class_ID=?", (tim,var_class_id,))
            TABLES.commit()

            print('---|Classes in Session/not in Session|---')
            print('--------------------------------------------------------')
            curs.execute('SELECT*FROM classes')
            [print(": ".join(str(x) for x in(row))) for row in curs.fetchall()]
            print('--------------------------------------------------------')
            print('')

            #Count Doswn Timer
            def count_down():
                # start with 2 minutes --> 120 seconds
                for t in range(120, -1, -1):
                    # format as 2 digit integers, fills with zero to the left
                    # divmod() gives minutes, seconds
                    sf = "{:02d}:{:02d}".format(*divmod(t, 60))
                    #print(sf)  # test
                    time_str.set(sf)
                    root.update()
                    # delay one second
                    time.sleep(1)
            # create root/main window
            root = TK.Tk()
            time_str = TK.StringVar()
            # create the time display label, give it a large font
            # label auto-adjusts to the font
            label_font = ('helvetica', 40)
            TK.Label(root, textvariable=time_str, font=label_font, bg='white', 
                     fg='blue', relief='raised', bd=3).pack(fill='x', padx=5, pady=5)
            # create start and stop buttons
            # pack() positions the buttons below the label
            TK.Button(root, text='Start Class', command=count_down).pack()
            #TK.Button(root, text='Class In Progress', command=count_down).pack() 
            # stop simply exits root window
            TK.Button(root, text='End Class', command=root.destroy).pack()
            # start the GUI event loop
            root.mainloop()

            print(''.join(i), "in session")
            #print('')
            #time.sleep(15)

            tim=(datetime.now().strftime('%d-%b-%Y %H:%M:%S'))
            curs.execute("UPDATE classes SET Satatus='Not In Session' WHERE Class_ID=?", (var_class_id,))
            curs.execute("UPDATE classes SET Time=? WHERE Class_ID=?", (tim,var_class_id,))
            TABLES.commit()
            
            print('---|Classes in Session/not in Session|---')
            print('--------------------------------------------------------')
            curs.execute('SELECT*FROM classes')
            [print(": ".join(str(x) for x in(row))) for row in curs.fetchall()]
            print('--------------------------------------------------------')
            print('')
            
            print(''.join(i), "has ended")
            print('')
            print("You can now select a different class")
        class_list()
    else:
        print("Wrong credentials/not in register")
        print("Not registered?")
        print("Register your name to get an ID")

#check_in_student()

#Remove Student from Class List

def remove_student():
        print("REMOVE a student from the student list")
        print('')
        ID_input=input("Enter the Student_ID of the STUDENT you wish to REMOVE: ")
        int_ID_input=int(ID_input)

        curs.execute("DELETE FROM students WHERE Class_ID=?", (int_ID_input,))
        oooh.commit()

        curs.execute('SELECT * FROM students')
        cls=[(row) for row in curs.fetchall()]
        dcls=dict(cls)
        d=""
        for i in dcls:
            a=i
            b=dcls
            c=str(a)+":"+dcls[i]
            d=d+c+'\n'
        print(d)
#remove_student()

#Add class to the class list
def add_class():
    print('')
    input("ADD class?")
    class_input=input("Enter the Class you wish to ADD to the CLASS LIST: ")
    curs.execute('INSERT INTO classes(Class_ID, Class_Name, Satatus)VALUES(null,?,?)',(class_input, 'Not in Session',))
    TABLES.commit()

    print('')
    curs.execute("SELECT DISTINCT Class_ID, Class_Name FROM classes")
    print("_______________________________")
    print("Class_ID: ", "Class_Name")
    print("--------:----------------------")
    cls=[(row) for row in curs.fetchall()]
    dcls=dict(cls)
    d=""
    for i in dcls:
        a=i
        b=dcls
        c="|"+str(a)+"      :  "+dcls[i]
        d=d+c+'\n'
    print(d)
    print("--------------------------------")
    print("")
    print(''.join(class_input), "class has been added to the class list")
    
#add_class()

#Delete class from the class list
def delete_class():
    print("---|Delete a class from the Class list|---")
    print('')
    curs.execute("SELECT DISTINCT Class_ID, Class_Name FROM classes")
    print("_______________________________")
    print("Class_ID: ", "Class_Name")
    print("--------:----------------------")
    cls=[(row) for row in curs.fetchall()]
    dcls=dict(cls)
    d=""
    for i in dcls:
        a=i
        b=dcls
        c="|"+str(a)+"      :  "+dcls[i]
        d=d+c+'\n'
    print(d)
    print("--------------------------------")
    print("")
    
    Class_ID_input=input("Enter the Class_id of the Class you wish to DELETE: ")
    int_Class_ID_input=int(Class_ID_input)
    curs.execute("SELECT DISTINCT class_Name From classes WHERE Class_ID=?", (int_Class_ID_input,))
    _class=[(row) for row in curs.fetchone()]
    for i in _class:
        print(''.join(i), "has been deleted")
    curs.execute("DELETE FROM classes WHERE Class_id=?", (int_Class_ID_input,))
    TABLES.commit()
    

    curs.execute("SELECT DISTINCT Class_ID, Class_Name FROM classes")
    print("_______________________________")
    print("Class_ID: ", "Class_Name")
    print("--------:----------------------")
    cls=[(row) for row in curs.fetchall()]
    dcls=dict(cls)
    d=""
    for i in dcls:
        a=i
        b=dcls
        c="|"+str(a)+"      :  "+dcls[i]
        d=d+c+'\n'
    print(d)
    print("--------------------------------")
    print("")
    
#delete_class()























