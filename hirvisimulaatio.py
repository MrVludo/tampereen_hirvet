""" import """
import os
from math import sqrt
import random
import time
import numpy as np

VIS: bool = True # visualisointi

LENTONOPEUS: float = 15.0 # m/s
LENTOAIKA: float = 3600.0 # s
SKANNAUSLEVEYS: float = 300.0

ALUE_WIDTH: float = 1000.0 # metriä
ALUE_HEIGHT: float = 600.0 # metriä

SPEED_MIN: float = 2.5 # m/s
SPEED_MAX: float = 3.0 # m/s

HIRVIMAARA: int = 40 # Hirviä

REVIIRI: float = 300.0 # metriä

TESTIMAARA: int = 100 # Testiä

hirvet = [] # Hirvilista

# input tulee olemaan:
# lentonopeus, skannausleveys,
# hirvimäärä, aluepituus
# hirvikeskinopeus, reviiri
class Drooni:
    """ DDRROOOOONIII    Viiiuuuuuu """
    # Olkoot:
    # lentonopeus 10 m/s
    # lentoaika 60 min
    # korkeus 250 metriä, kulma 60 astetta (30+30)
    # ja täten tarkasteluleveys 300 metriä
    # skannauksen pituus on sama kuin dronen nopeus, kun skannaus tapahtuu joka sekunti

    def __init__(self, kohteet):

        # Droonin koordhinaatit:
        # print("uusi drooni:", self)
        self.x: float = kohteet[0][0]
        self.y: float = kohteet[0][1]

        self.suunta: bool = 1 # 0 on x-suunta ja 1 on y-suunta

        self.kohteet = kohteet
        self.kohteet.reverse()
        self.ero_x, self.ero_y = 0, 0

        # Tarkastelualueen pituus ja leveys:
        self.pituus: float = LENTONOPEUS # metriä
        self.leveys: float = SKANNAUSLEVEYS # metriä

        self.lentoaika: float = LENTOAIKA # minuuttia
        self.nopeus: float = LENTONOPEUS # m/s


    def fly(self, dt):
        """ Drooni lentä dt ajan """

        if len(self.kohteet) < 1:
            return

        kohde_x, kohde_y = self.kohteet[-1]

        ero_x = kohde_x - self.x
        ero_y = kohde_y - self.y

        self.ero_x, self.ero_y = ero_x, ero_y

        vx = self.nopeus * ero_x/sqrt(ero_x**2+ero_y**2)
        vy = self.nopeus * ero_y/sqrt(ero_x**2+ero_y**2)

        dx = vx * dt
        dy = vy * dt

        self.x += dx
        self.y += dy


    def scan(self):
        """ Drooni skannaa hirviä """

        skannatut_hirvet = []

        # Droonialue
        if self.suunta:
            drooni_left: float = (self.x - self.leveys/2, self.y - self.pituus/2)
            drooni_right: float = (self.x + self.leveys/2, self.y + self.pituus/2)
        else:
            drooni_left: float = (self.x - self.pituus/2, self.y - self.leveys/2)
            drooni_right: float = (self.x + self.pituus/2, self.y + self.leveys/2)

        for hirvi in hirvet:
            # Katsotaan, onko hirvi droonin alueella

            if drooni_left[0] <= hirvi.x <= drooni_right[0]:
                if drooni_left[1] <= hirvi.y <= drooni_right[1]:
                    skannatut_hirvet.append((hirvi.x, hirvi.y))
                    hirvi.nahty += 1

        return skannatut_hirvet

    def on_kohteessa(self):
        """ Tarkistaa, onko hirvi päässyt kohteeseen """

        if len(self.kohteet) < 1:
            return True

        kohde_x, kohde_y = self.kohteet[-1]

        if self.x == kohde_x and self.y == kohde_y:
            return True

        if self.ero_x == 0 and self.ero_y == 0:
            return True

        ero_x = kohde_x - self.x
        ero_y = kohde_y - self.y

        if  ero_x * self.ero_x < 0 or ero_y * self.ero_y < 0:
            return True

        return False

class Vasa:
    """ Vasa """

    def __init__(self, emo_x, emo_y):
        # Vasa spawnaa jonnekin emonsa ympärille 2 metrin etäisyydelle

        delta_x = random.choice([0,2,-2])
        if delta_x == 0:
            delta_y = random.choice([2, -2])
        else:
            delta_y = random.choice([0, 2, -2])

        self.x = emo_x + delta_x
        self.y = emo_y + delta_y


