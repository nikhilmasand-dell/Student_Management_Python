#Libraries:-
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from PIL import ImageTk,Image
import mysql.connector
import socket
import requests
import bs4
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

#Declaring the user-defined exception class
class MyEx(Exception):
	def __init__(self,msg):
		self.msg = msg

#Declaring the GUI elements
root = Tk()
root.title("Student Management System")
root.geometry("640x450+400+200")

#Initialising the database and table:-
con = None
cursor = None
try:
	con = mysql.connector.connect(user = 'root',password = 'abc456',host = 'localhost')
	print("Connected to database")
	cursor = con.cursor()
	sql1 = "create database if not exists student;"
	cursor.execute(sql1)
	sql3 = "use student;"
	cursor.execute(sql3)
	sql2 = "create table if not exists student(rno int primary key, name varchar(30), marks int);"
	cursor.execute(sql2)
	print("Table Student created")
except Exception as e:
	messagebox.showerror(e)
	con.rollback()
finally:
	cursor.close()
	if con is not None:
		con.close()

#Events by Buttons:-

#Add a student button action
def f1():
	root.withdraw()
	addst.deiconify()

#Adding the student into database
def f2():
	con = None
	cursor = None

	try:
		con = mysql.connector.connect(user = 'root', password = 'abc456', host = 'localhost',database = 'student')
		cursor = con.cursor()
		name = entNameAdd.get()
		rno = int(entRnoAdd.get())
		marks = int(entMarksAdd.get())

		if (name =='' or rno =='' or marks ==''):
			raise MyEx("Entry fields can't be empty")
		if name.isalpha():
			pass
		else:
			raise MyEx("Name should contain only characters")
		if (rno<=0):
			raise MyEx("Roll Number Should be a positive non zero integer")
		if (marks<0 or marks>100):
			raise MyEx("Marks should be between 0 to 100")
		sql = "insert into student values('%d','%s','%d')"
		args = (rno,name,marks)
		cursor.execute(sql % args)
		con.commit()
		msg = name + " Added to database"
		messagebox.showinfo("Information", msg)
		entRnoAdd.delete(0,END)
		entNameAdd.delete(0,END)
		entMarksAdd.delete(0,END)
		entRnoAdd.focus()

	except MyEx as me:
		messagebox.showerror("Error",me)
	except ValueError as v:
		messagebox.showerror("Error","Enter integer in roll Number and Marks")
	except Exception as e:
		messagebox.showerror("Error",str(e))

	finally:
		if con is not None:
			con.rollback()
			con.close()

#Back button action in add window
def f3():
	addst.withdraw()
	root.deiconify()


#View action and Viewing student from database
def f4():
	viewst.deiconify()
	root.withdraw()
	con = None
	cursor = None
	try:
		stData.delete('1.0',END)
		con = mysql.connector.connect(user='root', password = 'abc456', host = 'localhost', database = 'student')
		cursor = con.cursor()
		sql = "select * from student;"
		cursor.execute(sql)
		data = cursor.fetchall()
		msg= ""
		stData.insert(INSERT, "Roll     Name    Marks\n")
		for d in data:
			msg += "  " +str(d[0]) +"      "+ str(d[1]) +"    "+ str(d[2])+"\n"
		stData.insert(INSERT, msg)
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()	

#Back action button on view window
def f5():
	viewst.withdraw()
	root.deiconify()



#Update button action
def f6():
	upst.deiconify()
	root.withdraw()

#Updating the student in database
def f10():
	con = None
	cursor = None
	try:
		rno=[]
		con = mysql.connector.connect(user = 'root', password = 'abc456', host = 'localhost', database = 'student')
		cursor = con.cursor()
		srno = int(entRnoUp.get())
		sname = entNameUp.get()
		smarks = int(entMarksUp.get())
	
		if (sname is None or srno is None or smarks is None):
			raise MyEx("Entry fields can't be empty")
		if sname.isalpha():
			pass
		else:
			raise MyEx("Name should be contain only characters")
		if (srno<=0):
			raise MyEx("Roll Number Should be a positive non zero integer")
		if (smarks<0 or smarks>100):
			raise MyEx("Marks should be between 0 to 100")
		
		sql = "select * from student;"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			rno.append(d[0])

		if srno in rno:
			sql = "update student set name = '%s', marks = '%d' where rno = '%d'"
			args = (sname,smarks,srno)
			cursor.execute(sql % args)
			con.commit()
			msg = "Roll-no: "+ str(srno) + " Updated in database"
			messagebox.showinfo("Information", msg)
			entRnoUp.delete(0,END)
			entNameUp.delete(0,END)
			entMarksUp.delete(0,END)
			entRnoUp.focus()
		else:
			raise MyEx("This roll number does not exists in database")

	except MyEx as me:
		messagebox.showerror("Error",me)
	except ValueError as v:
		messagebox.showerror("Error","Enter integer in roll Number and Marks")
	except Exception as e:
		con.rollback()
		messagebox.showerror("Error",e)
	finally:
		cursor.close()
		if con is not None:
			con.close()

