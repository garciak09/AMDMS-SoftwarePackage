

from pypylon import pylon
from PIL import Image

def takeImage():


    tl_factory = pylon.TlFactory.GetInstance()

    camera = pylon.InstantCamera()
    camera.Attach(tl_factory.CreateFirstDevice())

    camera.Open()
    camera.Gain = camera.Gain.Max
    camera.StartGrabbing(1)
    grab = camera.RetrieveResult(2000, pylon.TimeoutHandling_Return)
    if grab.GrabSucceeded():
        img = grab.GetArray()
        Image.fromarray(grab.Array).save("image.tiff")
        print(f'Size of image: {img.shape}')
    camera.Close()

    return img

