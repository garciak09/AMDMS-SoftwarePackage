# find the radii for the contours

# import necessary libraries
import math
import numpy as np


# variable definitions
# radii = array of radius values for each pixel in each contour
# theta = array of angle values for each pixel in each contour
# radiiList = list of radius values for each pixel in a contour
# thetaList = list of angle values for each pixel in a contour
# test = list of all the pixel values in the contours
# y = y value of a pixel location
# x = x value of a pixel location

# define function
def radiusSampling(contours, center):
    print("radiusSampling")
    # define array to hold radii values
    radii = [None] * len(contours)
    theta = [None] * len(contours)
    pixelCoordinates = []
    # loop through the contours
    j = 0
    for contour in contours:
        # loop through all the points in the contour
        radiiList = []
        thetaList = []
        coordinates = []
        for i in range(len(contour)):
            test = contour[i].flatten()
            test = test.tolist()
            y = test[1]
            x = test[0]
            coordinates.append(test)
            # print(test)
            # need to create a list of the radii values and then add it to the radii array
            radiiList.append(int(math.dist(center, test)))
            thetaList.append(math.atan2(y - center[1], x - center[0]))
        pixelCoordinates.append(coordinates)
        radii[j] = radiiList
        theta[j] = thetaList
        j += 1

    return radii, theta, pixelCoordinates
