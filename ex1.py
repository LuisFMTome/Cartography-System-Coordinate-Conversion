from math import sqrt , sin , cos , radians , tan

def dConv(d, m, s):
    return d + m/60 + s/3600


def calcKs(N, ro, lat):
    k1 = N / ro - (tan(lat) ** 2)
    k2 = N / ro + 4 * (N ** 2 / ro ** 2) - (tan(lat) ** 2)
    k3 = 4 * (N ** 3 / ro ** 3) * (1 - 6 * tan(lat) ** 2) + (N ** 2 / ro ** 2) * (1 + 8 * tan(lat) ** 2) - 2 * (
            N / ro) * tan(lat) ** 2 + tan(lat) ** 4
    k4 = 8 * (N ** 4 / ro ** 4) * (11 - 24 * tan(lat) ** 2) - 28 * (N ** 3 / ro ** 3) * (
                1 - 6 * tan(lat) ** 2) + (
                 N ** 2 / ro ** 2) * (1 - 32 * tan(lat) ** 2) - 2 * (N / ro) * tan(lat) ** 2 + tan(lat) ** 4
    k5 = 61 - 479 * (tan(lat) ** 2) + 179 * (tan(lat) ** 4) - (tan(lat) ** 6)
    k6 = 1385 - 3111 * (tan(lat) ** 2) + 543 * (tan(lat) ** 4) + (tan(lat) ** 6)

    return k1, k2, k3, k4, k5, k6


def calcXeY(k0, sigma, diffLong, N, lat, ro):
    k1, k2, k3, k4, k5, k6 = calcKs(N, ro, lat)

    y = k0 * (sigma + ((diffLong ** 2) / 2) * N * sin(lat) * cos(lat) + ((diffLong ** 4) / 24) * N * sin(
        lat) * (
                      cos(lat) ** 3) * k2 + ((diffLong ** 6) / 720) * N * sin(lat) * (cos(lat) ** 5) * k4 + (
                      (diffLong ** 8) / 40320) * N * sin(lat) * (cos(lat) ** 7) * k6)
    x = k0 * (diffLong * N * cos(lat) + ((diffLong ** 3) / 6) * N * (cos(lat) ** 3) * k1 + (
            (diffLong ** 5) / 120) * N * (cos(lat) ** 5) * k3 + ((diffLong ** 7) / 5040) * N * (
                          cos(lat) ** 7) * k5)

    return round(x, 4), round(y, 4)

def calcN(a, lat, e):
    N = a / ((1 - e ** 2 * sin(lat) ** 2) ** (1 / 2))
    return N

def calcRo(a, e, lat):
    ro = (a * (1 - e ** 2)) / ((1 - e ** 2 * sin(lat) ** 2) ** (3 / 2))
    return ro

def calcA(e):
    return 1 + (3 / 4) * e ** 2 + (45 / 64) * e ** 4 + (175 / 256) * e ** 6 + (11025 / 16384) * e ** 8 + (
                43659 / 65536) * e ** 10

def calcB(e):
    return (3 / 4) * e ** 2 + (15 / 16) * e ** 4 + (525 / 512) * e ** 6 + (2205 / 2048) * e ** 8 + (
                72765 / 65536) * e ** 10

def calcC(e):
    return (15 / 64) * e ** 4 + (105 / 256) * e ** 6 + (2205 / 4096) * e ** 8 + (10395 / 16384) * e ** 10

def calcD(e):
    return (35 / 512) * e ** 6 + (315 / 2048) * e ** 8 + (31185 / 131072) * e ** 10

def calcE(e):
    return (315 / 16384) * e ** 8 + (3465 / 65536) * e ** 10

def calcF(e):
    return (3465 / 131072) * e ** 10