class Hirvi:
    """ Hirvi """

    def __init__(self):
        self.spawnpoint = (random.randint(0, ALUE_WIDTH), random.randint(0, ALUE_HEIGHT))

        self.x, self.y = self.spawnpoint
        self.kohde_x, self.kohde_y = self.spawnpoint
        self.ero_x, self.ero_y = 0, 0

        self.nopeus = float(random.randint(int(SPEED_MIN*10), int(SPEED_MAX*10)))/10
        self.radius = REVIIRI

        self.eating: bool = False
        self.food: float = 0.0

        self.nahty: int = 0

        """ Hirvi on vasan emo todennäköisyydellä 25 % """
        if random.randint(1,4) == 1:
            # Hirvi on emo
            self.on_emo: bool = True
            self.vasa = Vasa(self.x, self.y)

            self.nopeus *= 0.75 # nopeus hidastuu 25 %
        else:
            # Hirvi ei ole emo
            self.on_emo: bool = False


    def uusikohde(self):
        """ Uusi liikkumiskohde """
        while True:
            normal_x = np.random.normal()*0.5
            normal_y = np.random.normal()*0.5

            if -2 < normal_x < 2 and -2 < normal_y < 2:
                break

        self.kohde_x = self.spawnpoint[0] + self.radius * normal_x
        self.kohde_y = self.spawnpoint[1] + self.radius * normal_y


    def liikkuu(self, dt):
        """ Hirvi liikkuu ajan dt(sekunneissa) """
        ero_x = self.kohde_x - self.x
        ero_y = self.kohde_y - self.y

        self.ero_x, self.ero_y = ero_x, ero_y
        if ero_x == ero_y == 0:
            return

        vx = self.nopeus * ero_x/sqrt(ero_x**2+ero_y**2)
        vy = self.nopeus * ero_y/sqrt(ero_x**2+ero_y**2)

        dx = vx * dt
        dy = vy * dt

        self.x += dx
        self.y += dy
        if self.on_emo:
            self.vasa.x += dx
            self.vasa.y += dy


    def on_kohteessa(self):
        """ Tarkistaa, onko hirvi päässyt kohteeseen """

        if self.x == self.kohde_x and self.y == self.kohde_y:
            return True

        if self.ero_x == 0 and self.ero_y == 0:
            return True

        ero_x = self.kohde_x - self.x
        ero_y = self.kohde_y - self.y

        if  ero_x * self.ero_x < 0 or ero_y * self.ero_y < 0:
            return True

        return False


    def starts_eating(self):
        """ Hirvi aloittaa syömisen """
        self.eating = True
        self.food = random.randint(5, 102)


    def eats(self, dt):
        """ Hirvi syö dt sekunnin aikana dt määrän ruokaa """
        self.food -= dt
        if self.food <= 0:
            self.food = 0
            self.eating = False

MAASTO_HEIGHT = 50
MAASTO_WIDTH = 100

maasto = [["." for j in range(MAASTO_WIDTH)] for i in range(MAASTO_HEIGHT)]


def maasto_print():
    """ Printtaa maaston """
    for i in range(MAASTO_HEIGHT):
        rivi = ""
        for j in range(MAASTO_WIDTH):
            rivi += maasto[i][j] + " "
        print(rivi)
    print("\n")


def maasto_hirvi(uusi_hirvi):
    """ Tallentaa tiedon hirveistä maastotaulukkoon """

    cl1: str = ""
    cl2: str = ""

    if uusi_hirvi.nahty == 1:
        # Vihreä (cl = colour line)
        cl1 = '\033[42m'
        cl2 ='\033[0m'

    if uusi_hirvi.nahty == 2:
        # Keltainen
        cl1 = '\033[43m'
        cl2 ='\033[0m'
    if uusi_hirvi.nahty >= 3:
        # Punainen
        cl1 = '\033[41m'
        cl2 ='\033[0m'

    hirvi_maasto_y = int(uusi_hirvi.y*MAASTO_HEIGHT/ALUE_HEIGHT)
    hirvi_maasto_x = int(uusi_hirvi.x*MAASTO_WIDTH/ALUE_WIDTH)

    if hirvi_maasto_y < 0 or hirvi_maasto_y >= MAASTO_HEIGHT:
        return
    if hirvi_maasto_x < 0 or hirvi_maasto_x >= MAASTO_WIDTH:
        return

    if "@" in maasto[hirvi_maasto_y][hirvi_maasto_x]:
        maasto[hirvi_maasto_y][hirvi_maasto_x] = cl1+"#"+cl2
    else:
        maasto[hirvi_maasto_y][hirvi_maasto_x] = cl1+"@"+cl2


    kohde_maasto_y = int(uusi_hirvi.kohde_y*MAASTO_HEIGHT/ALUE_HEIGHT)
    kohde_maasto_x = int(uusi_hirvi.kohde_x*MAASTO_WIDTH/ALUE_WIDTH)

    if False and not (kohde_maasto_y < 0 or kohde_maasto_y >= MAASTO_HEIGHT):
        if not (kohde_maasto_x < 0 or kohde_maasto_x >= MAASTO_WIDTH):
            maasto[kohde_maasto_y][kohde_maasto_x] = "K"


    if uusi_hirvi.on_emo:
        vasa_maasto_y = int(uusi_hirvi.y*MAASTO_HEIGHT/ALUE_HEIGHT)
        vasa_maasto_x = int(uusi_hirvi.x*MAASTO_WIDTH/ALUE_WIDTH)

        if vasa_maasto_y < 0 or vasa_maasto_y >= MAASTO_HEIGHT:
            return
        if vasa_maasto_x < 0 or vasa_maasto_x >= MAASTO_WIDTH:
            return

        if "@" in maasto[vasa_maasto_y][vasa_maasto_x]:
            maasto[vasa_maasto_y][vasa_maasto_x] = "#"
        else:
            maasto[vasa_maasto_y][vasa_maasto_x] = "@"


