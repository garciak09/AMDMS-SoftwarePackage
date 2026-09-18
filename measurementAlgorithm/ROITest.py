# testing region of interest code to determine exact region for each mirror
import sys # to access the system
import cv2

#image1 = "larger_mirror.tiff"
#mirrorType = "1"

image1 = "smaller_mirror.tiff"
mirrorType = 2

image1 = cv2.imread(image1)


if mirrorType == "1":
    image1 = image1[250:1700,60:2340]
else:
    image1 = image1[400:1500, 360:2000]

# Custom window
cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
cv2.imshow('custom window', image1)
cv2.resizeWindow('custom window', 200, 200)

cv2.waitKey(0)
cv2.destroyAllWindows()