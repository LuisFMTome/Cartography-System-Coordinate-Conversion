import ex1, ex2, ex3, ex4, ex5, ex6, ex7, os, sys

op = "Transformacao de coordenadas: \n"+\
    "+----------------------+ \n"+\
    "|Mesmo datum -------> 1| \n"+\
    "+----------------------+ \n"+\
    "|Datum diferentes --> 2| \n"+\
    "+----------------------+ \n"+\
    "|Limpar Interface --> 3| \n"+\
    "+----------------------+ \n"+\
    "|Sair --------------> 4| \n"+\
    "+----------------------+ \n"+\
    "Opcao --------------> "

op1 = "Qual Datum: \n" + \
    "+-------------------+ \n" +\
    "|ETRS89 ---------> 1| \n" +\
    "+-------------------+ \n" +\
    "|Datum Lisboa ---> 2| \n" +\
    "+-------------------+ \n" +\
    "|Datum 73 -------> 3| \n" +\
    "+-------------------+ \n" +\
    "|ITRF93 ---------> 4| \n" +\
    "+-------------------+ \n" +\
    "Opcao: "

datumDiferenteES = "Datum Entrada e Saida:\n"+\
    "+------------------------+ \n"+\
    "|Datum Lisboa/ETRS89 -> 1| \n"+\
    "+------------------------+ \n"+\
    "|Datum 73/ETRS89 -----> 2| \n"+\
    "+------------------------+ \n"+\
    "Opcao: "

transformacao = "Transformacao:\n"+\
    "+-----------------------+ \n"+\
    "|Bursa-Wolf ---------> 1| \n"+\
    "+-----------------------+ \n"+\
    "|Molodenski ---------> 2| \n"+\
    "+-----------------------+ \n"+\
    "|Polinomial 2º grau -> 3| \n"+\
    "+-----------------------+ \n"+\
    "Opcao: "

coorIODiffDatum = "Coordenadas de entrada e saida:\n"+\
    "+--------------------------------+ \n"+\
    "| Cartesianas/Cartesianas ----> 1| \n"+\
    "+--------------------------------+ \n"+\
    "| Cartesianas/Geográficas ----> 2| \n"+\
    "+--------------------------------+ \n"+\
    "| Cartesianas/Retangulares ---> 3| \n"+\
    "+--------------------------------+ \n"+\
    "| Geográficas/Cartesianas ----> 4| \n"+\
    "+--------------------------------+ \n"+\
    "| Geográficas/Geográficas ----> 5| \n"+\
    "+--------------------------------+ \n"+\
    "| Geográficas/Retangulares ---> 6| \n"+\
    "+--------------------------------+ \n"+\
    "| Retangulares/Cartesianas ---> 7| \n"+\
    "+--------------------------------+ \n"+\
    "| Retangulares/Geográficas ---> 8| \n"+\
    "+--------------------------------+ \n"+\
    "| Retangulares/Retangulares --> 9| \n"+\
    "+--------------------------------+ \n"+\
    "Opcao: "

coorIOMesmoDatum = "Coordenadas de entrada e saida: \n" +\
    "+------------------------------+ \n" +\
    "|Cartesianas/Geográficas  --> 1| \n" +\
    "+------------------------------+ \n" +\
    "|Cartesianas/Retangulares --> 2| \n" +\
    "+------------------------------+ \n" +\
    "|Geograficas/Retangulares --> 3| \n" +\
    "+------------------------------+ \n" +\
    "|Geográficas/Cartesianas  --> 4| \n" +\
    "+------------------------------+ \n" +\
    "|Retangulares/Geográficas --> 5| \n" +\
    "+------------------------------+ \n" +\
    "|Retangulares/Cartesianas --> 6| \n" +\
    "+------------------------------+ \n" +\
    "Opcao: "

op11 = "Coordenadas Cartesianas: \n"+\
    "-Formato: X Y Z \n"+\
    "-Exemplo: 4993821.5571 -676850.4038 3896819.7516 \n"+\
    "Coordenadas: "

op14 = "Coordenadas Geograficas: \n"+\
    "-Formato: Latitude Longitude h \n"+\
    "-Exemplo: 37 53 58.7635;7 43 7.2999;257.85 \n"+\
    "Coordenadas: "

op16 = "Coordenadas Retangulares: \n"+\
    "-Formato: M P h \n"+\
    "-Exemplo: 36448.61 -196253.96 257.85 \n"+\
    "Coordenadas: "

def clearUI():
    os.system('powershell.exe clear')

def resultadoCartesiano(x, y, z):
    print("Resultado:")
    print("X -> "+x)
    print("Y -> "+y)
    print("Z -> "+z)
    print()

