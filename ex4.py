from math import degrees, sqrt , sin , radians , tan , cos
import math
from traceback import print_tb

def dd2dms(decimaldegree, mult=1,  direction='x'):
    if type(decimaldegree) != 'float':
        decimaldegree = float(decimaldegree)
    if decimaldegree < 0:
        decimaldegree = -decimaldegree

    minutes = decimaldegree%1.0*60
    seconds = minutes%1.0*60

    return str(int(decimaldegree)*mult)+" "+\
        str(int(minutes))+" "+\
        str(round(seconds,4))  

def triInversa(x, y, z, datum):

    mult = 1

    if datum == "ETRS89":
        a = 6378137
        f = 1 / 298.257222101

    elif datum == "Lisboa":
        f = 1 / 297

    elif datum == "73":
        a = 6378388
        f = 1 / 297
        if y < 0:
            mult = -1
    
    elif datum == "ITRF93":
        a = 6378137
        f = 1 / 298.257222101

    e = sqrt(f*(2-f))

    lon = dd2dms(math.degrees(math.atan(y/x)), mult)

    P = (x**2 + y**2)**0.5
    latApr = math.atan(z/(P * (1 - e**2)))
    deltaLat = 10**(-8)

    while(abs(deltaLat) > 10**(-10)):

        N =  (a / (1 - (e ** 2) * (math.sin(latApr) ** 2)) ** (1/2) )
        h = (P/(math.cos(latApr))) - N

        latF = math.atan((z + e**2 * N * math.sin(latApr))/P)

        deltaLat = latF - latApr
        latApr = latF

    return [dd2dms(math.degrees(latApr)), lon, str(round(h,4))]
