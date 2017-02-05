""" Authour: Dickson Makale """

#Dependencies
from datetime import datetime
from time import gmtime, strftime
import time
import sys
import sqlite3

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
class_Table()


#Add student into the database
def student_add():
	print("----Student Add Portal----")
	print('')
	print("Thise portal helps new students Student_ID")
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
		print(names,',',"You've been Added into the register")
		print("Your student ID is ", key)
student_add()


#Check in a student
def check_in_student():
	print("Sign in before selecting a class")
	curs.execute("SELECT*FROM students")
	students_dict=dict([(row) for row in curs.fetchall()])
	student_ID_names=students_dict
	login_student_ID = int(input("Please enter your Student ID.\n"))
    login_student_names = str(input("Please enter your Names.\n"))
    #strip any whitespace from the ends of the input
    login_student_names=login_student_names.strip()
    #authenticate logins
    if login_student_ID in student_ID_names and login_student_names == student_ID_names[login_student_ID]:
        print("Logged in")

    else:
    	print("Wrong credentials/not in register")
    	print("Not registered?")
    	print("Register your name to get an ID")





























