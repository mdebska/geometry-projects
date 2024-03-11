import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
from customtkinter import *
from tkinter import filedialog
from math import atan2

root = CTk()
root.title('OTOCZKA WOKÓŁ PUNKTÓW')

fig, ax = plt.subplots()
ax.set_aspect('equal', adjustable='box')
plt.xlabel('Y')
plt.ylabel('X')
plt.title('Convex Hull around Points')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.config(width=800, height=800)
canvas_widget.grid(row=1, column=5, columnspan=6, rowspan=15)

punkty_all = []
punkty_otoczka = []
punkty_kraw = []


def graham_scan(points):
    global punkty_kraw
    punkty_kraw.clear()

    def orientation(p, q, r):
        # - 0, jeśli punkty są współliniowe,
        # - 1, jeśli skręt w lewo,
        # - (-1), jeśli skręt w prawo.
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        return 1 if val > 0 else -1

    def find_p0(points): # ppkt 1
        min_y = float('inf')
        min_x = float('inf')
        p0 = None
        for point in points:
            x, y = point
            if y < min_y or (y == min_y and x < min_x):
                min_y = y
                min_x = x
                p0 = point
        return p0

    def sort_by_polar_angle(points, p0):
        return sorted(points, key=lambda point: (atan2(point[1] - p0[1], point[0] - p0[0]), point))

    if len(points) < 3:
        raise ValueError("Za mało punktów do utworzenia otoczki wypukłej.")
    p0 = find_p0(points)
    # Sortowanie ze względu na azymuty
    sorted_points = sort_by_polar_angle(points, p0)
    stack = [p0, sorted_points[0], sorted_points[1]]
    # ppkt 5
    for i in range(2, len(sorted_points)):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], sorted_points[i]) != -1:
            stack.pop()
        stack.append(sorted_points[i])
    punkty_kraw = stack

    return stack


def import_points():
    global punkty_kraw
    ax.cla()
    punkty_kraw.clear()
    punkty_all.clear()
    punkty_otoczka.clear()
    file_path = filedialog.askopenfilename(title="Select File", filetypes=[("Text files", "*.txt")])
    if not file_path:
        print("No file selected. Exiting.")
        return
    messagebox.showinfo('SPRAWDZENIE PLIKU', 'PLIK WCZYTANY')
    with open(file_path, 'r') as file:
        lines = file.readlines()
    y = [float(line.split()[1]) for line in lines]
    x = [float(line.split()[0]) for line in lines]
    # x_min = min(y)
    # x_max = max(y)
    # y_min = min(x)
    # y_max = max(x)
    # prostokat_x = [x_min, x_max, x_max, x_min, x_min]
    # prostokat_y = [y_min, y_min, y_max, y_max, y_min]
    # ax.plot(prostokat_x, prostokat_y, linewidth=1, color='red')
    for line in lines:
        ig = float(line.split()[1])
        iks = float(line.split()[0])
        punkty_all.append([iks, ig])
        punkty_otoczka.append([iks, ig])
        ax.scatter(ig, iks, s=10, color='black')
    convex_hull = graham_scan(punkty_otoczka)
    iks = [convex_hull[i][1] for i in range(len(convex_hull))]
    ig = [convex_hull[i][0] for i in range(len(convex_hull))]
    ax.plot(iks, ig, linewidth=1, color='black')
    ax.plot([iks[-1], iks[0]], [ig[-1], ig[0]], linewidth=1, color='black')
    canvas.draw()
    return x, y


dash = ''
mark = ''
dash1 = ''


def otoczka():
    global dash, mark, dash1, punkty_kraw
    ax.cla()
    punkty_kraw.clear()
    grubosc = int(comb_size_ot.get())
    kolor = str(comb_kolor_ot.get())
    style = comb_shape_ot.get()
    kolor_pkt = str(comb_kolor_pkt.get())
    size_pkt = int(comb_size_pkt.get())
    styl_pkt = str(comb_shape_pkt.get())
    grubosc_prost = int(comb_size_prost.get())
    kolor_prost = str(comb_kolor_prost.get())
    style_prost = comb_shape_prost.get()
    if styl_pkt == 'okrąg':
        mark = 'o'
    elif styl_pkt == 'kwadrat':
        mark = 's'
    elif styl_pkt == 'trójkąt':
        mark = '^'
    if style == "ciągła":
        dash = 'solid'
    elif style == "przerywana":
        dash = 'dashed'
    elif style == "kropkowana":
        dash = 'dotted'
    if style_prost == "ciągła":
        dash1 = 'solid'
    elif style_prost == "przerywana":
        dash1 = 'dashed'
    elif style_prost == "kropkowana":
        dash1 = 'dotted'
    if wpis_x.get() != '' and wpis_y.get() != '':
        x = float(wpis_x.get())
        y = float(wpis_y.get())
        punkty_all.append([x, y])
    ig = [punkty_all[i][1] for i in range(len(punkty_all))]
    iks = [punkty_all[i][0] for i in range(len(punkty_all))]
    if check_frame.get() == 1:
        x_min = min(ig)
        x_max = max(ig)
        y_min = min(iks)
        y_max = max(iks)
        prostokat_x = [x_min, x_max, x_max, x_min, x_min]
        prostokat_y = [y_min, y_min, y_max, y_max, y_min]
        ax.plot(prostokat_x, prostokat_y, linewidth=grubosc_prost, color=kolor_prost, linestyle=dash1)
    for i in range(len(punkty_all)):
        y = punkty_all[i][1]
        x = punkty_all[i][0]
        ax.scatter(y, x, color=kolor_pkt, s=size_pkt, marker=mark)
        if check_points.get() == 1:
            ax.text(y + 0.1, x + 0.1, str(i + 1), fontsize=12)
    convex_hull = graham_scan(punkty_all)
    iks = [convex_hull[i][1] for i in range(len(convex_hull))]
    ig = [convex_hull[i][0] for i in range(len(convex_hull))]
    ax.plot(iks, ig, linewidth=grubosc, color=kolor, linestyle=dash)
    ax.plot([iks[-1], iks[0]], [ig[-1], ig[0]], linewidth=grubosc, color=kolor, linestyle=dash)
    canvas.draw()