def calcSigma(a, e, lat, lat0):
    A = calcA(e)
    ALat = A * (lat - lat0)

    B = calcB(e)
    BLat = (B / 2) * ((sin(2 * lat)) - (sin(2 * lat0)))

    C = calcC(e)
    CLat = (C / 4) * ((sin(4 * lat)) - (sin(4 * lat0)))

    D = calcD(e)
    DLat = (D / 6) * ((sin(6 * lat)) - (sin(6 * lat0)))

    E = calcE(e)
    ELat = (E / 8) * ((sin(8 * lat)) - (sin(8 * lat0)))

    F = calcF(e)
    FLat = (F / 10) * ((sin(10 * lat)) - (sin(10 * lat0)))

    sigma = a * (1 - e ** 2) * (ALat - BLat + CLat - DLat + ELat - FLat)

    return sigma

def calc(a, e, lat, lat0, diffLong, k0):
    sigma = calcSigma(a, e, lat, lat0)
    ro = calcRo(a, e, lat)
    N = calcN(a, lat, e)
    return calcXeY(k0, sigma, diffLong, N, lat, ro)

def minutesToDegrees(lista):
    graus = lista[0]
    minutos = lista[1]
    segundos = lista[2]
    if (graus < 0):
        minutos = -(minutos)
        segundos = -(segundos)

    return graus + minutos/60 + segundos/3600

def geodesicasToPlanas(lat, long, tipo):
    
    lat = lat.split(" ")
    long = long.split(" ")

    lat[0] = int(lat[0])
    lat[1] = int(lat[1])
    lat[2] = float(lat[2])
    long = [-(int(long[0])), int(long[1]), float(long[2])]

    lat = minutesToDegrees(lat)
    long = minutesToDegrees(long)
    
    if tipo == "ETRS89":
        return toETRS89(lat, long)
    elif tipo == "DATUMLISBOA":
        return toDatumLisboa(lat, long)
    elif tipo == "DATUM73":
        return toDatum73(lat, long)
    elif tipo == "ITRF93":
        return toITRF93(lat, long)

def toITRF93(lat, long):
    a = 6378137
    f = 1 / 298.257222101
    e = sqrt(f * (2 - f))

    lat = radians(lat)
    longDeg = abs(long)
    long = radians(long)

    if 12 < longDeg < 18:
        long0 = radians(-15)
    elif 24 < longDeg < 30:
        long0 = radians(-27)
    elif 30 < longDeg < 36:
        long0 = radians(-33)

    diffLong = long - long0

    x, y = calc(a, e, lat, 0, diffLong, 0.9996)
    print()
    print(round((x + 500000), 4), round(y, 4))
    print()
    #return round((x + 500000), 4), round(y, 4)

