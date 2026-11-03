import datetime
import os

import requests
import csv

# Constants
income_tax = 24

# Lihtsustamis funktsioon timestampi konvertimiseks kuupäevaks
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

# Funktsioon, et konverti MWh > s/kWh ja arvutada juurde käibemaks
def calculate_price(price):
    return round((price / 1000) * (income_tax/100 + 1) * 100, 3)


#API päringute jaoks kuupäevad, et oleks alati õige päev
current_date = datetime.datetime.now()
start_date = current_date.date() - datetime.timedelta(days=1)
end_date = current_date.date()
current_time = current_date.time().strftime("%H:%M")


#API päringute URLi variables
url_current_energy_price = "https://dashboard.elering.ee/api/nps/price/ee/current"
url_whole_day_energy_price = f"https://dashboard.elering.ee/api/nps/price?start={start_date}T22:00:00Z&end={end_date}T21:59:59Z"
print(url_whole_day_energy_price)

#Küsime eleringi API käest praeguse ajahetke elektri börsihinna
current_energy_price_info = requests.get(url_current_energy_price).json()

#Küsime eleringi API käest ühe päeva elektri börsihinnad
whole_day_energy_price_info = requests.get(url_whole_day_energy_price).json()
day_prices = whole_day_energy_price_info['data']["ee"]

#Võtame eleringi API JSON vastusest hinna ja aja väärtuse
current_energy_price = calculate_price(current_energy_price_info['data'][0]["price"])
current_price_time = current_energy_price_info['data'][0]["timestamp"]
max_day_energy_price_in_MWh = day_prices[0]["price"]
min_day_energy_price_in_MWh = day_prices[0]["price"]
max_price_time = day_prices[0]["timestamp"]
min_price_time = day_prices[0]["timestamp"]

#Tsükkel, et käia läbi whole_day_energy_price_info oleva hinna parameetrid ja leida kõige kõrgem elektri hind päevas
for timeslot in day_prices:
    energy_price = timeslot["price"]
    if energy_price > max_day_energy_price_in_MWh:
        max_day_energy_price_in_MWh = energy_price
        max_price_time = timeslot["timestamp"]
    if energy_price < min_day_energy_price_in_MWh:
        min_day_energy_price_in_MWh = energy_price
        min_price_time = timeslot["timestamp"]

max_day_energy_price_in_kWh = calculate_price(max_day_energy_price_in_MWh)
min_day_energy_price_in_kWh = calculate_price(min_day_energy_price_in_MWh)

#print(current_energy_price_info)
#print(whole_day_energy_price_info)
print("Praegune kellaaeg", current_time)
print("Praegune elektri hind:", current_energy_price, "s/kWh kell", convert_timestamp(current_price_time))
print("Päeva kõrgeim elektri hind:", max_day_energy_price_in_kWh, "s/kWh kell" ,convert_timestamp(max_price_time))
print("Päeva madalaim elektri hind:", min_day_energy_price_in_kWh, "s/kWh kell", convert_timestamp(min_price_time))


# AI abi sai kasutatud, et aru saada kuidas peaks day_prices json infot for loopiga läbima. Et saaks kindel tundide vahemik kätte
# Loop, läbimiseks päeva hinnad ja iga 15 min tagant tagastada 2 tunni keskmise hinde

def calculate_lowest_period_cost(hours):
    period = hours * 4
    lowest_energy_price_range = 99999
    lowest_energy_price_time = convert_timestamp(day_prices[0]["timestamp"])

    for i in range(len(day_prices) - period + 1):
        energy_price_sum = 0
        for n in range(i, i + period):
            energy_price_sum += calculate_price(day_prices[n]["price"])
        energy_price_time = convert_timestamp(day_prices[i]["timestamp"])
        period_average_price = round(energy_price_sum / period, 3)
        if period_average_price < lowest_energy_price_range:
            lowest_energy_price_range = period_average_price
            lowest_energy_price_time = energy_price_time.time().strftime("%H:%M")
        return lowest_energy_price_range, lowest_energy_price_time


