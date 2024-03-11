from customtkinter import *
from tkinter import filedialog
from PIL import ImageGrab
import tkinter as tk
import sys
import math
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = CTk()
root.title('PUNKTY & WIELOKĄT')

# Canvas
fig, rysunek = plt.subplots()
rysunek.set_aspect('equal', adjustable='box')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.config(width=1000, height=700)
canvas_widget.grid(row=1, column=6, columnspan=6, rowspan=11)

all_pts_figure = []
all_pts = []
current_letter = 65
wspol = []
dane = []
danepts = []
dash1 = ()
nowe_f = dane
x_poly, y_poly = [], []
count_inside = 0
not_in = []
in_poly = []


def close():
    for widget in root.winfo_children():
        widget.grid_remove()
    root.quit()


def save_canvas_as_image():
    global fig, canvas
    x, y, width, height = canvas.get_tk_widget().winfo_rootx(), canvas.get_tk_widget().winfo_rooty(), canvas.get_tk_widget().winfo_width(), canvas.get_tk_widget().winfo_height()
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if file_path:
        try:
            screenshot.save(file_path, "PNG")
            napis_zapis = CTkEntry(root, width=200, height=30)
            napis_zapis.grid(row=9, column=0, columnspan=2, rowspan=2)
            text = 'Image saved!'
            napis_zapis.insert(0, text.center(50))
        except Exception as e:
            print(f"An error occurred: {e}")


def display_points():
    global current_letter, wspol, all_pts, count_inside, in_poly, not_in
    count_inside = 0
    rysunek.cla()
    is_wiel = False
    if len(all_pts_figure) != 0:
        is_wiel = True
        rysowanie()
    else:
        messagebox.showinfo('SPRAWDZENIE PUNKTU', 'BRAK WGRANEGO WIELOKĄTA')
        pass
    letter = chr(current_letter)
    y = float(wpis_y.get())
    x = float(wpis_x.get())
    tab = [y, x]
    if is_point_inside_polygon(tab, dane) and is_wiel:
        in_poly.append(tab)
        print('----------')
        print(f'Punkt {tab} jest w wielokącie.')
        messagebox.showinfo('SPRAWDZENIE PUNKTU', 'PUNKT W WIELOKĄCIE')
    elif is_wiel:
        not_in.append(tab)
        print('----------')
        print(f'Punkt {tab} jest poza wielokątem.')
        messagebox.showinfo('SPRAWDZENIE PUNKTU', 'PUNKT POZA WIELOKĄTEM')
    if is_wiel:
        all_pts.append(tab)
        tab = [letter, x, y]
        wspol.append(tab)
        print(f'{x} ; {y} ]')
        print('----------')
        rysunek.scatter(y, x, color='black')
    canvas.draw()


def rysowanie():
    global dane, dash1, current_letter
    rysunek.cla()
    x_first = dane[0]
    y_first = dane[1]
    x_last = dane[-2]
    y_last = dane[-1]
    grubosc = int(comb_grubosc.get())
    kolor = str(comb_kolor.get())
    kolor_pkt = str(comb_kolor_pkt.get())
    for i in range(0, len(dane) - 3, 2):
        style = comb_styl.get()
        if style == "ciągłą":
            dash1 = 'solid'
        elif style == "przerywana":
            dash1 = 'dashed'
        elif style == "przerywana 2":
            dash1 = 'dotted'
        rysunek.plot([float(dane[i + 1]), float(dane[i + 3])], [float(dane[i]), float(dane[i + 2])],
                     color=kolor, linewidth=grubosc, linestyle=dash1)
        rysunek.scatter(float(dane[i + 1]), float(dane[i]), color=kolor_pkt)
    rysunek.scatter(float(y_last), float(x_last), color=kolor_pkt)
    rysunek.plot([float(y_last), float(y_first)], [float(x_last), float(x_first)], color=kolor, linewidth=grubosc, linestyle=dash1)
    if len(all_pts) != 0:
        redraw_points()
    canvas.draw()


def redraw_points():
    global current_letter, in_poly, not_in
    kolor_in = comb_kolor_pkt_in.get()
    kolor_out = comb_kolor_pkt_out.get()
    for point in in_poly:
        x = point[0]
        y = point[1]
        rysunek.scatter(x, y, color=kolor_in)
    for point in not_in:
        x = point[0]
        y = point[1]
        rysunek.scatter(x, y, color=kolor_out)
    canvas.draw()


