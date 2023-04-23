# function that finds the ratio of the distortion

# variable definitions
# distortionLevel = distortion level that is deemed acceptable
# xValue = the area under the curve of the mode radius distribution multiplied by the acceptable distortion level
# ratio1 = divison between area under the "unideal" curve over the ideal curve
# Q = array that holds each ratio value per contour
# results = string that returns pass or fail if the ratio is greater or less than 1

def ratio(mode, area1, h):
    Q = []
    # test commenet
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