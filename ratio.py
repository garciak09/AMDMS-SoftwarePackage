# function that finds the ratio of the distortion

def ratio(mode, area1, h):
    Q = []
    distortionLevel = 0.0011
    for m in range(len(area1)):
        xValue = distortionLevel * mode[m] * len(h[m])
        ratio1 = abs(area1[m] / xValue)
        Q.append(ratio1) 

    # print pass or fail
    # loop through each contour
    for i in range(len(mode)):
        if Q[i] > 1:
            print("Fail")
            results = "Fail"
            break
        elif Q[i] <= 1:
            results = "Pass"

    print(results)

    return results, distortionLevel