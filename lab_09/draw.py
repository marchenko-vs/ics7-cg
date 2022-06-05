import copy
import itertools
import sutherland_hodgman as sh

from tkinter import messagebox


def clear_canvas(canvas, figure, clipper):
    canvas.delete("all")

    figure.clear()
    clipper.clear()


def clear_clipper(canvas, figure, clipper, color_fig_var):
    canvas.delete("all")

    draw_figure(canvas, figure, color_fig_var)

    clipper.clear()


def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill=color)


def draw_figure(canvas, figure, color_var):
    color = get_color(color_var)

    for i in range(len(figure) - 1):
        canvas.create_line(figure[i], figure[i + 1], fill=color)


def get_color(color_var):
    col_var = color_var.get()
    color = ''

    match col_var:
        case 0:
            color = "#000000"
        case 1:
            color = "#ff0000"
        case 2:
            color = "#0000ff"
        case 3:
            color = "#3ebd33"
        case 4:
            color = "#ffa600"
        case 5:
            color = "#bd08fc"

    return color


def click_right(event, figure, clipper, canvas, color_cut_var, color_fig_var):
    click_left(event, figure, clipper, canvas, color_cut_var, color_fig_var)


def click_left(event, figure, clipper, canvas, color_cut_var, color_fig_var):
    if len(clipper) > 3 and clipper[0] == clipper[-1]:
        clear_clipper(canvas, figure, clipper, color_fig_var)

    x = event.x
    y = event.y

    if len(clipper) > 0 and clipper[-1][0] == x and clipper[-1][1] == y:
        return

    color = get_color(color_cut_var)
    set_pixel(canvas, x, y, color)

    clipper.append([x, y])

    if len(clipper) >= 2:
        canvas.create_line(clipper[-2], clipper[-1], fill=color)


def close_figure(figure, canvas, color_var, info_name):
    if len(figure) < 3:
        messagebox.showerror("Ошибка!", f"{info_name} иметь более 2-х вершин!")
        return

    if figure[0] == figure[-1]:
        return

    color = get_color(color_var)
    figure.append(figure[0])

    canvas.create_line(figure[-2], figure[-1], fill=color)


def add_vertex(figure, clipper, canvas, color_cut_var, color_fig_var, x_entry, y_entry):
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка!",
                             "Координаты вершины должны быть целыми числами.")
        return

    if len(clipper) > 3 and clipper[0] == clipper[-1]:
        clear_clipper(canvas, figure, clipper, color_fig_var)

    color = get_color(color_cut_var)
    set_pixel(canvas, x, y, color)

    clipper.append([x, y])

    if len(clipper) >= 2:
        canvas.create_line(clipper[-2], clipper[-1], fill=color)


def line_coefficients(x_0, y_0, x_1, y_1):
    a = y_0 - y_1
    b = x_1 - x_0
    c = x_0 * y_1 - x_1 * y_0

    return a, b, c


def solve_lines_intersection(a_0, b_0, c_0, a_1, b_1, c_1):
    determinant_0 = a_0 * b_1 - a_1 * b_0
    determinant_1 = (-c_0) * b_1 - b_0 * (-c_1)
    determinant_2 = a_0 * (-c_1) - (-c_0) * a_1

    if determinant_0 == 0:
        return -1, -1

    x = determinant_1 / determinant_0
    y = determinant_2 / determinant_0

    return x, y


def is_coordinate_between(left_coordinate, right_coordinate, dot_coordinate):
    return min(left_coordinate, right_coordinate) <= dot_coordinate <= max(left_coordinate, right_coordinate)


def is_dot_between(dot_left, dot_right, dot_intersection):
    return is_coordinate_between(dot_left[0], dot_right[0], dot_intersection[0]) and \
           is_coordinate_between(dot_left[1], dot_right[1], dot_intersection[1])


def are_sides_linked(line_0, line_1):
    if (line_0[0][0] == line_1[0][0] and line_0[0][1] == line_1[0][1]) or \
            (line_0[1][0] == line_1[1][0] and line_0[1][1] == line_1[1][1]) or \
            (line_0[0][0] == line_1[1][0] and line_0[0][1] == line_1[1][1]) or \
            (line_0[1][0] == line_1[0][0] and line_0[1][1] == line_1[0][1]):
        return True

    return False


