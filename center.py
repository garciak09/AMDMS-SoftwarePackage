# function to find the center of the image
import cv2

def centerImage(image):
    height, width = image.shape[:2]
    center = [height/2,width/2]

    return center