# -*- coding: utf-8 -*-
import os
import random
import time

print()
print("*****  Tervetuloa pelaamaan Miinaharavaa! *****")
print()


def alkuvalikko():
    """
    Aloittaa ohjelman ja toimii pelin alkupisteenä. Tulostuu aina pelin päättyessä. Ohjelma päättyy vasta kun pelaaja valitsee "4. Poistu pelistä".
    """
    while True:
        print()
        print("1. Aloita uusi peli")
        print("2. Ohjeet")
        print("3. Tilastot")
        print("4. Poistu pelistä")
        try:
            aloitus = int(input("- Syötä valintasi kirjoittamalla jokin numeroista 1-4: "))
            if aloitus <= 0 or aloitus > 4:
                print(">>> Valitse jokin numeroista 1-4")
        except ValueError:
            print(">>> Anna valintasi kokonaislukuna!")
            continue
        else:
            if aloitus == 1:
                break
            elif aloitus == 2:
                print()
                print(" - Ohjeet:")
                print()
                print("Miinaharavassa käytössä on pelilauta, jonka kaikki ruudut ovat alussa paljastamattomia.")
                print("Pelin ideana on avata kaikki pelilaudan ruudut ('-'-merkatut) osumatta miinoihin.")
                print("Tyhjät/avatut ruudut merkataan välilyönnillä ja numeroruudut tarkoittavat niitä ympäröivien miinojen lukumäärää eli max. 8.")
                print("Voit avata ruutuja syöttämällä laudan syöttämällä laudan koordinaatteja tai merkitä miinan paikan syöttämällä ensin x.")
                print("Peli päättyy, kun osut miinaan tai avaat kaikki ruudut joissa ei ole miinaa.")
                print()
                input("- Paina enteriä päästäksesi takaisin päävalikoon. ")
            elif aloitus == 3:
                print()
                try:
                    with open("tulokset.txt") as lahde:
                        print(" - Tilastot näkyvät vanhimmasta uusimpaan.")
                        print()
                        for rivi in lahde.readlines():
                            print(rivi)
                except FileNotFoundError:
                    print(">>> Edellisiä tilastoja ei ole")
                    continue
                print("Paina enteriä päästäksesi takaisin päävalikoon tai jos haluat poistaa edelliset tilastot syötä 'p'.")
                if input("- Syötä valintasi: ") == "p":
                    print("Oletko varma, että haluat poistaa kaikki edelliset tilastot?")
                    if input("- Syötä 'p' jos haluat poistaa muuten paina enteriä. ") == "p":
                        os.remove("tulokset.txt")
                        print(">>> Tilastot poistettu.")
            elif aloitus == 4:
                print()
                print("Lopetit pelin")
                return "q"


def kysy_koko():
    """
    Kysyy pelaajalta minkä kokoisen kentän haluaa ja palauttaa kentän koon ja miinat sen mukaan.
    """
    print()
    print("Voit valita valmiin kentän valitsemalla jonku kolmesta vaikeustasosta tai omatekoisen kentän.")
    print("1 Helppo - Kentän koko on 9 x 9 ruutua ja miinoja on 10.")
    print("2 Keskivaikea - Kentän koko on 16 x 16 ruutua ja miinoja on 40.")
    print("3 Vaikea - Kentän koko on 30 x 16 ruutua ja miinoja on 99.")
    print("4 Kustomoitu - Voit valita kentän leveyden, korkeuden ja miinojen lukumäärän itse.")
    while True:
        try:
            print()
            valinta = int(input("- Tee valintasi kirjoittamalla jokin numeroista 1-4: "))
            if valinta <= 0 or valinta > 4:
                print(">>> Valitse jokin numeroista 1-4")
                continue
        except ValueError:
            print(">>> Anna valintasi kokonaislukuna!")
            continue
        else:
            if valinta == 1:
                leveys = 9
                korkeus = 9
                pommit = 10
                return leveys, korkeus, pommit
            elif valinta == 2:
                leveys = 16
                korkeus = 16
                pommit = 40
                return leveys, korkeus, pommit
            elif valinta == 3:
                leveys = 30
                korkeus = 16
                pommit = 99
                return leveys, korkeus, pommit
            elif valinta == 4:
                while True:
                    try:
                        leveys = int(input("- Anna kentän leveys: "))
                        korkeus = int(input("- Anna kentän korkeus: "))
                        if korkeus <= 0 or leveys <= 0:
                            print(">>> Noin pienelle kentälle ei mahdu ainuttakaan pistettä!")
                            continue
                        if korkeus > 40 or leveys > 40:
                            print(">>> Kentän koko voi olla maksimissaan 40x40.")
                            continue
                        pommit = int(input("- Kentällä on ruutuja {}. Montako miinaa haluat kentälle? ".format(leveys*korkeus)))
                        if pommit > leveys*korkeus:
                            print(">>> Kentälle ei voi laittaa ruutuja enempää miinoja. Yritä uudestaan.")
                            continue
                    except ValueError:
                        print(">>> Syötä kentän leveys ja korkeus kokonaislukuina.")
                    else:
                        return leveys, korkeus, pommit


