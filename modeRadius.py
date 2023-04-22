# function to find the mode radius

import statistics

def modeRadius(radii):
    mode = []
    mode2 = []
    for i in range(len(radii)):
        mode = statistics.mode(radii[i])
        mode2.append(mode)

    return mode2