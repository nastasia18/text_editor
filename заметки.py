from tkinter import *
from tkinter import messagebox, font, colorchooser
from tkinter.filedialog import askopenfile, asksaveasfile

file_name = NONE
global selected


def new_file():  # Создать новый файл
    text.delete("1.0", END)
    root.title("Новый файл")


def save_file():  # Просто сохранить файл
    data = text.get('1.0', END)
    out = open(file_name, 'w')
    out.write(data)
    out.close()


def save_as():  # Сохранить файл как
    files = [('Text Document', '*.txt'),  # В каком формате можно сохранить файл
             ('All Files', '*.*')]
    file = asksaveasfile(mode='w', title='Save File', filetypes=files, defaultextension=files)
    data = text.get('1.0', END)
    try:
        file.write(data.rstrip())
    except EXCEPTION:
        messagebox.showerror("Ой!", "Нельзя сохранить файл!")
    file.close()


def open_file():  # Открыть файл
    global file_name
    my_file = askopenfile(mode="r", title='Open File', filetypes=(('Text Document', '*.txt'), ('HTML Files', '*.html*'),
                                                                  ('Python Files', '*.py*'), ('All Files', '*.*')))
    if my_file is None:
        return
    file_name = my_file.name
    root.title(f'{file_name}')
    data = my_file.read()
    text.delete("1.0", END)
    text.insert("1.0", data)
    my_file.close()


# Вырезать текст
def cut_text(e):
    global selected
    # Если выбран текст при помощи клавиатуры
    if e:
        selected = root.clipboard_get()
    else:
        if text.selection_get():
            # Выделить выбранный текст из поля
            selected = text.selection_get()
            # Удалить выбранный текст из поля
            text.delete("sel.first", "sel.last")
            # Очистить буфер обмена и добавить текст
            root.clipboard_clear()
            root.clipboard_append(selected)


# Копировать текст
def copy_text(e):
    global selected
    # Если выбран текст при помощи клавиатуры
    if e:
        selected = root.clipboard_get()
    # Выделить выбранный текст из поля при помощи вкладки Копировать в меню
    if text.selection_get():
        selected = text.selection_get()
        # Очистить буфер обмена и добавить текст
        root.clipboard_clear()
        root.clipboard_append(selected)


# Вставить текст
def paste_text(e):
    global selected
    # Если выбран текст при помощи клавиатуры
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = text.index(INSERT)
            text.insert(position, selected)


def info():
    messagebox.showinfo("О программе", "Название: Текстовый редактор."
                                       "\nДанная программа предназначена для работы с текстом.")


def info_dev():
    messagebox.showinfo("О разработчике", "Разработчик: Заварина Анастасия\nСтудентка группы ИСП-318а")


def bold_it():
    bold_font = font.Font(text, text.cget("font"))
    bold_font.configure(weight="bold")

    text.tag_configure("bold", font=bold_font)

    # Определение текущих тегов
    current_tags = text.tag_names("sel.first")

    # Если тег не выбран, то выделить текст жирным шрифтом. Если выбран, снять выделение
    if "bold" in current_tags:
        text.tag_remove("bold", "sel.first", "sel.last")
    else:
        text.tag_add("bold", "sel.first", "sel.last")


def italics_it():
    italics_font = font.Font(text, text.cget("font"))
    italics_font.configure(slant="italic")

    text.tag_configure("italic", font=italics_font)

    # Определение текущих тегов
    current_tags = text.tag_names("sel.first")

    # Если тег не выбран, то выделить текст жирным шрифтом. Если выбран, снять выделение
    if "italic" in current_tags:
        text.tag_remove("italic", "sel.first", "sel.last")
    else:
        text.tag_add("italic", "sel.first", "sel.last")


# Выбор цвета текста
def text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        color_font = font.Font(text, text.cget("font"))

        text.tag_configure("colored", font=color_font, foreground=my_color)

        # Определение текущих тегов
        current_tags = text.tag_names("sel.first")

        # Если тег не выбран, то выделить текст жирным шрифтом. Если выбран, снять выделение
        if "colored" in current_tags:
            text.tag_remove("colored", "sel.first", "sel.last")
        else:
            text.tag_add("colored", "sel.first", "sel.last")


# Цвет фона
def bg_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        text.config(bg=my_color)


# Цвет шрифта
def all_text_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        text.config(fg=my_color)


root = Tk()  # Создание окна
root.title("Текстовый редактор")
root.geometry("600x600")

# Создание панели инструментов
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Создание фрейма
frame = Frame(root)
frame.pack()

# Создание скролл-бара
text_scroll = Scrollbar(root)
text_scroll.pack(side=RIGHT, fill=Y)

# Создание текстового поля
text = Text(root, width=500, height=500, font='Helvetica 14', bg="white",
            fg='black', wrap=WORD, undo=True, yscrollcommand=text_scroll.set)
text.pack()
text_scroll.config(command=text.yview)

# Создание меню
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Создание вкладок меню
# Вкладка Файл
file_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Новый", command=new_file)
file_menu.add_command(label="Открыть", command=open_file)
file_menu.add_command(label="Сохранить", command=save_file)
file_menu.add_command(label="Сохранить как", command=save_as)
file_menu.add_separator()
file_menu.add_cascade(label="Выход", command=root.quit)

# Вкладка Изменить
edit_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Изменить", menu=edit_menu)
edit_menu.add_command(label="Вырезать", command=lambda: cut_text(False), accelerator="(Ctrl+x)")
edit_menu.add_command(label="Копировать", command=lambda: copy_text(False), accelerator="(Ctrl+c)")
edit_menu.add_command(label="Вставить", command=lambda: paste_text(False), accelerator="(Ctrl+v)")
edit_menu.add_separator()
edit_menu.add_command(label="Отменить действие", command=text.edit_undo, accelerator="(Ctrl+z)")
edit_menu.add_command(label="Повторить действие", command=text.edit_redo, accelerator="(Ctrl+Shift+z)")

# Вкладка Цвета
color_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Цвет", menu=color_menu)
color_menu.add_command(label="Выделенного текста", command=text_color)
color_menu.add_command(label="Всего текста", command=all_text_color)
color_menu.add_command(label="Фон", command=bg_color)

# Вкладка Справка
info_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Справка", menu=info_menu)
info_menu.add_command(label="О программе", command=info)
info_menu.add_command(label="О разработчике", command=info_dev)

# Горячие клавиши для изменения
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

# Кнопка для выделения полужирным
bold_img = PhotoImage(file="bold1.png")
bold_btn = Button(toolbar_frame, image=bold_img, command=bold_it)
bold_btn.grid(row=0, column=0, sticky=W, padx=5, pady=5)
# Кнопка для выделения курсивом
italic_img = PhotoImage(file="italic.png")
italics_btn = Button(toolbar_frame, image=italic_img, command=italics_it)
italics_btn.grid(row=0, column=1, padx=5, pady=5)
# Кнопки отмены и повтора
undo_img = PhotoImage(file="undo.png")
undo_btn = Button(toolbar_frame, image=undo_img, command=text.edit_undo)
undo_btn.grid(row=0, column=2, padx=5, pady=5)
redo_img = PhotoImage(file="redo.png")
redo_btn = Button(toolbar_frame, image=redo_img, command=text.edit_redo)
redo_btn.grid(row=0, column=3, padx=5, pady=5)

root.mainloop()
