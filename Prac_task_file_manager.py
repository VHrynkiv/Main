from tkinter.filedialog import askdirectory
from tkcalendar import Calendar
from tkinter import messagebox
from datetime import datetime
from tkinter import *
import time
import os

window = Tk()

window['bg'] = '#fafafa'
window.title('file manager')
window.geometry('300x250')

folder = ''

def choise_folder():
    global folder
    folder = askdirectory()
    
    if folder != '':
        os.chdir(folder)
        way = os.path.basename(folder)
        folder_name.configure(text=way)
    else:
        messagebox.showinfo("Помилка!!!", "Ви не обрали папку!")

def folder_info():
    number_of_files = 0
    weight_of_files = 0

    if folder != '':
        for dirpath, dirnames, filenames in os.walk("."):
            number_of_files += len(filenames)
            for i in filenames:
                weight_of_files += os.path.getsize(os.path.join(dirpath, i))
        messagebox.showinfo("Дані про папку", f"Кількість файлів: {number_of_files}\nВага файлів: {weight_of_files} байт")
    else:
        messagebox.showinfo("Помилка!!!", "Ви не обрали папку!")


def edited_files():
    if folder != '':
        edited_window = Tk()
        edited_window.title("Файли")
        file_list = Listbox(edited_window, selectmode=EXTENDED)
        scroll_file_list = Scrollbar(edited_window, orient=VERTICAL, command=file_list.yview)
        scroll_file_list.pack(side=RIGHT, fill=Y)
        file_list.pack(side=LEFT)

        way_list = []

        for dirpath, dirnames, filenames in os.walk("."):
                for i in filenames:
                    file_list.insert(END, i)
                    way_list.append(os.path.join(dirpath, i))

        def choice_date():
            calendar_window = Tk()
            calendar_window.title("Вибір дати")
            calendar_text = Label(calendar_window, text="Редаговані раніше").pack()
            cal = Calendar(calendar_window, selectmode = 'day', year = 2022, month = 2, day = 24)
            cal.pack(pady = 20)

            def get_date():
                raw_date = cal.get_date()
                reformat_date = datetime.strptime(raw_date, "%d.%m.%Y")
                unix_time = time.mktime(reformat_date.timetuple())
                while len(way_list) > 0:
                    way_list.pop(0)
                    file_list.delete(0)
                for dirpath, dirnames, filenames in os.walk("."):
                    for i in filenames:
                        if time.time() - os.path.getmtime(os.path.join(dirpath, i)) > time.time() - unix_time:
                            file_list.insert(END, i)
                            way_list.append(os.path.join(dirpath, i))
                calendar_window.destroy()
            Button(calendar_window, text = "Вибрати", command = get_date).pack()

            calendar_window.mainloop()

        def delete_file():
            select = list(file_list.curselection())
            if len(select) != 0:
                select.reverse()
                for e in select:
                    file_list.delete(e)
                    os.remove(way_list[e])
                    way_list.pop(e)


        delete_file_button = Button(edited_window, text = "Видалити", command = delete_file).pack()
        choice_date_button = Button(edited_window, text = "Дата зміни", command = choice_date).pack()
    
        edited_window.mainloop()
    else:
        messagebox.showinfo("Помилка!!!", "Ви не обрали папку!")

folder_name = Label(window, text = "Назва папки")
folder_name.pack()

choise_folder_button = Button(window, text = "Вибрати папку", command = choise_folder).pack()

get_info_button = Button(window, text = "Отримати дані", command = folder_info).pack()

get_edited_button = Button(window, text = "Змінені файли", command = edited_files).pack()

window.mainloop()
