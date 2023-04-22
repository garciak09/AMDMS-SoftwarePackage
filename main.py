# the main file where all the functions will be called/run from
from contours import contours
from radiusSampling import radiusSampling
from modeRadius import modeRadius
import numpy as np
from differenceFromIdeal import differenceFromIdeal
from areaUnderCurve import areaUnderCurve
from ratio import ratio
from center import centerImage
from takeImage import takeImage
import cv2

# import image
# image1 = "./IMG_0258.jpeg"
# img = takeImage()
image1 = "4lightscardboard.tiff"
mirrorType = "1"

image = cv2.imread(image1)

# select ROI based on mirror size
if mirrorType == "1":
    image1 = image[250:1700,60:2340]
else:
    image1 = image[400:1500, 360:2000]

# find contours
contours = contours(image1)
# contours = circleContours(image1)

# finding the radii of the contours
# returns an array with each element being a list of the radii values per contour
# find the center of the image
center = centerImage(image1)
radii, theta = radiusSampling(contours, center)

# find most often radius
# returns a list of the mode radius for each contour
radiiMode = modeRadius(radii)

# define the difference between the ideal and measure circles
# returns a list
# each element in the list is an array for each contour
# these lists are the difference of the actual radii values and the mode radii value
h = differenceFromIdeal(radii, radiiMode)

# find the area under the curve for each element in h
# returns a list of areas, each element is for a different contour
area = areaUnderCurve(h,theta)

# take the ratio of the area under h to the area under the mode * (distortion level)
ratio(radiiMode,area, h)