#Back action on update window
def f7():
	upst.withdraw()
	root.deiconify()

#Delete button action
def f8():
	delst.deiconify()
	root.withdraw()

#Deleting the student from database
def f11():
	rno = []
	con = None
	cursor = None
	try:
		con = mysql.connector.connect(user = 'root',password = 'abc456',host = 'localhost',database = 'student')
		srno = int(entRnoDel.get())
		cursor = con.cursor()
		if srno is None:
			raise MyEx("Roll number entry can't be empty")
		if (srno<=0):
			raise MyEx("Roll Number Should be a positive non zero integer")
		
		sql = "select * from student;"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			rno.append(d[0])

		if srno in rno:
			sql = "delete from student where rno = '%d'"
			args = (srno)
			cursor.execute(sql % args)
			con.commit()
			msg = "Roll-no: "+ str(srno) + " deleted in database"
			messagebox.showinfo("Information", msg)
			entRnoDel.delete(0,END)
			entRnoDel.focus()
		else:
			raise MyEx("Roll number to be deleted is not present in database")
	except MyEx as me:
		messagebox.showerror("Error",me)
	except ValueError as v:
		messagebox.showerror("Error","Enter integer in roll Number")
	except Exception as e:
		con.rollback()
		messagebox.showerror("Error",e)

	finally:
		cursor.close()
		if con is not None:
			con.close()


#Back button action on delete window
def f9():
	delst.withdraw()
	root.deiconify()

#Graph Button action and graphic representation of marks of students
def f12():
	con = None
	cursor = None
	name = []
	marks = []
	try:
		con = mysql.connector.connect(user='root', password = 'abc456', host = 'localhost', database = 'student')
		cursor = con.cursor()
		sql = "select * from student;"
		cursor.execute(sql)
		data = cursor.fetchall()

		if data is None:
			raise MyEx("No students present in database")
		for d in data:
			name.append(d[1])
			marks.append(d[2])
		#x = np.arange(len(marks))
		plt.bar(name,marks,label="Marks of students",width = 0.3)
		plt.title("Marks of Students")
		plt.xlabel('Names',fontsize = 10)
		plt.ylabel('Marks',fontsize = 10)
		plt.legend()
		plt.grid()
		plt.show()
	except Exception as e:
		messagebox.showerror("Error", str(e))
	finally:
		if con is not None:
			con.close()	


#Connecting to internet and retrieving city,temperature and quote of the day.
try:	
	socket.create_connection(("www.google.com", 80))
	print("connected to internet")
	res = requests.get("https://ipinfo.io/")
	print(res)
	data = res.json()
	city = data['city']
	print("City is "+city)
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q="+ str(city)
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address = a1 + a2 + a3
	res1 = requests.get(api_address)
	print(res1)
	data = res1.json()
	main = data['main']
	temperature = main['temp']
	res = requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
	print(res)
	soup = bs4.BeautifulSoup(res.text,'lxml')
	quote = soup.find('img',{"class":"p-qotd"})
	quote = quote['alt']


except OSError:
	messagebox.showerror("Error","Connection failed")

