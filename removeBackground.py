'''
    This file is used to remove the background of any image given as an input to the
    removeBG function. The string path of the image without the background is returned.
'''

from rembg import remove
from PIL import Image
import time

"""
    imagePath: string that is the path of image whose background will be removed.
"""


def removeBG(imagePath):
    # Store path of the image in the variable input_path
    start = time.time()
    input_path = imagePath

    # Store path of the output image in the variable output_path
    output_path = 'new_image.tiff'

    # Processing the image
    input = Image.open(input_path)

    # Removing the background from the given Image
    output = remove(input)

    # Saving the image in the given path
    output.save(output_path)
    print("new image saved!")
    # print(f'runtime: {time.time() - start}')

    return "new_image.tiff"
