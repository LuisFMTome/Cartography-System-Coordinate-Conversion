from math import degrees, sqrt , sin , radians , tan , cos

def dConv(d, m, s):
    return d + m/60 + s/3600

def minutesToDegrees(lista):
    graus = lista[0]
    minutos = lista[1]
    segundos = lista[2]
    if (graus < 0):
        minutos = -(minutos)
        segundos = -(segundos)

    return graus + minutos/60 + segundos/3600

def geodesicasToCatersianas(lat, long, h, tipo):
    if tipo == "DATUM73":
        a = 6378388
        f = 1 / 297
    else:
        a = 6378137
        f = 1 / 298.257222101


    lat = minutesToDegrees(lat)
    long = [-(long[0]), long[1], long[2]]
    long = minutesToDegrees(long)

    e = sqrt(f * (2 - f))
    N = calcN(a, radians(lat), e)

    X = (N + h) * cos(radians(lat)) * cos(radians(long))
    Y = (N + h) * cos(radians(lat)) * sin(radians(long))
    Z = ((1 - (e ** 2)) * N + h) * sin(radians(lat))

    return [round(X, 4), round(Y, 4), round(Z, 4)]

def triDireta(lat, lon, h, datum):

    if datum == "ETRS89":
        a = 6378137
        f = 1 / 298.257222101

    elif datum == "Lisboa":
        a = 6378388
        f = 1 / 297

    elif datum == "73":
        a = 6378388
        f = 1 / 297
    
    elif datum == "ITRF93":
        a = 6378137
        f = 1 / 298.257222101

    e = sqrt(f*(2-f))

    lat = lat.split(" ")
    lon = lon.split(" ")

    if float(lon[0]) < 0:
        lon[0] = str(-float(lon[0])) 

    latRad = radians(dConv(float(lat[0]), float(lat[1]), float(lat[2])))
    if float(lon[0]) < 0:
           lon[0] = -float(lon[0])
    lonRad = -radians(dConv(float(lon[0]), float(lon[1]), float(lon[2])))


    h = float(h)

    sinLat = sin(latRad)
    sinLon = sin(lonRad)
    cosLat = cos(latRad)
    cosLon = cos(lonRad)

    N = a / ((1 - (e**2)*(sinLat**2))**0.5)

    x = (N+h) * cosLat * cosLon
    y = (N+h) * cosLat * sinLon
    z = (((1-(e**2))*N+h))*sinLat

    return [str(round(x,4)), str(round(y,4)), str(round(z,4))]