from constants import *
from draw import *
from tkinter import *

window = Tk()
window.title("Лабораторная работа #5")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+0+0")
window.resizable(False, False)

canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(side='right')

figures = [[[]]]

p_min = [CANVAS_WIDTH, CANVAS_HEIGHT]
p_max = [0, 0]

Label(text="Цвет закраски", font=("Calibri", 20, "bold")).place(width=445, x=0, y=0)

color_var = IntVar()
color_var.set(0)

Radiobutton(text="Фиолетовый", variable=color_var, value=0,
            font=("Calibri", 18), anchor="w").place(width=170, height=25, x=40, y=40)

Radiobutton(text="Черный", variable=color_var, value=1,
            font=("Calibri", 18), anchor="w").place(width=120, height=25, x=40, y=70)

Radiobutton(text="Красный", variable=color_var, value=2,
            font=("Calibri", 18), anchor="w").place(width=120, height=25, x=40, y=100)

Radiobutton(text="Синий", variable=color_var, value=3,
            font=("Calibri", 18), anchor="w").place(width=120, height=25, x=260, y=40)

Radiobutton(text="Зеленый", variable=color_var, value=4,
            font=("Calibri", 18), anchor="w").place(width=120, height=25, x=260, y=70)

Radiobutton(text="Желтый", variable=color_var, value=5,
            font=("Calibri", 18), anchor="w").place(width=120, height=25, x=260, y=100)

Label(text="Режим закраски", font=("Calibri", 20, "bold")).place(width=445, height=30, x=0, y=140)

mode_var = BooleanVar()
mode_var.set(True)

Radiobutton(text="Без задержки", variable=mode_var, value=0,
            font=("Calibri", 18), anchor="w").place(width=170, height=25, x=40, y=175)

Radiobutton(text="С задержкой", variable=mode_var, value=1,
            font=("Calibri", 18), anchor="w").place(width=170, height=25, x=260, y=175)

Label(text="Добавление точки", font=("Calibri", 20, "bold")).place(width=445, height=30, x=0, y=215)

Label(text="X", font=("Calibri", 18)).place(width=130, height=25, x=70, y=250)
Label(text="Y", font=("Calibri", 18)).place(width=130, height=25, x=255, y=250)

x_entry = Entry(font=("Calibri", 20), justify='center')
x_entry.place(width=185, height=35, x=40, y=285)

y_entry = Entry(font=("Calibri", 20), justify='center')
y_entry.place(width=185, height=35, x=225, y=285)

points_listbox = Listbox(font=("Calibri", 18))
points_listbox.place(width=370, height=280, x=40, y=325)

Button(text="Построить точку", font=("Calibri", 18),
       highlightbackground="#b3b3cc", highlightthickness=30,
       command=lambda: draw_point(figures, img, color_var, x_entry, y_entry,
                                  p_min, p_max, points_listbox)).place(width=370, height=50, x=40, y=615)

Button(text="Замкнуть фигуру", font=("Calibri", 18),
       highlightbackground="#b3b3cc", highlightthickness=30,
       command=lambda: click_right(figures, img, color_var)).place(width=370, height=50, x=40, y=670)

Label(text="Построение с помощью мыши",
      font=("Calibri", 20, "bold")).place(width=445, height=30, x=0, y=740)

Label(text="Левая кнопка - добавить точку",
      font=("Calibri", 18)).place(width=445, height=30, y=770)

Label(text="Правая кнопка - замкнуть фигуру",
      font=("Calibri", 18)).place(width=445, height=30, y=800)

Label(text="Время закраски:", font=("Calibri", 18)).place(width=170, height=30, x=40, y=830)

time_entry = Entry(font=("Calibri", 18), justify='center')
time_entry.place(width=170, height=30, x=240, y=830)

Button(text="Выполнить закраску", font=("Calibri", 18),
       highlightbackground="#d1d1e0", highlightthickness=30,
       command=lambda: fill_figure(figures, img, canvas, color_var, p_min, p_max, mode_var, time_entry)). \
    place(width=370, height=50, x=40, y=870)

Button(text="Очистить экран", font=("Calibri", 18),
       highlightbackground="#b3b3cc", highlightthickness=30,
       command=lambda: clear_canvas(img, figures, p_min, p_max,
                                    time_entry, points_listbox)).place(width=370, height=50, x=40, y=925)

img = PhotoImage(width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.create_image(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, image=img, state='normal')

canvas.bind('<Button-1>',
            lambda event: click_left(event, figures, img, color_var, p_min, p_max, points_listbox))
canvas.bind('<Button-3>',
            lambda event: click_right(figures, img, color_var))

x_entry.insert(0, '100')
y_entry.insert(0, '100')

window.mainloop()
