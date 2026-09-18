# function to find the center of the image
import cv2


# variable definitions
# height = height of image in pixels
# width = width of image in pixels
# center = pixel location of center of image

def centerImage(image):
    print("centerImage")
    height, width = image.shape[:2]
    center = [height / 2, width / 2]

    return center