j = 0
templist1 = []
templist2 = []
qList = quote.split(' ')
for i in range(len(qList)//2):
	templist1.append(qList[i])
	j = i

for i in range(j+1,len(qList)):
	templist2.append(qList[i])

msga = ' '.join(templist1)
msgb = ' '.join(templist2)


#Installing the canvas on root and adding a background image and placing the button-windows,messages
canvas = Canvas(root,width = 700, height = 550)
canvas.pack()

bgImage = ImageTk.PhotoImage(Image.open('bgimage.jpg'))
canvas.create_image(320,225,image = bgImage)

canvas.create_text(300,20,fill="black",font="Times 20 italic bold",text="Student Management System")

canvas.create_line(15, 40, 620, 40)

btnAdd = Button(root,text = 'Add',width = 15, font = ('roman',25,'bold'), command = f1)
btnAddWindow =canvas.create_window(300,90, window = btnAdd)
 
btnView = Button(root,text = 'View',width = 15, font = ('roman',25,'bold'), command = f4)
btnViewWindow =canvas.create_window(300,140, window = btnView)

btnUpdate = Button(root,text = 'Update',width = 15, font = ('roman',25,'bold'), command = f6)
btnUpdateWindow =canvas.create_window(300,190, window = btnUpdate)

btnDelete = Button(root,text = 'Delete',width = 15, font = ('roman',25,'bold'), command = f8)
btnDeleteWindow =canvas.create_window(300,240, window = btnDelete)

btnGraph = Button(root,text = 'Graph',width = 15, font = ('roman',25,'bold'),command = f12)
btnGraphWindow =canvas.create_window(300,290, window = btnGraph)

canvas.create_text(100,350,fill="black",font="Times 20 italic bold",text="QOTD: ")
msg1 = msga + "\n" + msgb
canvas.create_text(350,350,fill="black",font="Times 20 italic bold",text=msg1)

canvas.create_text(200,400,fill="black",font="Times 20 italic bold",text="Temperature: ")
msg2 = str(temperature) + "\u00b0" + "C in " + city
canvas.create_text(350,400,fill="black",font="Times 20 italic bold",text=msg2)


#Adding the student window
addst = Toplevel(root)
addst.title("Add a Student")
addst.geometry("400x400+500+300")

lblRno = Label(addst, text = "Roll Number:", font = ('roman',20,'bold'))
lblRno.pack(pady = 5)

entRnoAdd = Entry(addst, bd = 5)
entRnoAdd.pack()

lblName = Label(addst, text = "Name:", font = ('roman',20,'bold'))
lblName.pack(pady = 5)

entNameAdd = Entry(addst, bd = 5)
entNameAdd.pack()

lblMarks = Label(addst, text = "Marks:", font = ('roman',20,'bold'))
lblMarks.pack(pady = 5)

entMarksAdd = Entry(addst, bd = 5)
entMarksAdd.pack()

btnAddstSave = Button(addst, text = "Save", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black',command = f2)
btnAddstSave.pack(pady = 30)

btnAddstBack = Button(addst, text = "Back", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black',command = f3)
btnAddstBack.pack()

addst.withdraw()


#Viewing the students window

viewst = Toplevel(root)
viewst.title("Student Details")
viewst.geometry("400x400+500+300")

stData = scrolledtext.ScrolledText(viewst, width = 30, height = 20)
stData.pack(pady = 20)

btnViewstBack = Button(viewst, text = "Back", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black', command = f5)
btnViewstBack.pack()

viewst.withdraw()


#Updating the student window
upst = Toplevel(root)
upst.title("Update the Student")
upst.geometry("400x400+500+300")

lblRno = Label(upst, text = "Roll Number:", font = ('roman',20,'bold'))
lblRno.pack(pady = 5)

entRnoUp = Entry(upst, bd = 5)
entRnoUp.pack()

lblName = Label(upst, text = "Name:", font = ('roman',20,'bold'))
lblName.pack(pady = 5)

entNameUp = Entry(upst, bd = 5)
entNameUp.pack()

lblMarks = Label(upst, text = "Marks:", font = ('roman',20,'bold'))
lblMarks.pack(pady = 5)

entMarksUp = Entry(upst, bd = 5)
entMarksUp.pack()

btnUpstSave = Button(upst, text = "Save", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black', command = f10)
btnUpstSave.pack(pady = 30)

btnUpstBack = Button(upst, text = "Back", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black', command = f7)
btnUpstBack.pack()

upst.withdraw()


#Deleting a student window
delst = Toplevel(root)
delst.title("Delete the Student")
delst.geometry("400x400+500+300")

lblRno = Label(delst, text = "Roll Number:", font = ('roman',20,'bold'))
lblRno.pack(pady = 5)

entRnoDel = Entry(delst, bd = 5)
entRnoDel.pack()

btnDelstSave = Button(delst, text = "Save", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black', command = f11)
btnDelstSave.pack(pady = 30)

btnDelstBack = Button(delst, text = "Back", font = ('arial',25,'bold'), width = 15,fg='black',highlightbackground='black', command = f9)
btnDelstBack.pack()

delst.withdraw()



#Running of GUI
root.mainloop()#Running of GUI
root.mainloop()