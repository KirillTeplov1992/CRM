from tkinter import* 
from tkcalendar import*
from datetime import date
import json

top_window_open = false


class TButton:
	def __init__(self, frame, text, c):
		self.button = Button(frame, text = text, command = self.fun)
		self.button.grid(row=0, column = c)
	def fun(self):
		pass

class TLine:
	def __init__(self, main, text, r):
		self.label = Label(main, text = text)
		self.label.grid(row = r, column = 0)
		self.entry = Entry(main)
		self.entry.grid(row = r, column = 1)
		
class TProgram:
	def __init__(self, master):
		self.listbox = Listbox(master)
		self.listbox.grid(row = 0, column = 0)
		self.frame = Frame(master)
		self.frame.grid(row = 3, column = 0)
		self.label = Label(master, text="")
		self.label.grid(row = 1, column = 0)
		self.b1 = Button(frame, text = "Добавить", command = self.add)
		self.b1.grid(row = 0, column = 0)
		self.b2 = Button(frame, text = "Урок проведен", command = self.lesson_finished)
		self.b2.grid(row = 0, column = 1)
	def load_students(self):
		f = open("state.txt", "r")
		students = json.load(f)
		for student in students:
			self.listbox.insert(END, student["name"])
		f.close()
	def add(self):
		global top_window_open 
		top_window_open = true
		top_window = TTopWindow("Добавить")


class TTopWindow:
	def __init__(self,text):
		today = date.today()
		self.day = int(today.strftime("%d"))
		self.month = int(today.strftime("%m"))
		self.year = int(today.strftime("%y"))
		self.top = Toplevel()
		self.top.title(text)
		self.top_frame = Frame(self.top)
		self.top_frame.grid(row = 0, column = 0)
		self.name = TLine(self.top_frame, "Имя", 0)
		self.amount = TLine(self.top_frame, "Сумма", 1)
		self.price = TLine(self.top_frame, "Цена урока", 2)
		self.calendar = Calendar(self.top, selectmode = "day", day = self.day, month = self.month, year = self.year)
		self.calendar.grid(row = 0, column = 2)
		self.button = Button(self.top, text = "Добавить в список", command = self.add)
		self.button.grid(row = 3, column = 2)
	def add(self):
		global top_window_open
		student = {"name": "",
					"amount": 0,
					"price": 0}
		student["name"] = self.name.entry.get()
		student["amount"] = self.amount.entry.get()
		student["price"] = self.price.entry.get()
		f = open("state.txt", "r")
		students = json.load(f)
		f.close()
		students.append(student)
		f = open("state.txt", "w")
		json.dump(students, f)
		f.close()
		f1 = open("data_base.txt", "a")
		f1.write(student["name"]+"    "+"Платеж: "+str(student["amount"])+"    "+"Дата: "+self.calendar.get_date()+"\n")
		f1.close()
		self.top.destroy()
		top_window_open = false

		#for i in range(master.listbox.size()):
		#	master.listbox.delite(END)
		#for i in students:
		#	master.listbox.insert(END, i["name"])
		

# Кнопка "Урок проведен"
class TLesson_finished (TButton):
	def fun(self):
		pass


		