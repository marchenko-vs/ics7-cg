import matplotlib.pyplot as plt
import numpy as np
import time

from constants import *
from draw import clear_canvas, add_circle, add_ellipse

NUMBER_OF_RUNS = 20
MAX_RADIUS = 10000
STEP = 1000


def time_comparison(canvas, color_fg, algorithm, figure):
    time_list = []

    xc = CANVAS_WIDTH // 2
    yc = CANVAS_HEIGHT // 2

    ellipse = figure.get()
    old_algorithm = algorithm.get()

    for i in range(5):
        algorithm.set(i)

        time_start = [0] * (MAX_RADIUS // STEP)
        time_end = [0] * (MAX_RADIUS // STEP)

        for _ in range(NUMBER_OF_RUNS):
            ra = STEP
            rb = STEP

            for j in range(MAX_RADIUS // STEP):
                if ellipse:
                    time_start[j] += time.time()
                    add_ellipse(canvas, color_fg, algorithm, xc, yc, ra, rb, draw=False)
                    time_end[j] += time.time()

                    rb += STEP
                else:
                    time_start[j] += time.time()
                    add_circle(canvas, color_fg, algorithm, xc, yc, ra, draw=False)
                    time_end[j] += time.time()

                ra += STEP

            clear_canvas(canvas)

        size = len(time_start)
        res_time = list((time_end[i] - time_start[i]) / NUMBER_OF_RUNS for i in range(size))
        time_list.append(res_time)

    algorithm.set(old_algorithm)
    radius_arr = list(i for i in range(STEP, MAX_RADIUS + STEP, STEP))

    if ellipse:
        figure = "эллипса"
    else:
        figure = "окружности"

    plt.figure(figsize=(10, 6))
    plt.rcParams['font.size'] = '12'
    plt.title(f"Время построения {figure} различными алгоритмами")

    plt.plot(radius_arr, time_list[0], label='Каноническое уравнение')
    plt.plot(radius_arr, time_list[1], label='Параметрическое уравнение')
    plt.plot(radius_arr, time_list[2], label='Алгоритм Брезенхема')
    plt.plot(radius_arr, time_list[3], label='Алгоритм средней точки')
    plt.plot(radius_arr, time_list[4], label='Библиотечная функция')

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Радиус в пикселах")
    plt.ylabel("Время в секундах")

    plt.show()
