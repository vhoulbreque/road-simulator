def color_range_init():
    color_range = []

    # yellow
    for red in range(220, 255):
        for green in range(220, 255):
            for blue in range(0, 40):
                t = (red, green, blue)
                color_range.append(t)
    # white
    for red in range(230, 255):
        for green in range(230, 255):
            for blue in range(190, 255):
                t = (red, green, blue)
                color_range.append(t)

    return color_range


def white_range_init():
    color_range = []

    # white
    for red in range(230, 255):
        for green in range(230, 255):
            for blue in range(190, 255):
                t = (red, green, blue)
                color_range.append(t)

    return color_range


def yellow_range_init():
    color_range = []
    local_samples = [(207, 188, 104), (203, 190, 125), (234, 214, 126), (225, 212, 141),
                   (248, 244, 146), (238, 215, 122), (250, 245, 219), (250, 245, 199)]

    crange = 5
    for (r, g, b) in local_samples:
        for red in range(r-crange, r+crange):
            for green in range(g-crange, g+crange):
                for blue in range(b-crange, b+crange):
                    t = (red, green, blue)
                    color_range.append(t)

    return color_range


def shadow_colors_init():
    colors = []
    for i in range(0, 150):
        for j in range(0, 10):
            for k in range(0, 10):
                t1 = (i, i+j, i+k)
                t2 = (i+j, i, i+k)
                t3 = (i+j, i+k, i)
                colors.append(t1)
                colors.append(t2)
                colors.append(t3)

    for i in range(0, 30):
        for j in range(0, 30):
            for k in range(0, 30):
                t = (i, j, k)
                if t not in colors:
                    colors.append(t)
    return colors
