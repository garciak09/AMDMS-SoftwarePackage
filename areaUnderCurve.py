# function to find the area under the curve of each h list
from scipy.integrate import simpson
from numpy import trapz

def areaUnderCurve(h,theta):
    Q = []
    area1 = []
    area2 = []
    sum = 0
    for p in range(len(h)):
        test = h[p]
        # trap1 = trapz(h[p], range(len(h[p])))
        # simpson1 = simpson(h[p], range(len(h[p])))
        trap1 = trapz(h[p],theta[p])
        simpson1 = simpson(h[p],theta[p])
        area1.append(trap1)
        area2.append(simpson1)
        # for i in range(len(h[p])):
        #     sum = sum + (h[p][i])
        # area1.append(sum)
        # sum = 0

    return area1