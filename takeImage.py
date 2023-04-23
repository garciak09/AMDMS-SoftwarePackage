from pypylon import pylon
from PIL import Image

# variable defintions
# tl_factory = looking for an instance of the pylon
# camera = the camera that is getting connected
# grab = the camera taking a image, grab returns an array
# img = image in array format

def takeImage():

    # connecting the camera
    tl_factory = pylon.TlFactory.GetInstance()
    camera = pylon.InstantCamera()
    camera.Attach(tl_factory.CreateFirstDevice())
    camera.Open()
    # setting the camera gain to max
    camera.Gain = camera.Gain.Max
    # start image capture
    camera.StartGrabbing(1)
    grab = camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)
    if grab.GrabSucceeded():
        # save image as array and to file name image.tiff
        img = grab.GetArray()
        Image.fromarray(grab.Array).save("image.tiff")
        # print(f'Size of image: {img.shape}')
    camera.Close()

    return img