def rakenna_kentta(leveys, korkeus, pommit):
    """
    Rakentaa kentän ja miinoittaa kentän pelaajan toiveen mukaan.
    """
    if not kentta:
            for rivi in range(korkeus):
                kentta.append([])
                for sarake in range(leveys):
                    kentta[-1].append("-")
    jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))
    lista = []
    while len(lista) < pommit:
        lista += [miinoita_kentta(kentta, jaljella)]
    miinat = pommit
    return kentta, jaljella, miinat


def miinoita_kentta(kentta, jaljella):
    """
    Tuottaa miinat kentän rakennukseen.
    """
    (x, y) = random.choice(jaljella)
    kentta[y][x] = "-"
    jaljella.remove((x,y))
    return x, y


def kysy_koordinaatit(kentta):
    """
    Kysyy pelaajalta kentän ruutua vastaavia koordinaatteja. Nämä koordinaatit joko avaavat kentältä ruudun tai merkkaavat mahdollisen miinan paikan pelaajan valinnan mukaan.
    """
    while True:
        lasku = 0
        for rivi in kentta:
            for sarake in rivi:
                if "x" in sarake:
                    lasku += 1
        x_maara = miinat - lasku
        if laske_avaamattomat(kentta) == 0 and x_maara == 0 or laske_avaamattomat(kentta) == x_maara:
            return "v"
        print()
        print("Voit avata ruudun tai merkata ruudun jossa epäilet pommin olevan x:llä")
        print("Merkitse ruutu syöttämällä x tai syötä avattavan ruudun koordinaatit (leveys korkeus) tai lopetta syöttämällä q")
        print("Avataan ruutu:")
        avattava_ruutu = input("- Syötä koordinaatit välilyönnillä erotettuna tai 'x': ").split()
        print("------------------------------------------------")
        if len(avattava_ruutu) == 0:
            print(">>> Syötä koordinaatit kokonaislukuina välilyönnillä erotettuna toisistaan!")
            tulosta_kentta(kentta, miinat)
            continue
        elif avattava_ruutu[0] == "q":
            print("Oletko varma, että haluat lopettaa? Tietoja ei tallenneta.")
            if input("- Syötä 'n', jos haluat lopettaa. Painamalla enteriä pääset takaisin peliin: ") == "n":
                return "q"
            else:
                tulosta_kentta(kentta, miinat)
                continue
        elif len(avattava_ruutu) == 1:
            if avattava_ruutu[0] == "x":
                merkkaa_miina(kentta)
                continue
            else:
                print(">>> Syötä koordinaatit kokonaislukuina välilyönnillä erotettuna toisistaan!")
                tulosta_kentta(kentta, miinat)
                continue
        elif len(avattava_ruutu) != 2:
            print(">>> Syötä kaksi koordinaattia kokonaislukuina välilyönnillä erotettuna toisistaan!")
            tulosta_kentta(kentta, miinat)
            continue
        try:
            leveys = int(avattava_ruutu[0])
            korkeus = int(avattava_ruutu[1])
            if leveys >= len(kentta[0]) or korkeus >= len(kentta) or leveys < 0 or korkeus <0:
                print(">>> Syöttämäsi koordinaatit ovat kentän ulkopuolella. Yritä uudestaan.")
                tulosta_kentta(kentta, miinat)
                continue
        except ValueError:
            print(">>> Anna koordinaatit kokonaislukuina!")
            tulosta_kentta(kentta, miinat)
        else:
            return leveys, korkeus