period_average_price, energy_price_time = calculate_lowest_period_cost(2)
print('Odavaim periood:',period_average_price, energy_price_time)

def save_day_prices(prices, filename):
    file_exists = os.path.exists("./data/energy.csv")
    if not file_exists:
        with open("./data/energy_price.csv", "a", newline='') as datafile:
            datawriter = csv.writer(datafile)
            datawriter.writerow(["timestamp", "time", "price", "income_tax"])

        with open("./data/energy.csv", "r") as datafile:
            reader = csv.reader(datafile)
            for row in reader:
                if row[0] != day_prices[0]["timestamp"]:
                    write_to_file = True
        if write_to_file:
            with open("./data/energy.csv", "a", newline='') as datafile:
                datawriter = csv.writer(datafile)
                datawriter.writerow(
                    [int(day_prices[i]["timestamp"]),
                     energy_price_time,
                     float(period_average_price),
                     int(income_tax)])

def write_price_data_to_file(hours = 2):
    write_to_file = False
    period = hours * 4
    lowest_energy_price_range = 99999
    lowest_energy_price_time = convert_timestamp(day_prices[0]["timestamp"])

    for i in range(len(day_prices) - period + 1):
        energy_price_sum = 0
        for n in range(i, i + period):
            energy_price_sum += calculate_price(day_prices[n]["price"])
        energy_price_time = convert_timestamp(day_prices[i]["timestamp"])
        period_average_price = round(energy_price_sum / period, 3)
        if period_average_price < lowest_energy_price_range:
            lowest_energy_price_range = period_average_price
            lowest_energy_price_time = energy_price_time.time().strftime("%H:%M")
        file_exists = os.path.exists("./data/energy.csv")
        with open("./data/energy.csv", "a") as datafile:
            if not file_exists:
                with open("./data/energy.csv", "a", newline='') as datafile:
                    datawriter = csv.writer(datafile)
                    datawriter.writerow(["timestamp", "time", "price", "income_tax"])
            with open("./data/energy.csv", "r") as datafile:
                reader = csv.reader(datafile)
                for row in reader:
                    if row[0] != day_prices[0]["timestamp"]:
                        write_to_file = True
            if write_to_file:
                with open("./data/energy.csv", "a", newline='') as datafile:
                    datawriter = csv.writer(datafile)
                    datawriter.writerow(
                        [int(day_prices[i]["timestamp"]),
                         energy_price_time,
                         float(period_average_price),
                         int(income_tax)])

write_price_data_to_file(2)

# ---------------------------------------------------------------------
# ÜLESANNE B: AJALOO SALVESTAMINE
# Salvesta iga päeva hinnad faili ja võrdle päevi omavahel.
# - Vali formaat: CSV (tabel, avaneb Excelis) või JSON (sarnane
#   API vastusega). Pythonis on mõlema jaoks moodul: csv / json
# - Loe eilne fail sisse, arvuta mõlema päeva keskmine ja prindi:
#   "Täna on elekter 12% kallim kui eile"
# - Nädala keskmine:
# - Mõtlemiseks: Eleringi API annab ka mineviku hindu -
#   miks võiks ikkagi olla mõistlik andmeid ise salvestada?
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# ÜLESANNE C: GRAAFIK (matplotlib)
# Joonista päeva hindadest graafik.
# - Paigalda: pip install matplotlib
# - Koosta tsükliga kaks listi: kellaajad (x) ja hinnad s/kWh (y)
# - plt.plot() või plt.step() - kumb sobib paremini, kui hind
#   kehtib terve 15 minuti jooksul muutumatult?
# - Lisa telgede nimed ja pealkiri koos kuupäevaga
# - Märgi praegune hetk püstjoonega (plt.axvline())
#   ja päeva max/min punktid
# - Boonus: tulpdiagramm (plt.bar()), kus odavad perioodid on
#   rohelised ja kallid punased
# - Salvesta pildina: plt.savefig()
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE D: EKRAAN JA LED (Raspberry Pi)
# Füüsiline seade, mis näitab hinda pidevalt.
# - Vaja: Raspberry Pi, LED-id + takistid, hiljem väike ekraan
#   (nt I2C OLED SSD1306)
# - Alusta ühest LED-ist: teek gpiozero, LED(17).on() / .off()
# - Tingimus: hind alla piiri -> roheline LED, muidu punane
#   Boonus: kolm LED-i odav / keskmine / kallis (vt Urmo ülesanne 2)
# - Programm peab töötama pidevalt: while True + time.sleep()
#   Kui tihti on mõtet hinda uuesti küsida?
# - Ekraan: kuva praegune hind, kellaaeg ja päeva max
# - NB! Siin muutub vigade käsitlemine päriselt oluliseks:
#   kui WiFi korraks kaob, ei tohi seade "surra" (try / except)
# ---------------------------------------------------------------------


