from ast import literal_eval
from itertools import groupby, product
from ydata_profiling import ProfileReport
import pandas as pd
import numpy as np


def createReport(query):
    coordinates = []
    partNumbers = []
    distortionLevels = []
    passOrFail = []
    for result in query:
        for pair in literal_eval(result[1]):
            coordinates.append(pair)
            partNumbers.append(result[2])
            distortionLevels.append(result[3])
            passOrFail.append([result[5]])

    pixel_coordinates = coordinates
    pixels = np.array(list(pixel_coordinates))
    distortions = np.array(distortionLevels)
    result = np.array(passOrFail)
    print(len(distortions), len(pixels[:, 0]), len(pixels[:, 1]), len(distortionLevels), len(passOrFail))
    data = pd.DataFrame({'X_Coord': pixels[:, 0], 'Y_Coord': pixels[:, 1], 'Part_Num': partNumbers,
                         'Distortion': distortionLevels, 'Result': result[:, 0]})

    import pdfkit

    report = ProfileReport(data, dark_mode=True, explorative=True,)
    report.to_file("file_name.html")