def extra_check_polygon(clipper):
    clipper_figure = []

    for i in range(len(clipper) - 1):
        clipper_figure.append([clipper[i], clipper[i + 1]])

    combinations_figure = list(itertools.combinations(clipper_figure, 2))

    for i in range(len(combinations_figure)):
        line1 = combinations_figure[i][0]
        line2 = combinations_figure[i][1]

        if are_sides_linked(line1, line2):
            continue

        a1, b1, c1 = line_coefficients(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
        a2, b2, c2 = line_coefficients(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

        dot_intersection = solve_lines_intersection(a1, b1, c1, a2, b2, c2)

        if is_dot_between(line1[0], line1[1], dot_intersection) and \
                is_dot_between(line2[0], line2[1], dot_intersection):
            return True

    return False


def make_unique(sides):
    for side in sides:
        side.sort()

    return list(filter(lambda x: (sides.count(x) % 2) == 1, sides))


def is_dot_on_side(dot, side):
    if abs(sh.vector_mul(sh.get_vector(dot, side[0]), sh.get_vector(side[1], side[0]))) <= 1e-6:
        if side[0] < dot < side[1] or side[1] < dot < side[0]:
            return True

    return False


def get_sides(side, rest_dots):
    dots_list = [side[0], side[1]]

    for dot in rest_dots:
        if is_dot_on_side(dot, side):
            dots_list.append(dot)

    dots_list.sort()

    sections_list = list()

    for i in range(len(dots_list) - 1):
        sections_list.append([dots_list[i], dots_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_dots):
    all_sides = list()
    rest_dots = figure_dots[2:]

    for i in range(len(figure_dots)):
        cur_side = [figure_dots[i], figure_dots[(i + 1) % len(figure_dots)]]

        all_sides.extend(get_sides(cur_side, rest_dots))

        rest_dots.pop(0)
        rest_dots.append(figure_dots[i])

    return make_unique(all_sides)


def check_polygon(clipper):
    if len(clipper) < 4:
        return False

    if sh.vector_mul(sh.get_vector(clipper[1], clipper[2]),
                     sh.get_vector(clipper[0], clipper[1])) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(3, len(clipper)):
        if sign * sh.vector_mul(sh.get_vector(clipper[i - 1], clipper[i]),
                                sh.get_vector(clipper[i - 2], clipper[i - 1])) < 0:
            return False

    if sign < 0:
        clipper.reverse()

    return True


def clip(clipper, figure, canvas, color_result_var):
    if len(clipper) < 4:
        messagebox.showerror("Ошибка!", "Отсутствует отсекатель.")
        return

    if len(figure) < 4:
        messagebox.showerror("Ошибка!", "Отсутствует фигура.")
        return

    if clipper[0] != clipper[-1]:
        messagebox.showerror("Ошибка!", "Отсекатель не замкнут.")
        return

    if figure[0] != figure[-1]:
        messagebox.showerror("Ошибка!", "Фигура не замкнута.")
        return

    if not check_polygon(clipper) or extra_check_polygon(clipper):
        messagebox.showerror("Ошибка!", "Отсекатель должен быть выпуклым многоугольником.")
        return

    if extra_check_polygon(figure):
        messagebox.showerror("Ошибка!", "Фигура должна быть многоугольником.")
        return

    result_color = get_color(color_result_var)
    result = copy.deepcopy(figure)

    for index in range(-1, len(clipper) - 1):
        line = [clipper[index], clipper[index + 1]]
        position_dot = clipper[index + 1]

        result = sh.sutherland_hodgman_algorithm(line, position_dot, result)

        if len(result) <= 2:
            return

    draw_result_figure(result, canvas, result_color)


def draw_result_figure(figure_dots, canvas, res_color):
    fixed_figure = remove_odd_sides(figure_dots)

    for line in fixed_figure:
        canvas.create_line(line[0], line[1], fill=res_color)