# =====================================================================
# URMO ÜLESANDED
# (Ülesannete kirjeldused koostatud AI abiga, kood kirjutatud iseseisvalt)
# Kasuta andmeid: day_prices (list, igas elemendis "timestamp" ja "price")
#                 current_energy_price (praegune hind, s/kWh koos käibemaksuga)
# =====================================================================

# ---------------------------------------------------------------------
# ÜLESANNE 1: PÄEVA KESKMINE HIND  (~8 rida)
# Tee funktsioon, mis saab sisse hindade listi ja tagastab keskmise.
# - Loo muutuja summa jaoks, alguses 0
# - Käi for-tsükliga list läbi ja liida iga "price" summale
# - Keskmine = summa / mitu elementi listis on (vihje: len())
# - Prindi tulemus välja
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE 2: ODAV VÕI KALLIS?  (~10 rida)
# Tee funktsioon, mis saab sisse praeguse hinna ja päeva keskmise
# ning tagastab sõna "odav", "keskmine" või "kallis".
# - Kasuta if / elif / else
# - Nt: alla 80% keskmisest = odav, üle 120% = kallis, muidu keskmine
# - Prindi: "Praegu on elekter: odav"
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE 3: MITU ODAVAT PERIOODI  (~8 rida)
# Loe kokku, mitu 15-min perioodi päevas on hinnaga alla X.
# - Küsi X kasutajalt: input() ja teisenda numbriks (float())
# - Loendur alguses 0, tsüklis +1 kui hind on piirist väiksem
# - Prindi: "Täna on 23 perioodi hinnaga alla 50 €/MWh"
# - Boonus: mitu tundi see kokku teeb? (1 periood = 15 min)
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE 4: PÄEVA HINNATABEL  (~8 rida)
# Prindi välja kõik päeva hinnad loetaval kujul:
#   00:00   4.12 s/kWh
#   00:15   3.98 s/kWh
#   ...
# - for-tsükkel üle day_prices
# - Kellaaeg timestampist (kasuta Alo funktsiooni)
# - Ainult tund ja minut: .strftime("%H:%M")
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE 5: TEKSTILINE TULPDIAGRAMM  (~10 rida)
# Sama tabel, aga iga hinna kõrval on tulp sümbolitest:
#   07:45  41.0 s/kWh  ########################################
#   23:15   2.0 s/kWh  ##
# - Pythonis saab teksti korrutada: "#" * 5 annab "#####"
# - Tulba pikkus = hind sentides, ümardatud täisarvuks (int())
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# ÜLESANNE 6: SEADME KULU KALKULAATOR  (~15 rida)
# Kasutaja sisestab seadme võimsuse ja kasutusaja, programm
# arvutab, palju see praeguse hinnaga maksab.
# - Küsi: võimsus kW-des (nt saun 9 kW) ja aeg tundides
# - Energia (kWh) = võimsus * aeg
# - Hind eurodes = energia * hind €/kWh
# - Prindi: "Saun 1h maksab praegu 0.93 €"
# - Boonus: arvuta ka, palju see maksaks päeva odavaimal ajal
# ---------------------------------------------------------------------