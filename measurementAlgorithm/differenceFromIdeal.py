# function that calculates h which is the difference from the ideal circle defined by the mode

# variable definitions
# h = array of amount the radii is different from the mode value per contour
# holder = used as a holder variable that is used to append the final array
# radii = array of radius values for each contour
# mode = array of mode values for each contour

def differenceFromIdeal(radii, mode):
    print("differenceFromIdeal")
    h = []
    holder = []
    # loop over each contour
    for i in range(len(radii)):
        # loop over the radii values inside the contour
        for w in range(len(radii[i])):
            holder.append(radii[i][w] - mode[i])
        h.append(holder)
        holder = []

    return h