def guassDireta(lat, lon, datum, fuso = ""):

    if datum == "ETRS89":
        lat0 = radians(dConv(39, 40, 5.73))
        lon0 = radians(-dConv(8, 7, 59.19))
        a = 6378137
        f = 1 / 298.257222101
        m0=0
        p0=0
        k=1

    elif datum == "Lisboa":
        lat0 = radians(dConv(39, 40, 0))
        lon0 = radians(-dConv(8, 7, 54.862))
        a = 6378388
        f = 1 / 297
        m0=0
        p0=0
        k=1

    elif datum == "73":
        lat0 = radians(dConv(39, 40, 0))
        lon0 = radians(-dConv(8, 7, 54.862))
        a = 6378388
        f = 1 / 297
        m0=180.598
        p0=-86.990
        k=1
    
    elif datum == "PTRA08-UTM/ITRF93":
        lat0 = radians(dConv(0, 0, 0))

        if fuso == "25":
            lon0 = radians(-dConv(33, 0, 0))
        elif fuso == "26":
            lon0 = radians(-dConv(27, 0, 0))
        elif fuso == "28":
            lon0 = radians(-dConv(15, 0, 0))

        a = 6378137
        f = 1 / 298.257222101
        m0=500000
        p0=0
        k=0.9996

    lat = lat.split(" ")
    lon = lon.split(" ")

    if float(lon[0]) < 0:
        lon[0] = str(-float(lon[0]))

    latRad = radians(dConv(float(lat[0]), float(lat[1]), float(lat[2])))
    lonRad = -radians(dConv(float(lon[0]), float(lon[1]), float(lon[2])))

    sinLat = sin(latRad)
    sinLon = sin(lonRad)

    cosLat = cos(latRad)
    cosLon = cos(lonRad)

    e = sqrt(f*(2-f))
    ldiff = lonRad - lon0
    N = a / ((1 - (e**2)*(sinLat**2))**0.5)
    ro = (a*(1-e**2)) / ((1-(e**2)*(sinLat**2))**(3/2))

    k1 = (N / ro) - (tan(latRad)**2)
    k2 = (N / ro) + (4 * ((N**2) / (ro**2))) - (tan(latRad)**2)
    k3 = (4 * ((N**3) / (ro**3))) * (1 - (6*(tan(latRad)**2))) + ((N**2) / (ro**2)) * (1+8*(tan(latRad)**2)) - 2 * (N/ro) * (tan(latRad)**2) + (tan(latRad)**4)
    k4 = 8 * (((N**4)/(ro**4)) * (11 - 24 * tan(latRad)**2)) - 28 * (((N**3)/(ro**3)) * (1 - 6*(tan(latRad)**2))) + (((N**2)/(ro**2)) * (1-32*(tan(latRad)**2))) - 2 * (N/ro) * (tan(latRad)**2) + (tan(latRad)**4)
    k5 = 61-479*(tan(latRad)**2)+179*(tan(latRad)**4) - (tan(latRad)**6)
    k6 = 1385 - 3111 * (tan(latRad)**2) + 543 * (tan(latRad)**4) - (tan(latRad)**6)

    A = 1 + (3/4)*(e**2) + (45/64)*(e**4) + (175/256)*(e**6) + (11025/16384)*(e**8) + (43659/65536)*(e**10)
    B = (3/4)*(e**2) + (15/16)*(e**4) + (525/512)*(e**6) + (2205/2048)*(e**8) + (72765/65536)*(e**10)
    C = (15/64)*(e**4) + (105/256)*(e**6) + (2205/4096)*(e**8) + (10395/16384)*(e**10)
    D = (35/512)*(e**6) + (315/2048)*(e**8) + (31185/131072)*(e**10)
    E = (315/16384)*(e**8) + (3465/65536)*(e**10)
    F = (3465/131072)*(e**10)

    sigmaAP = (latRad - lat0) * (A*a*(1-e**2))

    deltaLat = 10**(-8)
        
    partA = (A * (latRad-lat0))
    partB = ((B/2) * (sin(2*latRad) - sin(2*lat0)))
    partC = ((C/4) * (sin(4*latRad) - sin(4*lat0)))
    partD = ((D/6) * (sin(6*latRad) - sin(6*lat0)))
    partE = (E/8) * (sin(8*latRad) - sin(8*lat0))
    partF = ((F/10) * (sin(10*latRad) - sin(10*lat0)))

    sigma = a * (1-e**2)*(partA - partB + partC - partD + partE - partF)

    ro = a*(1-e**2)/(1-(e**2)*(sinLat**2))**(3/2)
        
    #calculo de y
    parte1y = ((ldiff**2) / 2) * N * sinLat * cosLat
    parte2y = ((ldiff**4) / 24) * (N * sinLat * cosLat**3) * k2
    parte3y = ((ldiff**6) / 720) * (N * sinLat * cosLat**5) * k4
    parte4y = ((ldiff**8) / 40320) * (N * sinLat * cosLat**7) * k6
    y = k * (sigma + parte1y + parte2y + parte3y + parte4y)
    y += p0

    #calculo de x
    parte1x = ldiff*N*cosLat
    parte2x = (((ldiff)**3) / 6) * N * (cosLat**3) * k1
    parte3x = (((ldiff)**5) / 120) * N * (cosLat**5) * k3
    parte4x = (((ldiff)**7) / 5040) * N * (cosLat**7) * k5
    x = k * (parte1x + parte2x + parte3x + parte4x)
    x += m0
    return [str(round(x, 4)), str( round(y, 4))]
