# function to find the mode radius

import statistics

# variable definitions
# mode = holder variable that calculates the mode per contour
# mode2 = final variable where the individual mode values are appended to

def modeRadius(radii):
    mode = []
    mode2 = []
    for i in range(len(radii)):
        mode = statistics.mode(radii[i])
        mode2.append(mode)

    return mode2