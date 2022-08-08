import math
import py_compile

def molodenski(lat, lon, h, datum):
    
    lat = lat.split(" ")
    lon = lon.split(" ")
    h = float(h)

    latRad = math.radians(float(lat[0]) +\
                            float(lat[1]) / 60 +\
                            float(lat[2]) / 3600)

    lonRad = math.radians(-(float(lon[0]) +\
                            float(lon[1]) / 60 +\
                            float(lon[2]) / 3600))

    sinLat = math.sin(latRad)
    sinLon = math.sin(lonRad)
    cosLat = math.cos(latRad)
    cosLon = math.cos(lonRad)

    if datum == "Lisboa":

        deltaX = -303.861
        deltaY = -60.693
        deltaZ = 103.607
        delta_a = -251
        delta_f = -1.4192686*(10**(-5))
        a = 6378388
        f = 1/297
        b = a*(1-f)
        e = math.sqrt(f*(2-f))
        eSQRD = f*(2-f)
        N = a / (1 - eSQRD * sinLat**2)**0.5
        ro = a * (1-eSQRD)/((1 - eSQRD) * sinLat**2)**(3/2)

    elif datum == "73":

        deltaX = -223.150
        deltaY = 110.132
        deltaZ = 36.711
        delta_a = -251.0
        delta_f = -1.4192686*(10**(-5))
        a = 6378388
        f = 1/297
        b = a*(1-f)
        e = math.sqrt(f*(2-f))
        N = a / ((1 - (e**2)*(sinLat**2))**0.5)
        ro = (a*(1-e**2)) / ((1-(e**2)*(sinLat**2))**(3/2))
        
    
    latX = -deltaX*(sinLat*cosLon)
    latY = -deltaY*(sinLat*sinLon)
    latZ = deltaZ*cosLat
    latA = delta_a*(((e**2)*N*(sinLat*cosLat))/a)
    latF = (delta_f*(sinLat*cosLat))*((a/b)*ro+(b/a)*N)

    latNume = (latX+latY+latZ+latA+latF)
    latDeno = ro+h

    latN = math.degrees(latRad+(latNume/latDeno))

    lonX = -deltaX*sinLon
    lonY = deltaY*cosLon
    lonNume = (lonX) + lonY
    lonDeno = (N+h)*cosLat
    lonN = -(math.degrees(lonRad+(lonNume/lonDeno)))

    h_n = h +\
        (deltaX*(cosLat*cosLon))+\
        (deltaY*(cosLat*sinLon))+\
        (deltaZ*sinLat)-\
        (delta_a*(a/N))+\
        (delta_f*((b/a)*N*(sinLat**2)))

    latDegree = latN - (latN - int(latN))
    latMinute = (latN - int(latN))*60
    latSecond = (latMinute - int(latMinute))*60

    lonDegree = lonN - (lonN - int(lonN))
    lonMinute = (lonN - int(lonN))*60
    lonSecond = (lonMinute - int(lonMinute))*60

    return [str(int(latDegree))+" "+str(int(latMinute))+" "+str(round(latSecond, 5)),
            str(int(lonDegree))+" "+str(int(lonMinute))+" "+str(round(lonSecond, 5)),
            str(round(h_n, 4))]