def merkkaa_miina(kentta):
    """
    Kysyy merkattavan ruudun koordinaatteja ja muuttaa avaamattoman ruudun x-kirjaimeksi.
    """
    while True:
        print("Voit merkata tyhjän paikan x:llä tai poistaa merkkauksen syöttämällä merkatun paikan koordinaatit uudestaan.")
        print("Merkataan ruutu x:llä")
        merkattava_ruutu = input("- Syötä koordinaatit välilyönnillä erotettuna: ").split()
        print("------------------------------------------------")
        if len(merkattava_ruutu) == 0:
            print(">>> Syötä koordinaatit kokonaislukuina välilyönnillä erotettuna toisistaan!")
            tulosta_kentta(kentta, miinat)
            continue
        elif merkattava_ruutu[0] == "q":
            return "q"
        elif len(merkattava_ruutu) != 2:
            print(">>> Syötä kaksi koordinaattia kokonaislukuina välilyönnillä erotettuna toisistaan!")
            tulosta_kentta(kentta, miinat)
            continue
        try:
            miinan_leveys = int(merkattava_ruutu[0])
            miinan_korkeus = int(merkattava_ruutu[1])
            if miinan_leveys >= len(kentta[0]) or miinan_korkeus >= len(kentta) or miinan_leveys < 0 or miinan_korkeus <0:
                print(">>> Syöttämäsi koordinaatit ovat kentän ulkopuolella. Yritä uudestaan.")
                tulosta_kentta(kentta, miinat)
                continue
        except ValueError:
            print(">>> Anna koordinaatit kokonaislukuina!")
            tulosta_kentta(kentta, miinat)
        else:
            if kentta[miinan_korkeus][miinan_leveys] == "-":
                kentta[miinan_korkeus][miinan_leveys] = "x"
                tulosta_kentta(kentta, miinat)
            elif kentta[miinan_korkeus][miinan_leveys] == "x":
                kentta[miinan_korkeus][miinan_leveys] = "-"
                tulosta_kentta(kentta, miinat)
            else:
                print(">>> Et voi merkata avattua ruutua!")
                tulosta_kentta(kentta, miinat)
            return miinan_leveys, miinan_korkeus



