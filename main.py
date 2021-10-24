from tkinter import *
import json
from tkcalendar import*
from datetime import date

class Line:
    def __init__(self,main,c,r,t):
        self.label=Label(main,text=t)
        self.entry=Entry(main)

        self.label.grid(row=r,column=c)
        self.entry.grid(row=r, column=c+1)

def get_payment():
    def add_to_base():
        for i in students:
            if i["name"] == name:
                a = int(i["amount"])
                a = a + int(amount_frame.entry.get())
                i['amount'] = str(a)
                f = open("state.txt", "w")
                json.dump(students, f)
        f1 = open("data_base.txt", "a")
        f1.write(name_frame.entry.get()+"    "+"Платеж: "+amount_frame.entry.get()+"    "+"Дата: "+cal.get_date()+"\n")
        f1.close()
        f=open("state.txt","w")
        json.dump(students, f)
        f.close()

        top.destroy()

    name = l.get(ANCHOR)

    top = Toplevel()
    top.title("Платеж")
    frame = LabelFrame(top, padx=10, pady=50)
    frame.grid(row=0, column=0)
    name_frame = Line(frame, 0, 0, "Имя")
    amount_frame = Line(frame, 0, 1, "Сумиа")
    price_frame = Line(frame, 0, 2, "Цена урока")
    name_frame.entry.insert(0,name)
    cal = Calendar(top, selectmode="day", year=year, month=month, day=day)
    cal.grid(row=0, column=2)

    add_button = Button(top, text="Добавить в список", command=add_to_base)
    add_button.grid(row=3, column=0)

def add():
    def get():
        student = {"name": "",
                   "amount": 0,
                   "price": 0}
        f = open("state.txt", "w")
        student["name"] = name.entry.get()
        student["amount"] = amount.entry.get()
        student["price"] = price.entry.get()
        students.append(student)
        json.dump(students, f)
        f.close()
        f1 = open("data_base.txt", "a")
        f1.write(name.entry.get()+"    "+"Платеж: "+amount.entry.get()+"    "+"Дата: "+cal.get_date()+"\n")
        f1.close()
        top.destroy()
        for i in range(l.size()):
            l.delete(END)
        for i in students:
            l.insert(END, i["name"])

    top=Toplevel()
    top.title("Добавть")
    frame=LabelFrame(top,padx=10,pady=50)
    frame.grid(row=0,column=0)
    name=Line(frame,0,0,"Имя")
    amount=Line(frame,0,1,"Сумиа")
    price=Line(frame,0,2,"Цена урока")



    cal=Calendar(top, selectmode="day", year=year, month=month, day=day)
    cal.grid(row=0, column=2)

    add_button=Button(top,text="Добавить в список",command=get)
    add_button.grid(row=3, column=0)

def show():
    name=l.get(ANCHOR)
    for i in students:
        if i["name"] == name:
            p = int(i['price'])
            a = int(i["amount"])
            label1.configure(text=i['name'] + "  " + str(a / p) + " уроков")

def lesson_finished():
    def add_to_base():
        f1=open("data_base.txt","a")
        f1.write(name+"    "+"Урок проведен"+"    "+"Дата: "+cal.get_date()+"\n")
        f1.close()
        top.destroy()
        for i in students:
            if i["name"] == name:
                p = int(i['price'])
                a = int(i["amount"])
                a = a - p
                i['amount'] = str(a)
                f = open("state.txt", "w")
                json.dump(students, f)
                f.close()
    name = l.get(ANCHOR)
    for i in students:
        if i["name"] == name:
            p = int(i['price'])
            a = int(i["amount"])
            i['amount'] = str(a)
            f = open("state.txt", "w")
            json.dump(students, f)
            f.close()
            top = Toplevel()
            top.title("Урок проведен")
            frame=LabelFrame(top,padx=10,pady=50)
            frame.grid(row=0,column=0)
            name_frame = Line(frame, 0, 0, "Имя")
            amount_frame = Line(frame, 0, 1, "Сумиа")
            price_frame = Line(frame, 0, 2, "Цена урока")
            name_frame.entry.insert(0,i["name"])
            amount_frame.entry.insert(0,i["amount"])
            price_frame.entry.insert(0,i["price"])
            cal = Calendar(top, selectmode="day", year=year, month=month, day=day)
            cal.grid(row=0, column=2)

            add_button = Button(top, text="Добавить в список", command=add_to_base)
            add_button.grid(row=3, column=0)

def search():
    name=l.get(ANCHOR)
    top=Toplevel()
    list_label=Label(top,text="",font=20)
    list_label.pack()
    #t=Text(top,width=10,height=5,font=("Ubntu",20))
    #t.pack()
    f1=open("data_base.txt","r")
    text=""
    for i in f1:
        if name in i:
            text=text+(i.strip()+"\n")
    list_label.configure(text=text)

def delete_item():
    name=l.get(ANCHOR)
    for i in students:
        if i["name"]==name:
            students.remove(i)
    l.delete(ANCHOR)
    f=open("state.txt","w")
    json.dump(students,f)
    f.close()

root=Tk()
root.title("База  данных учеников")

l=Listbox(root, width=30)
l.grid(row=0,column=0)

label1=Label(root,text="")
label1.grid(row=1, column=0)

frame=Frame(root,padx=20,pady=5)
frame.grid(row=2,column=0)

button1=Button(frame, text="Добавить", command=add)
button1.grid(row=0,column=0)

button2=Button(frame, text="Удалить", command=delete_item)
button2.grid(row=0,column=1)

button3=Button(frame, text="Информация",command=show)
button3.grid(row=0,column=2)

button4=Button(frame, text="Урок проведен", command=lesson_finished)
button4.grid(row=0,column=3)

button5=Button(frame, text="Платеж", command=get_payment)
button5.grid(row=0,column=4)

button6=Button(frame, text="Поиск", command=search)
button6.grid(row=0,column=5)

students=[]
f=open("state.txt","r")
students=json.load(f)
for i in students:
    l.insert(END,i["name"])
f.close()

today=date.today()

day=int(today.strftime("%d"))
month=int(today.strftime("%m"))
year=int(today.strftime("%Y"))


root.mainloop()