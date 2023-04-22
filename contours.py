import cv2
import numpy as np

def contours(image):

    # Let's load a simple image with 3 black squares
    #image = cv2.imread(image1)
    #image = image[250:1750,700:1800]
    # cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('custom window', image)
    # cv2.resizeWindow('custom window', 200, 200)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply gaussian filter to reduce noise
    gray = cv2.GaussianBlur(gray,(5,5),0)
    
    # Find Canny edges
    edged = cv2.Canny(gray, 100, 300)
    # cv2.waitKey(0)

    # remove small edges
    # for e in edged:
    #     if (edged[e]==255).sum() <100:
    #         edged.pop(e)
    
    # Finding Contours
    # Use a copy of the image e.g. edged.copy()pip3 install imutils
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    #cv2.imshow('Canny Edges After Contouring', edged)
    #cv2.waitKey(0)
    
    # print("Number of Contours found = " + str(len(contours)))
    
    # Draw all contours
    # -1 signifies drawing all contours
    # cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
    # blank = np.zeros(image.shape[:2],dtype='uint8')
    # cv2.drawContours(blank, contours, -1, (255, 0, 0), 1)
    # cv2.imshow('Contours', blank)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return contours