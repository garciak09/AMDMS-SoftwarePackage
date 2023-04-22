# function that calculates h which is the difference from the ideal circle defined by the mode

def differenceFromIdeal(radii, mode):
    j = 0
    h = []
    holder = []
    # loop over each contour
    for i in range(len(radii)):
        # w = 0
        # test1 = range(len(radii))
        
        # loop over the radii values inside the contour
        for w in range(len(radii[i])):
            holder.append(radii[i][w] - mode[i])
        h.append(holder)
        holder = []

    return h 