def save_to_file():
    global punkty_kraw
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not file_path:
        print("No file selected. Exiting.")
        return
    with open(file_path, 'w') as file:
        for punkt in punkty_kraw:
            file.write(f"{punkt[0]:.3f}      {punkt[1]:.3f}\n")
    messagebox.showinfo('ZAPISANO DO PLIKU', 'Punkty otoczki zostały zapisane do pliku.')


def close():
    for widget in root.winfo_children():
        widget.grid_remove()
    root.quit()


# labels
label_napis1 = CTkLabel(root, text="   Wpisz współrzędne:", font=("Arial", 20, "bold"))
label_napis1.grid(row=0, column=0, columnspan=2)

label_napis2 = CTkLabel(root, text="              ")
label_napis2.grid(row=1, column=4)

label_napis3 = CTkLabel(root, text="         X: ")
label_napis3.grid(row=1, column=0)

label_napis4 = CTkLabel(root, text="Y: ")
label_napis4.grid(row=1, column=2)

label_napis5 = CTkLabel(root, text="Kolor punktu")
label_napis5.grid(row=4, column=1)

label_napis6 = CTkLabel(root, text="Kształt punktu")
label_napis6.grid(row=5, column=1)

label_napis7 = CTkLabel(root, text="Wielkość punktu")
label_napis7.grid(row=6, column=1)

label_napis8 = CTkLabel(root, text="Kolor otoczki")
label_napis8.grid(row=8, column=1)

label_napis9 = CTkLabel(root, text="Kształt otoczki")
label_napis9.grid(row=9, column=1)

label_napis10 = CTkLabel(root, text="Wielkość otoczki")
label_napis10.grid(row=10, column=1)

label_napis11 = CTkLabel(root, text="Kolor ramki")
label_napis11.grid(row=11, column=1)

label_napis12 = CTkLabel(root, text="Kształt ramki")
label_napis12.grid(row=12, column=1)

label_napis13 = CTkLabel(root, text="Wielkość ramki")
label_napis13.grid(row=13, column=1)

# buttons
but_punkty = CTkButton(root, text="WYZNACZ PUNKT", font=("Arial", 15, "bold"), command=otoczka, width=300,
                       height=50, border_width=3)
but_punkty.grid(row=2, column=1, columnspan=3)

but_otoczka = CTkButton(root, text="WCZYTAJ PUNKTY Z PLIKU", command=import_points, font=("Arial", 15, "bold"),
                        text_color='black', width=300, height=50,
                        border_width=5, border_color='orange', fg_color='yellow')
but_otoczka.grid(row=3, column=1, columnspan=3)

but_zapis = CTkButton(root, text="ZAPISZ PUNKTY OTOCZKI DO PLIKU", command=save_to_file, font=("Arial", 15, "bold"),
                      text_color='black', width=300, height=50,
                      border_width=5, border_color='orange', fg_color='yellow')
but_zapis.grid(row=14, column=1, columnspan=3)

# entery
wpis_x = CTkEntry(root, width=100)
wpis_x.grid(row=1, column=1)

wpis_y = CTkEntry(root, width=100)
wpis_y.grid(row=1, column=3)

# comboboxy
comb_kolor_pkt = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                             values=['black', 'red', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_pkt.grid(row=4, column=2)

comb_shape_pkt = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                             values=['okrąg', 'kwadrat', 'trójkąt'])
comb_shape_pkt.grid(row=5, column=2)

comb_size_pkt = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                            values=['10', '20', '30'])
comb_size_pkt.grid(row=6, column=2)

check_points = CTkCheckBox(root, width=150, height=30, command=otoczka, text='Numeracja punktów')
check_points.grid(row=7, column=2)

comb_kolor_ot = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                            values=['black', 'red', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_ot.grid(row=8, column=2)

comb_shape_ot = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                            values=['ciągła', 'przerywana', 'kropkowana'])
comb_shape_ot.grid(row=9, column=2)

comb_size_ot = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                           values=['1', '2', '3'])
comb_size_ot.grid(row=10, column=2)

comb_kolor_prost = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                               values=['red', 'black', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_prost.grid(row=11, column=2)

comb_shape_prost = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                               values=['ciągła', 'przerywana', 'kropkowana'])
comb_shape_prost.grid(row=12, column=2)

comb_size_prost = CTkComboBox(root, width=150, height=30, command=lambda value: otoczka(),
                              values=['1', '2', '3'])
comb_size_prost.grid(row=13, column=2)

check_frame = CTkCheckBox(root, width=150, height=30, command=otoczka, text='Pokaż ramkę')
check_frame.grid(row=7, column=1)

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