def rysowanie_punkt():
    global wspol, current_letter, all_pts, danepts, x_poly, y_poly, dane, count_inside, in_poly, not_in
    file_path = filedialog.askopenfilename()
    wpis_selected_file = CTkEntry(root, width=200)
    if file_path:
        if file_path.lower().endswith('.txt'):
            wpis_selected_file.grid(row=5, column=0, columnspan=2)
            wpis_selected_file.delete(0, 'end')
            text = 'File uploaded!'
            wpis_selected_file.insert(1, text.center(50))
            try:
                with open(file_path, 'r') as file:
                    rysunek.cla()
                    all_pts.clear()
                    not_in.clear()
                    wspol.clear()
                    in_poly.clear()
                    rysowanie()
                    count_inside = 0
                    file_contents = file.readlines()
                    y_min = min(x_poly)
                    y_max = max(x_poly)
                    x_min = min(y_poly)
                    x_max = max(y_poly)
                    count_inside = 0
                    # print(f'Drew points:')
                    for line in file_contents:
                        y, x = map(float, line.split())
                        print(x)
                        tab = [x, y]
                        all_pts.append(tab)
                        letter = chr(current_letter)
                        if x_min <= y <= x_max and y_min <= x <= y_max:
                            if is_point_inside_polygon(tab, dane):
                                rysunek.scatter(x, y, color='red')
                                in_poly.append(tab)
                            else:
                                rysunek.scatter(x, y, color='green')
                                not_in.append(tab)
                        tab = [letter, x, y]
                        wspol.append(tab)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                pass
            finally:
                canvas.draw()
                add_point_to_polygon_list()
        else:
            wpis_selected_file.delete(0, 'end')
            wpis_selected_file.insert(0, "Error: Please select a .txt file")


def rysowanie_poly():
    global dane, current_letter, all_pts_figure, x_poly, y_poly, count_inside, rysunek
    file_path = filedialog.askopenfilename()
    wpis_selected_file = CTkEntry(root, width=200)
    if file_path:
        if file_path.lower().endswith('.txt'):
            wpis_selected_file.grid(row=5, column=0, columnspan=2)
            wpis_selected_file.delete(0, 'end')
            text = 'File uploaded!'
            wpis_selected_file.insert(1, text.center(50))
            try:
                with open(file_path, 'r') as file:
                    all_pts_figure.clear()
                    dane.clear()
                    rysunek.cla()
                    not_in.clear()
                    wspol.clear()
                    in_poly.clear()
                    x_poly.clear()
                    y_poly.clear()
                    count_inside = 0
                    file_contents = file.readlines()
                    for line in file_contents:
                        x, y = map(float, line.split())
                        dane.append(x)
                        dane.append(y)
                    x_first = dane[0]
                    y_first = dane[1]
                    x_last = dane[-2]
                    y_last = dane[-1]
                    for i in range(0, len(dane) - 3, 2):
                        rysunek.scatter(float(dane[i + 1]), float(dane[i]), color='black')
                        rysunek.plot([float(dane[i + 1]), float(dane[i + 3])], [float(dane[i]), float(dane[i + 2])],
                                     color='black')
                        tab = [float(dane[i + 1]), float(dane[i])]
                        all_pts_figure.append(tab)
                    rysunek.scatter(float(y_last), float(x_last), color='black')
                    rysunek.plot([float(y_last), float(y_first)], [float(x_last), float(x_first)], color='black')
                    canvas.draw()
                    tab = [float(dane[-2]), float(dane[-1])]
                    all_pts_figure.append(tab)
                    print(f'Punkty wielokąta: {all_pts_figure}')
                    for i in range(0, len(dane) - 1, 2):
                        x_poly.append(float(dane[i + 1]))
                        y_poly.append(float(dane[i]))
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except Exception as e:
                print(f"An error occurred: {e}")
                pass
        else:
            wpis_selected_file.delete(0, 'end')
            wpis_selected_file.insert(0, "Error: Please select a .txt file")


inside_points = []
x_intersect = 0


def is_point_inside_polygon(point, polygon):
    x, y = point[0], point[1]
    angle_sum = 0

    for i in range(0, len(polygon) - 2, 2):
        if x == float(polygon[i+1]) and y == float(polygon[i]) or x == float(polygon[i + 3]) and y == float(
                polygon[i + 2]):
            angle_sum = math.pi - 0.1
            break
        y1, x1 = polygon[i], polygon[i + 1]
        y2, x2 = polygon[i + 2], polygon[i + 3]

        dx1 = float(x1) - x
        dy1 = float(y1) - y
        dx2 = float(x2) - x
        dy2 = float(y2) - y

        angle1 = math.atan2(dy1, dx1)
        angle2 = math.atan2(dy2, dx2)
        angle = angle2 - angle1

        if angle > math.pi:
            angle -= 2 * math.pi
        elif angle < -math.pi:
            angle += 2 * math.pi

        angle_sum += angle

    return abs(angle_sum) >= math.pi - 0.1  # Wewnątrz, jeśli suma kątów nie jest 0


def add_point_to_polygon_list():
    global dane, all_pts, wspol, count_inside
    count_inside = 0
    inside_points = []
    polygon = dane
    for i in range(len(wspol)):
        point = [float(wspol[i][1]), float(wspol[i][2])]
        res = is_point_inside_polygon(point, polygon)
        if res != 0:
            count_inside += 1
            # inside_points.append((point[0], point[1]))
            # # inside_points.append(wspol[i][0])

    # print(f'Punkty w wielokącie: {inside_points}')
    print(f'Ilość punktów w wielokącie: {count_inside}')


