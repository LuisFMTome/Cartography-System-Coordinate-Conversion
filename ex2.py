from math import degrees, sqrt , sin , radians , tan , cos

def dConv(d, m, s):
    return d + m/60 + s/3600

def decdeg2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (degrees,minutes,round(seconds,4))

def gaussInversa(m, p, datum, fuso = ""):

    m = float(m)
    p = float(p)
    mult=1

    if datum == "ETRS89":
        lat0 = radians(dConv(39, 40, 5.73))
        lon0 = -radians(dConv(8, 7, 59.19))
        a = 6378137
        f = 1 / 298.257222101
        m0=0
        p0=0
        k=1

    elif datum == "Lisboa":
        lat0 = radians(dConv(39, 40, 0))
        lon0 = -radians(dConv(8, 7, 54.862))
        a = 6378388
        f = 1 / 297
        m0=0
        p0=0
        k=1

    elif datum == "73":
        lat0 = radians(dConv(39, 40, 0))
        lon0 = -radians(dConv(8, 7, 54.862))
        a = 6378388
        f = 1 / 297
        m0=-180.598
        p0=86.990
        k=1
        
        if p < 0:
            mult = -1
    
    elif datum == "ITRF93":
        lat0 = radians(dConv(0, 0, 0))

        if fuso == "25":
            lon0 = -radians(dConv(33, 0, 0))
        elif fuso == "26":
            lon0 = -radians(dConv(27, 0, 0))
        elif fuso == "28":
            lon0 = -radians(dConv(15, 0, 0))

        a = 6378137
        f = 1 / 298.257222101
        m0=-500000
        p0=0
        k=0.9996

    e = sqrt(f*(2-f))
    m+=m0
    p+=p0

    A = 1 + 3/4*(e**2) + 45/64*(e**4) + 175/256*(e**6) + 11025/16384*(e**8) + 43659/65536*(e**10)
    B = 3/4*(e**2) + 15/16*(e**4) + 525/512*(e**6) + 2205/2048*(e**8) + 72765/65536*(e**10)
    C = 15/64*(e**4) + 105/256*(e**6) + 2205/4096*(e**8) + 10395/16384*(e**10)
    D = 35/512*(e**6) + 315/2048*(e**8) + 31185/131072*(e**10)
    E = 315/16384*(e**8) + 3465/65536*(e**10)
    F = 3465/131072*(e**10)

    sigmaAP = p/k
    lat = lat0 + (sigmaAP/(A*a*(1-e**2)))
    delta_lat = 10**(-8)
    N = a/(1-e**2*sin(lat)**2)**0.5

    while(abs(delta_lat) > 10**(-10)):

        partA = (A* (lat-lat0))
        partB = ((B/2) * (sin(2*lat) - sin(2*lat0)))
        partC = ((C/4) * (sin(4*lat) - sin(4*lat0)))
        partD = ((D/6) * (sin(6*lat) - sin(6*lat0)))
        partE = ((E/8) * (sin(8*lat) - sin(8*lat0)))
        partF = ((F/10) * (sin(10*lat) - sin(10*lat0)))

        sigma = a * (1-e**2)*(partA - partB + partC - partD + partE - partF)
        ro = a*(1-e**2)/(1-(e**2)*(sin(lat)**2))**(3/2)
        delta_lat = (sigmaAP - sigma)/ro
        lat = lat + delta_lat

    N = a/(1-e**2*sin(lat)**2)**0.5
    ro = a*(1-e**2)/(1-(e**2)*(sin(lat)**2))**(3/2)
    tridente = N / ro
    t = tan(lat)

    part1 = (t/(k*ro))*((m**2)/(2*k*N))
    part2 = (t/(k*ro))*((m**4)/(24*(k**3)*(N**3))) * (-4*(tridente**2) + 9*tridente * (1-(t**2)) + 12*(t**2))
    part3 = (t/(k*ro))*((m**6)/(720*(k**5)*(N**5)))
    part4 = 8*(tridente**4) * (11-(24*(t**2))) - 12*(tridente**3) * (21-71*(t**2)) + 15*(tridente**2) * (15 - 98*(t**2) + 15*(t**4)) + 180*tridente * (5*(t**2) - 3*(t**4) - 360*(t**4))
    part5 = (t/(k*ro))*((m**8)/(40320*(k**7)*(N**7))) * (1385 + 3633*(t**2) + 4095*(t**4) + 1575*(t**6))


    latF = lat - part1 + part2 - part3 * part4 + part5
    latF = degrees(latF)
    latF = decdeg2dms(latF)

    parte1 = (m/(k*N))
    parte2 = ((m**3)/(6*(k**3)*(N**3))) * (tridente + 2*(t**2))
    parte3 = ((m**5)/(120*(k**5)*(N**5))) * (-4*(tridente**3) * (1-(6*(t**2))) + tridente**2 * (9-(68*(t**2))) + 72*tridente*(t**2) + 24*(t**2))
    parte4 = ((m**7)/(5040*(k**7)*(N**7))) * (61 + (662*(t**2)) + 1320*(t**4) + 720*(t**6))

    termo = parte1 - parte2 + parte3 - parte4
    numerador = termo + lon0*cos(lat)
    lonF = (numerador/cos(lat))
    lonF = degrees(lonF)
    lonF = decdeg2dms(lonF)

    return [str(int(latF[0]))+" "+str(int(latF[1]))+" "+ str(latF[2]) , 
            str(int(lonF[0])*mult)+" "+str(int(lonF[1]))+" "+ str(lonF[2])]