def avaa_ruutuja(kentta, x, y):
    """
    Muuttaa avaamattomat ruudut välilyönneiksi ja niitä ympäröivät ruudut numeroruuduiksi.
    """
    lista = [(x, y)]
    while len(lista) > 0:
        x = lista[0][0]
        y = lista[0][1]
        if kentta[y][x] != "-":
            lista.remove(lista[0])
            continue
        elif kentta[y][x] == "-":
            kentta[y][x] = " "

        if y == 0:
            pass
        elif kentta[y - 1][x] == "-":
            if laske_miinat(x, y - 1, kentta, jaljella) > 0:
                kentta[y - 1][x] = ("{}".format(laske_miinat(x, y - 1, kentta, jaljella)))
            else:
                lista.append((x, y - 1))

        if y == (len(kentta) - 1):
            pass
        elif kentta[y + 1][x] == "-":
            if laske_miinat(x, y + 1, kentta, jaljella) > 0:
                kentta[y + 1][x] = ("{}".format(laske_miinat(x, y + 1, kentta, jaljella)))
            else:
                lista.append((x, y + 1))

        if x == 0:
            pass
        elif kentta[y][x - 1] == "-":
            if laske_miinat(x - 1, y, kentta, jaljella) > 0:
                kentta[y][x - 1] = ("{}".format(laske_miinat(x - 1, y, kentta, jaljella)))
            else:
                lista.append((x - 1,y))

        if x == (len(kentta[0]) - 1):
            pass
        elif kentta[y][x + 1] == "-":
            if laske_miinat(x + 1, y, kentta, jaljella) > 0:
                kentta[y][x + 1] = ("{}".format(laske_miinat(x + 1, y, kentta, jaljella)))
            else:
                lista.append((x + 1, y ))

        if x == (len(kentta[0]) - 1) or y == (len(kentta) - 1):
            pass
        elif kentta[y + 1][x + 1] == "-":
            if laske_miinat(x + 1, y + 1, kentta, jaljella) > 0:
                kentta[y + 1][x + 1] = ("{}".format(laske_miinat(x + 1, y + 1, kentta, jaljella)))
            else:
                lista.append((x + 1, y + 1))

        if x == 0 or y == (len(kentta) - 1):
            pass
        elif kentta[y + 1][x - 1] == "-":
            if laske_miinat(x - 1, y + 1, kentta, jaljella) > 0:
                kentta[y + 1][x - 1] = ("{}".format(laske_miinat(x - 1, y + 1, kentta, jaljella)))
            else:
                lista.append((x - 1, y + 1))

        if x == (len(kentta[0]) - 1) or y == 0:
            pass
        elif kentta[y - 1][x + 1] == "-":
            if laske_miinat(x + 1, y - 1, kentta, jaljella) > 0:
                kentta[y - 1][x + 1] = ("{}".format(laske_miinat(x + 1, y - 1, kentta, jaljella)))
            else:
                lista.append((x + 1, y - 1))

        if x == 0 or y == 0:
            pass
        elif kentta[y - 1][x - 1] == "-":
            if laske_miinat(x - 1, y - 1, kentta, jaljella) > 0:
                kentta[y - 1][x - 1] = ("{}".format(laske_miinat(x - 1, y - 1, kentta, jaljella)))
            else:
                lista.append((x - 1, y - 1))
        lista.remove(lista[0])


