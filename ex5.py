import math
import py_compile
import numpy as np

def bursaWolf(X, Y, Z, tCoor):

    if tCoor == "73":
        deltaX = -230.994
        deltaY = 102.591
        deltaZ = 25.199

        Rx = math.radians((0.633/3600))
        Ry = math.radians((-0.239/3600))
        Rz = math.radians((0.9/3600))

        alfaPPM = 1.95 * 10**(-6)
    else:
        deltaX = -283.088
        deltaY = -70.693
        deltaZ = 117.445

        Rx = math.radians((-1.157/3600))
        Ry = math.radians((0.0059/3600))
        Rz = math.radians((-0.652/3600))

        alfaPPM = -4.058 * 10**(-6)

    matrix3 = np.array([[deltaX], [deltaY], [deltaZ]])
    mult = np.dot(np.array([[1, -Rz, Ry],
                    [Rz, 1, -Rx], 
                    [-Ry, Rx, 1]]), np.array([[X], 
                                                [Y], 
                                                [Z]]))
    
    result = []

    for l in range(len(mult)):
        result.append(str(round(mult[l][0] * 
                        (1+alfaPPM) + 
                        matrix3[l][0], 4)))
    return result