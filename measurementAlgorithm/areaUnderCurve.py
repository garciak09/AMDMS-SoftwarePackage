# function to find the area under the curve of each h list
from scipy.integrate import simpson
from numpy import trapz


# variable definitions
# Q 
# area1 is the area under the curve calculated using the trapezoid method
# area2 is the area under the curve calculated using the simpson method
# trap1 is the holder variable for the trapezoid method
# simpson1 is the holder variable for the simpson method
# theta is the array holding the angle values for the contours
# h is the array that holds the difference from ideal values for the contours

def areaUnderCurve(h, theta):
    print("areaUnderCurve")
    area1 = []
    area2 = []
    # loop through contours
    for p in range(len(h)):
        # calculate the area under the curve numerically
        trap1 = trapz(h[p], theta[p])
        simpson1 = simpson(h[p], theta[p])
        # append the area arrays for each contour
        area1.append(trap1)
        area2.append(simpson1)

    return area1
