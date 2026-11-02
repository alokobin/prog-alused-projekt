import datetime
import requests

# Lihtsustamis funktsioon timestampi konvertimiseks kuupäevaks
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

# Funktsioon, et konverti MWh > s/kWh ja arvutada juurde käibemaks
def calculate_price(price):
    return round((price / 1000) * 1.24 * 100, 3)


#API päringute jaoks kuupäevad, et oleks alati õige päev
current_date = datetime.datetime.now()
start_date = current_date.date() - datetime.timedelta(days=1)
end_date = current_date.date()
current_time = current_date.time()

#API päringute URLi variables
url_current_energy_price = "https://dashboard.elering.ee/api/nps/price/ee/current"
url_whole_day_energy_price = f"https://dashboard.elering.ee/api/nps/price?start={start_date}T22:00:00Z&end={end_date}T21:59:59Z"

#Küsime eleringi API käest praeguse ajahetke elektri börsihinna
current_energy_price_info = requests.get(url_current_energy_price).json()

#Küsime eleringi API käest ühe päeva elektri börsihinnad
whole_day_energy_price_info = requests.get(url_whole_day_energy_price).json()
day_prices = whole_day_energy_price_info['data']["ee"]

#Võtame eleringi API JSON vastusest hinna väärtuse
current_energy_price = calculate_price(current_energy_price_info['data'][0]["price"])
current_price_time = convert_timestamp(current_energy_price_info['data'][0]["timestamp"])
max_day_energy_price_in_MWh = day_prices[0]["price"]
min_day_energy_price_in_MWh = day_prices[0]["price"]
max_price_time = convert_timestamp(day_prices[0]["timestamp"])
min_price_time = convert_timestamp(day_prices[0]["timestamp"])

#Tsükkel, et käia läbi whole_day_energy_price_info oleva hinna parameetrid ja leida kõige kõrgem elektri hind päevas
for timeslot in day_prices:
    energy_price = timeslot["price"]
    if energy_price > max_day_energy_price_in_MWh:
        max_day_energy_price_in_MWh = energy_price
        max_price_time = convert_timestamp(timeslot["timestamp"])
    if energy_price < min_day_energy_price_in_MWh:
        min_day_energy_price_in_MWh = energy_price
        min_price_time = convert_timestamp(timeslot["timestamp"])

max_day_energy_price_in_kWh = calculate_price(max_day_energy_price_in_MWh)
min_day_energy_price_in_kWh = calculate_price(min_day_energy_price_in_MWh)

#print(current_energy_price_info)
#print(whole_day_energy_price_info)
print("Praegune kellaaeg", current_time)
print("Praegune elektri hind:", current_energy_price, "s/kWh kell", current_price_time)
print("Päeva kõrgeim elektri hind:", max_day_energy_price_in_kWh, "s/kWh kell" , max_price_time)
print("Päeva madalaim elektri hind:", min_day_energy_price_in_kWh, "s/kWh kell", min_price_time)



# =====================================================================
# URMO ÜLESANDED
# (Ülesannete kirjeldused koostatud AI abiga, kood kirjutatud iseseisvalt)
# Kasuta andmeid: day_prices (list, igas elemendis "timestamp" ja "price")
#                 current_energy_price_in_MWh (praegune hind)
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