import cv2
import numpy as np


# variable definitions
# gray = grayscale version of image from camera
# gray = grayscale image after a guassian filter is applied
# edged = the edges in the image formatted as pixel locations in an array
# contours = the pixel locations of contours defined from the edges
# hierarchy = hierarchy chosen for the contours

def contours(image):
    print("contours")

    # section can be used to view the image the camera is taking
    # cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('custom window', image)
    # cv2.resizeWindow('custom window', 1000, 1000)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply gaussian filter to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Find Canny edges
    edged = cv2.Canny(gray, 100, 300)
    # cv2.waitKey(0)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()pip3 install imutils
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # draw the edges of the image
    # cv2.imshow('Canny Edges After Contouring', edged)
    # cv2.waitKey(0)

    # Draw all contours
    # -1 signifies drawing all contours
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    # blank = np.zeros(image.shape[:2], dtype='uint8')
    # cv2.drawContours(blank, contours, -1, (255, 0, 0), 1)
    #
    # cv2.imshow('Contours', blank)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return contours