def main(droonikohteet):
    """ main """

    # Lisätään hirvet listaan
    for _ in range(HIRVIMAARA):
        uusi_hirvi = Hirvi()
        hirvet.append(uusi_hirvi)

    drooni = Drooni(kohteet = droonikohteet) # Uusi drooni (default)

    hirvi_counter = 0

    for _ in range(1000000000):

        if VIS:
            for i in range(MAASTO_HEIGHT):
                for j in range(MAASTO_WIDTH):
                    maasto[i][j] = " "

        for hirvi in hirvet:
            if hirvi.eating:
                hirvi.eats(1) # syö 1 sekunnin ajan
                if VIS:
                    maasto_hirvi(hirvi)
                continue
            if hirvi.on_kohteessa():
                if random.randint(1,4) == 1: # todennäköisyys 25 % hirvi löysi ruoan
                    hirvi.starts_eating()
                else:
                    hirvi.uusikohde()

            hirvi.liikkuu(1)
            maasto_hirvi(hirvi)

        if VIS:
            drooni_maasto_y = int(drooni.y*MAASTO_HEIGHT/ALUE_HEIGHT)
            drooni_maasto_x = int(drooni.x*MAASTO_WIDTH/ALUE_WIDTH)
            if 0 <= drooni_maasto_y < MAASTO_HEIGHT and 0 <= drooni_maasto_x < MAASTO_WIDTH:
                maasto[drooni_maasto_y][drooni_maasto_x] = '\033[44mG\033[0m'

            os.system('cls' if os.name == 'nt' else 'clear')
            maasto_print()
            print("Hirvien skannattu määrä:", hirvi_counter, "/", HIRVIMAARA)

        skannatut_hirvet = drooni.scan()
        hirvi_counter += len(skannatut_hirvet)

        if len(drooni.kohteet) < 1:
            return hirvi_counter
        if drooni.on_kohteessa():
            if len(drooni.kohteet) > 1:
                drooni.kohteet.pop()
                drooni.suunta ^= 1
            else:
                return hirvi_counter

        drooni.fly(1)

        if VIS:
            time.sleep(0.01)
    return hirvi_counter


def clear_randomdata():
    """ Clearing """
    hirvet.clear()


def start_vis_query():
    """ Kysyy alussa asioita """

    true_vastaukset = ["","j","joo","jaa","jo","ja","kyllä","kyl","yes","y","true","oui","jep"]
    false_vastaukset = ["e","ei","nej","nein","no","n","false","en",""]

    kys = "kys" # KYSymys

    while True:
        if kys in true_vastaukset:
            # Käyttäjä haluaa visualisoinnin
            return True
        if kys in false_vastaukset:
            # Käyttäjä ei halua visualisointia
            return False
        kys = input("Haluatko visualisoinnin?: ").lower().strip()


if __name__ == "__main__":
    # input tulee olemaan:
    # lentonopeus, skannausleveys,
    # hirvimäärä, aluepituus,
    # hirvikeskinopeus, reviiri

    VIS = start_vis_query() # kysyy visualisoinnista
    time_alku = time.time()

    with open("testit.txt", "r", encoding='utf-8') as input_file:
        LINE_COUNTER = 1
        for line in input_file:
            print("Line:", LINE_COUNTER)
            LINE_COUNTER += 1

            test_data = line.split() # lista

            LENTONOPEUS = float(test_data[0])
            SKANNAUSLEVEYS = float(test_data[1])
            HIRVITIHEYS = float(test_data[2])
            ALUE_WIDTH = float(test_data[3])
            SPEED_MIN = float(test_data[4])-0.25
            SPEED_MAX = float(test_data[4])+0.25
            REVIIRI = float(test_data[5])

            HIRVIMAARA = int(HIRVITIHEYS * ALUE_WIDTH * ALUE_HEIGHT / 1e7)

            testitulokset = []

            LENTOMAARA = 5

            for testi_n in range(TESTIMAARA):
                TESTITULOS = 0
                for lento_n in range(LENTOMAARA):
                    DROONIKOHTEET = [(0,ALUE_HEIGHT/4), (ALUE_WIDTH, ALUE_HEIGHT/4),
                                    (ALUE_WIDTH, ALUE_HEIGHT/4*3), (0, ALUE_HEIGHT/4*3)]
                    TESTITULOS += main(DROONIKOHTEET)
                    clear_randomdata()
                testitulokset.append(TESTITULOS)

            hirvi_keskiarvo = sum(testitulokset)/len(testitulokset)
            hirvi_keskihajonta = np.std(testitulokset)
            with open("output.txt", "a", encoding='utf-8') as output_file:

                output_file.write(str(TESTIMAARA)+' '+str(HIRVIMAARA*LENTOMAARA)
                                  +' '+str(hirvi_keskiarvo)+' '+str(hirvi_keskihajonta)+'\n')


    time_loppu = time.time()
    print("Aikaa kesti:", time_loppu - time_alku, "s")
