from pixels import draw_pixels


def bresenham_circle(xc, yc, r, color, canvas, draw):
    x = 0
    y = r
    delta = 2 * (1 - r)

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)

    while x < y:
        d = 2 * (delta + y) - 1
        x += 1

        if d >= 0:
            y -= 1
            delta += 2 * (x - y + 1)
        else:
            delta += x + x + 1

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)


def bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw):
    x = 0
    y = rb
    sqr_ra = ra * ra
    sqr_rb = rb * rb
    delta = sqr_rb - sqr_ra * (rb + rb + 1)

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

    while y >= 0:
        if delta <= 0:
            d = 2 * delta + sqr_ra * (y + y + 2)
            x += 1
            delta += sqr_rb * (x + x + 1)

            if d >= 0:
                y -= 1
                delta += sqr_ra * (- y - y + 1)
        else:
            d = 2 * delta + sqr_rb * (- x - x + 2)
            y -= 1
            delta += sqr_ra * (- y - y + 1)

            if d <= 0:
                x += 1
                delta += sqr_rb * (x + x + 1)

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)
