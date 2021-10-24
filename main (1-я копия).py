from tkinter import* 
from tkcalendar import*
from datetime import date
import json

class TButton:
	def __init__(self, frame, text, c):
		self.button = Button(frame, text = text, command = self.fun)
		self.button.grid(row=0, column = c)
	def fun(self):
		pass

class TAdd(TButton):
	def fun(self):
		top_window = TTopWindow("Добавить")

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
		self.b1 = TAdd(self.frame, "Добавить", 0)
		self.b2 = Button(self.frame, text = "Урок проведен", command = self.lesson_finished)
		self.b2.grid(row = 0, column = 1)
		self.b3 = Button(self.frame, text = "Платеж", command = self.get_payment)
		self.b3.grid(row = 0, column = 2)
		self.b4 = Button(self.frame, text = "Информация", command = self.get_information)
		self.b4.grid(row = 0, column = 3)
		self.b5 = Button(self.frame, text = "Удалить", command = self.delete)
		self.b5.grid(row = 0, column = 4)
		self.b6 = Button(self.frame, text = "Поиск", command = self.search)
		self.b6.grid(row = 0, column = 5)
	def load_students(self):
		f = open("state.txt", "r")
		students = json.load(f)
		for student in students:
			self.listbox.insert(END, student["name"])
		f.close()
	def lesson_finished(self):
		TLessonFinishedWindow("Урок проведен", self.listbox.get(ANCHOR))
	def get_payment(self):
		TGetPaymentWindow("Платеж", self.listbox.get(ANCHOR))
	def get_information(self):
		name= self.listbox.get(ANCHOR)
		students = get_students()
		for student in students:
			if student["name"] == name:
				p = int(student["price"])
				a = int(student["amount"])
				self.label.configure(text = name +"   "+ str(a/p)+ " уроков")
	def delete(self):
		name = self.listbox.get(ANCHOR)
		students = get_students()
		for student in students:
			if student["name"] == name:
				students.remove(student)
		set_students(students)
		reload_list()
	def search(self):
		pass

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
		student = {"name": "",
					"amount": 0,
					"price": 0}
		student["name"] = self.name.entry.get()
		student["amount"] = self.amount.entry.get()
		student["price"] = self.price.entry.get()
		students = get_students()
		students.append(student)
		set_students(students)
		f1 = open("data_base.txt", "a")
		f1.write(student["name"]+"    "+"Платеж: "+str(student["amount"])+"    "+"Дата: "+self.calendar.get_date()+"\n")
		f1.close()
		self.top.destroy()
		reload_list(students)

class TLessonFinishedWindow(TTopWindow):
	def __init__(self, text, name):
		super().__init__(text)
		self.name_of_student = name
		students = get_students()
		for student in students:
			if student["name"] == name:
				self.amount_of_student = student["amount"]
				self.price_of_student = student["price"]
		self.name.entry.insert(0, self.name_of_student)
		self.amount.entry.insert(0, self.amount_of_student)
		self.price.entry.insert(0, self.price_of_student)
	def add(self):
		students = get_students()
		p = int(self.price_of_student)
		a = int(self.amount_of_student)-p
		for student in students:
			if student["name"] == self.name_of_student:
				student["amount"] = str(a)
		set_students(students)
		f1 = open("data_base.txt", "a")
		f1.write(self.name_of_student+"    "+"Урок проведен:     "+"Дата: "+self.calendar.get_date()+"\n")
		f1.close()
		self.top.destroy()

class TGetPaymentWindow(TTopWindow):
		def __init__(self, text, name):
			super().__init__(text)
			self.name_of_student = name
			self.name.entry.insert(0, self.name_of_student)
		def add(self):
			payment = int(self.amount.entry.get())
			students = get_students()
			for student in students:
				if student["name"] == self.name_of_student:
					student["amount"] = str(int(student["amount"])+payment)
			set_students(students)
			f1 = open("data_base.txt", "a")
			f1.write(self.name_of_student+"    "+"Платеж : "+str(payment)+"   "+"Дата: "+self.calendar.get_date()+"\n")
			f1.close()
			self.top.destroy()

class TSearchWindow:
	pass

def reload_list():
	students = get_students()
	for i in range(program.listbox.size()):
			program.listbox.delete(END)
	for i in students:
			program.listbox.insert(END, i["name"])

def get_students():
	f = open("state.txt", "r")
	students = json.load(f)
	f.close()
	return students

def set_students(students):
	f = open("state.txt", "w")
	json.dump(students, f)
	f.close()


root=Tk()
root.title("База данных учеников")

program = TProgram(root)
program.load_students()



root.mainloop()