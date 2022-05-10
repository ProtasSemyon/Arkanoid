def center(boxSize, elemSize):
    return boxSize[0] // 2 - elemSize[0] // 2, boxSize[1] // 2 - elemSize[1] // 2


def left(boxSize, elemSize):
    return 0, boxSize[1] // 2 - elemSize[1] // 2


def right(boxSize, elemSize):
    return boxSize[0] - elemSize[0], boxSize[1] // 2 - elemSize[1] // 2


def point_in_box(boxStart, boxSize, cursPos):
    return boxStart[0] + boxSize[0] > cursPos[0] > boxStart[0] and boxStart[1] + boxSize[1] > cursPos[1] > boxStart[1]
