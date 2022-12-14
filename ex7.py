#EX7:

def polinomial(X, Y, datum):

    X = float(X)
    Y = float(Y)

    if datum == "Lisboa":
        a0 = 1.38051
        a1 = 129998.56256
        a2 = -1.69483
        a3 = -0.57226
        a4 = -2.9606
        a5 = -2.45601
        b0 = 0.80894
        b1 = 1.31669
        b2 = 279995.74505
        b3 = 0.24888
        b4 = 2.65999
        b5 = -3.86484
        x0 = 0
        y0 = 0

    elif datum == "73":
        a0 = 0.28961
        a1 = 129999.16977
        a2 = -5.26888
        a3 = 0.32257
        a4 = -0.87853
        a5 = -1.22237
        b0 = -0.08867
        b1 = 2.39595
        b2 = 279997.91435
        b3 = 0.15146
        b4 = 1.11109
        b5 = -1.06143
        x0 = 0
        y0 = 0

    h = 130000
    k = 280000

    u = X/h
    v = Y/k

    M = a0 + a1 * u + a2 * v + a3 * (u**2) + a4 * u * v + a5 * (v**2)
    P = b0 + b1 * u + b2 * v + b3 * (u**2) + b4 * u * v + b5 * (v**2)

    return [str(round(M, 4)), str(round(P, 4))]
