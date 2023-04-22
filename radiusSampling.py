# find the radii for the contours

# import necessary libraries
import math
import numpy as np

# define function
def radiusSampling(contours, center):
    # define array to hold radii values
    radii = [None] * len(contours)
    theta = [None] * len(contours)
    # define center
    #center = [0, 0]
    # loop through the contours
    j = 0
    for contour in contours:
        # loop through all the points in the contour
        radiiList = []
        thetaList = []
        for i in range(len(contour)):
            test = contour[i].flatten()
            test = test.tolist()
            y = test[1]
            x = test[0]
            # print(test)
            # need to create a list of the radii values and then add it to the radii array
            radiiList.append(int(math.dist(center,test)))
            thetaList.append(math.atan2(y-center[1],x-center[0]))
            
        radii[j] = radiiList
        theta[j] = thetaList
        j = j + 1

    return radii, theta