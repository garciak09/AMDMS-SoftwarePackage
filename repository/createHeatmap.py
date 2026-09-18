from ast import literal_eval
import matplotlib.pyplot as plt
import numpy as np

"""
    This function will get the pixel coordinates where distortion was found in each coordinate.
"""
def extractCoordinates(query):
    coordinates = []
    for result in query:
        for pair in literal_eval(result[1]):
            # if type(pair) is list:
            #     print(pair)
            coordinates.append(pair)
    pixel_coordinates = coordinates #+ list(product(range(0, 5000, 50), range(0, 5000, 50)))
    # frequency = np.array([len(list(group)) - 1 for key, group in groupby(sorted(pixel_coordinates))])
    return np.array(pixel_coordinates)

def createHeatmap(query):
    pixels = extractCoordinates(query)
    # Creating the matplotlib heatmap
    plt.figure(figsize=(8, 6))
    plt.hexbin(pixels[:, 0], pixels[:, 1], gridsize=50, cmap='Reds', edgecolors='w', extent=[0, 5000, 0, 5000])
    plt.xticks(np.arange(0, max(pixels[:, 0])+1, 100))
    plt.yticks(np.arange(0, max(pixels[:, 1])+1, 100))
    plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
    # plt.xticks(rotation=90, ha='right')
    plt.title('Frequency of Distortion in Mirror Locations')
    plt.xlabel('X Location')
    plt.ylabel('Y Location')
    plt.colorbar(label='Frequency', ticks=[])
    plt.savefig('heatmap.png', dpi=300)
    #plt.show()