def resultadoGeografico(lat, lon, h):
    print("Resultado:")
    print("Latitude ---> "+lat)
    print("Longitude --> "+lon)
    print("h ----------> "+h)
    print()

def resultadoRetangular(m, p, h):
    print("Resultado:")
    print("M -> "+m)
    print("P -> "+p)
    print("h -> "+h)
    print()

def cg(c, datum):
    return ex4.triInversa(float(c[0]), float(c[1]), float(c[2]), datum)

def cr(c, datum):
    r = ex4.triInversa(float(c[0]), float(c[1]), float(c[2]), datum)
    h = r[2]
    r = ex1.guassDireta(r[0], r[1], datum)
    r.append(h)
    return r

def gr(c, datum):
    return ex1.geodesicasToPlanas(c[0], c[1], datum)

def gc(c, datum):
    return ex3.triDireta(c[0], c[1], c[2], datum)

def rg(c, datum):
    return ex2.gaussInversa(c[0], c[1], datum)

def rc(c, datum):
    r = ex2.gaussInversa(c[0], c[1], datum)
    return ex3.triDireta(r[0], r[1], c[2], datum)

def inOutCoorMesmoDatum(datum, coorIO):
    if coorIO in "1 cg":
        print()
        r = cg(input(op11).split(" "), datum)
        resultadoGeografico(r[0], r[1], r[2])
    elif coorIO in "2 cr":
        print()
        r = cr(input(op11).split(" "), datum)
        resultadoRetangular(r[0], r[1], r[2])
    elif coorIO in "3 gr":#ESTE###########
        print()
        c = input(op14).split(";")
        r = gr(c, datum)
        #resultadoRetangular(r[0], r[1], c[2])
    elif coorIO in "4 gc":
        print()
        r = gc(input(op14).split(";"), datum)
        resultadoCartesiano(r[0], r[1], r[2])
    elif coorIO in "5 rg":
        print()
        c = input(op16).split(" ")
        r = rg(c, datum)
        resultadoGeografico(r[0], r[1], c[2])
    elif coorIO in "6 rc":
        print()
        r = rc(input(op16).split(" "), datum)
        resultadoCartesiano(r[0], r[1], r[2])

clearUI()

while True:

    ini = input(op)
    print()

    if ini == "1":
        
        op1d = input(op1)
        print()
        coorIO = input(coorIOMesmoDatum)

        if op1d == "1":
            inOutCoorMesmoDatum("ETRS89", coorIO)
        elif op1d == "2":
            inOutCoorMesmoDatum("Lisboa", coorIO)
        elif op1d == "3":
            inOutCoorMesmoDatum("73", coorIO)
        elif op1d == "4":
            inOutCoorMesmoDatum("ITRF93", coorIO)
            
    elif ini == "2":

        op2 = input(datumDiferenteES)
        
        if op2 in "2 Datum 73/ETRS89":
            print()
            op22 = input(transformacao)
            if op22 in "1 Bursa-Wolf":
                print()
                c = input(coorIODiffDatum)

                if c in "1 cc":
                    print()
                    c = input(op11).split(" ")
                    r = ex5.bursaWolf(float(c[0]), float(c[1]), float(c[2]), "73")
                    resultadoRetangular(r[0], r[1], r[2])

                elif c in "4 gc":
                    print()
                    c = input(op14).split(";")
                    r = gc(c, "73")
                    print("gc",r)
                    r = ex5.bursaWolf(float(r[0]), float(r[1]), float(r[2]), "73")
                    resultadoCartesiano(r[0], r[1], r[2])

                elif c in "9 rr":
                    print()
                    c = input(op16).split(" ")
                    r = rc(c, "73")
                    r = ex5.bursaWolf(float(r[0]), float(r[1]), float(r[2]), "73")
                    r = cr(r, "ETRS89")
                    resultadoRetangular(r[0], r[1], r[2])

            elif op22 in "2 Molodenski":
                print()
                c = input(coorIODiffDatum)
                if c in "5 Geográficas/Geográficas":
                    print()
                    c = input(op14).split(";")
                    r = ex6.molodenski(c[0], c[1], c[2], "73")
                    resultadoGeografico(r[0], r[1], r[2])

            elif op22 in "3 Polinomial 2º grau":
                print()
                c = input(coorIODiffDatum)
                if c in "9 rr":
                    print()
                    c = input(op16).split(" ")
                    r = ex7.polinomial(c[0], c[1], "73")
                    resultadoCartesiano(r[0], r[1], c[2])

    elif ini in "3 limpar clear":
        os.system('powershell.exe clear')

    elif ini in "4 sair exit":
        os.system('powershell.exe clear')
        sys.exit()