def redirect_stdout_to_text_widget(text_widget):
    class StdoutRedirector:
        def __init__(self, text_widget):
            self.text_widget = text_widget

        def write(self, text):
            self.text_widget.insert(tk.END, text)
            self.text_widget.see(tk.END)  # Scroll to the end

        def flush(self):
            pass

    sys.stdout = StdoutRedirector(text_widget)


def save_to_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                console_text = console_output.get(1.0, tk.END)  # Get the console output from the Text widget
                file.write(console_text)
                napis_zapis = CTkEntry(root, width=200)
                napis_zapis.grid(row=9, column=2, columnspan=2)
                text = 'File saved!'
                napis_zapis.insert(0, text.center(50))
        except Exception as e:
            print(f"An error occurred: {e}")


# Labels
label_napis1 = CTkLabel(root, text="Wpisz współrzędne:", font=("Arial", 20, "bold"))
label_napis1.grid(row=0, column=0, columnspan=2)

label_napis3 = CTkLabel(root, text="Grubość linii:")
label_napis3.grid(row=15, column=7, rowspan=2)

but_napis5 = CTkLabel(root, text="Kolor lini:")
but_napis5.grid(row=15, column=5, rowspan=2)

label_napis7 = CTkLabel(root, text="Styl linii:")
label_napis7.grid(row=15, column=9, rowspan=2)

label_napis8 = CTkLabel(root, text=" ")
label_napis8.grid(row=5, column=0)

but_napis9 = CTkLabel(root, text="Kolor punktu wielokąta:")
but_napis9.grid(row=17, column=5, rowspan=2)

but_napis10 = CTkLabel(root, text="Kolor punktów w środku:")
but_napis10.grid(row=17, column=7, rowspan=2)

but_napis11 = CTkLabel(root, text="Kolor punktów na zewnątrz:")
but_napis11.grid(row=17, column=9, rowspan=2)

label_x = CTkLabel(root, text="X:")
label_x.grid(row=1, column=0)

label_y = CTkLabel(root, text="Y:")
label_y.grid(row=1, column=2)

# Entry widgets
wpis_x = CTkEntry(root, width=100)
wpis_x.grid(row=1, column=1)

wpis_y = CTkEntry(root, width=100)
wpis_y.grid(row=1, column=3)

# Buttons

but_punkty = CTkButton(root, text="Wczytaj punkty", font=("Arial", 15, "bold"), command=rysowanie_punkt, width=200,
                       height=50, border_width=3)
but_punkty.grid(row=4, column=2, columnspan=2)

but_oblicz = CTkButton(root, text="SPRAWDŹ PUNKT", command=display_points, font=("Arial", 15, "bold"),
                       text_color='black', width=400, height=50,
                       border_width=5, border_color='orange', fg_color='yellow')
but_oblicz.grid(row=2, column=0, columnspan=4, rowspan=2)

but_daneplik = CTkButton(root, text="Wczytaj wielokąt z pliku", font=("Arial", 15, "bold"), border_width=3,
                         command=rysowanie_poly, width=200, height=50)
but_daneplik.grid(row=4, column=0, columnspan=2)

but_zapiszplik = CTkButton(root, text="Zapisz raport", command=save_to_file, width=200, height=40)
but_zapiszplik.grid(row=5, column=2, columnspan=2, rowspan=2)

but_zapiszobraz = CTkButton(root, text="Zapisz obraz", command=save_canvas_as_image, width=200, height=40)
but_zapiszobraz.grid(row=7, column=2, columnspan=2)

but_zamknij = CTkButton(root, text="Zamknij program", command=close, width=150, height=50, fg_color='red',
                        border_color='dark red',
                        border_width=5)
but_zamknij.grid(row=16, column=12, rowspan=2)

# Pola rozwijane
console_output = tk.Text(root, wrap=tk.WORD, width=50, height=20)
console_output.grid(row=9, column=0, rowspan=7, columnspan=4)
redirect_stdout_to_text_widget(console_output)

comb_kolor = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(),
                         values=['black', 'red', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor.grid(row=15, column=6, rowspan=2)

comb_styl = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(),
                        values=['ciągłą', 'przerywana', 'przerywana 2'])
comb_styl.grid(row=15, column=10, rowspan=2)

comb_grubosc = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(), values=['1', '2', '3'])
comb_grubosc.grid(row=15, column=8, rowspan=2)

comb_kolor_pkt = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(),
                         values=['black', 'red', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_pkt.grid(row=17, column=6, rowspan=2)

comb_kolor_pkt_in = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(),
                         values=['red', 'black', 'green', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_pkt_in.grid(row=17, column=8, rowspan=2)

comb_kolor_pkt_out = CTkComboBox(root, width=150, height=30, command=lambda value: rysowanie(),
                         values=['green', 'black', 'red', 'blue', 'yellow', 'pink', 'purple', 'orange'])
comb_kolor_pkt_out.grid(row=17, column=10, rowspan=2)

root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()