def laske_miinat(x, y, kentta, jaljella):
    """
    Laskee montako "miinaa" ympäröi kutakin ruutua ja palauttaa määrän ruutuja avaavaan funktioon.
    """
    lista = []
    try:
        if y == 0 or x == 0:
            pass
        elif (x - 1, y - 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if y == 0:
            pass
        elif (x, y - 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if x == len(kentta[0]) - 1 or y == 0:
            pass
        elif (x + 1, y - 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if x == len(kentta[0]) - 1:
            pass
        elif (x + 1, y) not in jaljella:
            lista.append("n")
        else:
            pass
    except IndexError:
        pass
    try:
        if x == 0:
            pass
        elif (x - 1, y) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if x == len(kentta[0]) - 1 or y == len(kentta) - 1:
            pass
        elif (x + 1, y + 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if y == len(kentta) - 1:
            pass
        elif (x, y + 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    try:
        if y == len(kentta) - 1 or x == 0:
            pass
        elif (x - 1, y + 1) not in jaljella:
            lista.append("n")
    except IndexError:
        pass
    return lista.count("n")


def pelaaminen(kentta, koordinaatit,  jaljella):
    """
    Pyörittää itse peliä. Tarkastaa onko ruutu avattu tai merkattu, osuiko pelaaja miinaan, onko avattava ruutu numero vai tyhjä ruutu.
    """
    x = koordinaatit[0]
    y = koordinaatit[1]
    if kentta[y][x] == "x":
        print(">>> Et voi avata merkattua ruutua!")
    elif (x, y) not in jaljella:
        return "h"
    elif kentta[y][x] == " " or kentta[y][x] != "-":
        print(">>> Tämä ruutu on jo avattu!")
    elif laske_miinat(x, y, kentta, jaljella) > 0:
        kentta[y][x] = "{}".format(laske_miinat(x, y, kentta, jaljella))
    else:
        avaa_ruutuja(kentta, x, y)


def laske_avaamattomat(kentta):
    """
    Laskee montako avaamatonta ruutua ("-" merkityt) kentällä on.
    """
    tulos = 0
    for rivi in kentta:
        for sarake in rivi:
            if "-" in sarake:
                tulos += 1
    return tulos


def tulosta_kentta(kentta, miinat):
    """
    Tulostaa kentän, sen ympärille koordinaatit ja jäljellä olevien miinojen lukumäärän.
    """
    print()
    lasku = 0
    for rivi in kentta:
        for sarake in rivi:
            if "x" in sarake:
                lasku += 1
    print("Miinoja jäljellä: {}".format(miinat - lasku))
    print()
    for a, pala in (enumerate(kentta[0], start = 0)):
        if a == 0:
            print("   ", str(a), end="  ")
        elif a < 10:
            print(str(a), end="  ")
        else:
            print(str(a), end=" ")
    print()
    for i, osa in enumerate(kentta):
        if i < 10:
            print(" " + str(i) + " " + " "+ "  ".join(osa) + "  " + str(i))
        else:
            print("" + str(i) + "  " + "  ".join(osa) + "  " + str(i))
    for a, pala in (enumerate(kentta[0], start = 0)):
        if a == 0:
            print("   ", str(a), end="  ")
        elif a < 10:
            print(str(a), end="  ")
        else:
            print(str(a), end=" ")
    print()
    return str(miinat - lasku)


def tilastot(alku, loppu):
    """
    Laskee peliin kuluneen ajan ja kierrokset sekä ottaa ylös päivämäärän ja kellonajan pelin päättyessä.
    """
    kulunut = loppu - alku
    if kulunut >  60:
        min = int(kulunut/60)
        s = int(kulunut)%60
        ajankohta = time.strftime("%A, %d.%m.%Y %H:%M:%S", time.localtime())
        vuorot = "Vuoroja kului {}".format(kierrokset.count("t"))
        aika = "Aikaa kului {} minuuttia {} sekuntia".format(min, s)
        return ajankohta, vuorot, aika
    else:
        ajankohta = time.strftime("%A, %d.%m.%Y %H:%M:%S", time.localtime())
        vuorot = "Vuoroja kului {}".format(kierrokset.count("t"))
        aika = "Aikaa kului {:.0f} sekuntia".format(kulunut)
        return ajankohta, vuorot, aika


def tallenna_tulokset(ajankohta, vuorot, aika, tulos):
    """
    Tallentaa pelin tiedot(päivämäärä, kellonaika, kesto vuoroissa ja ajassa ja pelin lopputuloksen(voitto/häviö, kentän koko, miinojen lukumäärä).
    """
    with open("tulokset.txt", "a") as kohde:
        kohde.write("{} | {} | {} | {}\n".format(ajankohta, tulos, aika, vuorot))


if __name__ == "__main__":
    while True:
        if alkuvalikko() == "q":
            break
        kentta = []
        kierrokset = []
        leveys, korkeus, pommit = kysy_koko()
        jaljella = rakenna_kentta(leveys, korkeus, pommit)[1]
        miinat = rakenna_kentta(leveys, korkeus, pommit)[2]
        tulosta_kentta(kentta, miinat)
        alku = time.time()
        while True:
            koordinaatit = kysy_koordinaatit(kentta)
            kierrokset.append("t")
            if koordinaatit == "v":
                loppu = time.time()
                print()
                print(">>> Onneksi olkoon! Voitit pelin!")
                ajankohta, vuorot, aika = tilastot(alku, loppu)
                tulos = ("Tulos: voitto, kentän koko {}x{}, miinoja: {}".format(len(kentta[0]), len(kentta), miinat))
                tallenna_tulokset(ajankohta, vuorot, aika, tulos)
                print()
                print(ajankohta)
                print(vuorot)
                print(aika)
                print(tulos)
                break
            if koordinaatit == "q":
                loppu = time.time()
                print()
                print("Lopetit pelin. Tietoja ei tallennettu.")
                break
            else:
                if pelaaminen(kentta, koordinaatit, jaljella) == "h":
                    print()
                    print(">>> Osuit pommiin, hävisit pelin :(")
                    loppu = time.time()
                    ajankohta, vuorot, aika = tilastot(alku, loppu)
                    tulos = ("Tulos: häviö, kentän koko {}x{}, miinoja: {}".format(len(kentta[0]), len(kentta), miinat))
                    tallenna_tulokset(ajankohta, vuorot, aika, tulos)
                    print()
                    print(ajankohta)
                    print(vuorot)
                    print(aika)
                    print(tulos)
                    break
                tulosta_kentta(kentta, miinat)