import datetime
import os
import requests
import csv
import price_charts

# Constants
VAT_PERCENT = 24
CURRENT_ENERGY_PRICE_URL = "https://dashboard.elering.ee/api/nps/price/ee/current"
DAY_ENERGY_PRICE_URL = "https://dashboard.elering.ee/api/nps/price"
PRICE_DATA_FILE = "./data/energy.csv"
PRICES_PER_HOUR = 4
CHART_FILE = "hinnagraafik.png"

# Aeg
current_date = datetime.datetime.now()

# Lihtsustamis funktsioon timestampi konvertimiseks kuupäevaks
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

# Funktsioon, et konverti MWh > s/kWh ja arvutada juurde käibemaks
def calculate_price(price):
    return round((price / 1000) * (VAT_PERCENT / 100 + 1) * 100, 3)

# Funktsioon päeva max hinna/aja leidmiseks
def get_day_max_price_and_time():
    max_day_energy_price_in_mwh = day_prices[0]["price"]
    max_price_time = day_prices[0]["timestamp"]

    for timeslot in day_prices:
        energy_price = timeslot["price"]
        if energy_price > max_day_energy_price_in_mwh:
            max_day_energy_price_in_mwh = energy_price
            max_price_time = timeslot["timestamp"]

    return calculate_price(max_day_energy_price_in_mwh), convert_timestamp(max_price_time)

# Funktsioon päeva min hinna/aja leidmiseks
def get_day_min_price_and_time():
    min_day_energy_price_in_mwh = day_prices[0]["price"]
    min_price_time = day_prices[0]["timestamp"]

    for timeslot in day_prices:
        energy_price = timeslot["price"]
        if energy_price < min_day_energy_price_in_mwh:
            min_day_energy_price_in_mwh = energy_price
            min_price_time = timeslot["timestamp"]

    return calculate_price(min_day_energy_price_in_mwh), convert_timestamp(min_price_time)

# Loop, läbimiseks päeva hinnad ja iga 15 min tagant tagastada 2 tunni keskmise hinde
def calculate_lowest_period_cost(hours):
    period = hours * PRICES_PER_HOUR
    lowest_energy_price_range = 99999
    lowest_energy_price_time = convert_timestamp(day_prices[0]["timestamp"])

    # AI aitas kuidas seda for loopi tuleks alustada
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

# AI aitas millisel kujul oleks if loogika mõistlikum.
# Salvesta päeva hinna info faili hilisemaks kasutamiseks
def save_day_prices(prices, filename):
    file_exists = os.path.exists(filename)
    already_saved = False

    if file_exists:
        with open(filename, "r") as datafile:
            reader = csv.reader(datafile)
            next(reader)
            for row in reader:
                if int(row[0]) == prices[0]["timestamp"]:
                    already_saved = True

    if not file_exists:
        with open(filename, "a", newline='') as datafile:
            datawriter = csv.writer(datafile)
            datawriter.writerow(["timestamp", "time", "price", "vat_percent"])

    if not already_saved:
        with open(filename, "a", newline='') as datafile:
            datawriter = csv.writer(datafile)
            for row in range(len(prices)):
                timestamp = int(prices[row]["timestamp"])
                datawriter.writerow([
                    timestamp,
                    convert_timestamp(prices[row]["timestamp"]),
                    prices[row]["price"],
                    int(VAT_PERCENT)])

def get_current_energy_price():
    current_energy_price_info = requests.get(CURRENT_ENERGY_PRICE_URL).json()
    current_energy_price = current_energy_price_info['data'][0]["price"]
    current_price_time = current_energy_price_info['data'][0]["timestamp"]

    return calculate_price(current_energy_price), convert_timestamp(current_price_time)

def get_whole_day_price_info_estonia_dictionary():
    #Kuupäev URLi jaoks, et iga päev saaks õige kuupäeva
    start_date = current_date.date() - datetime.timedelta(days=1)
    end_date = current_date.date()

    url_whole_day_energy_price = f"{DAY_ENERGY_PRICE_URL}?start={start_date}T22:00:00Z&end={end_date}T21:59:59Z"
    whole_day_energy_price_info = requests.get(url_whole_day_energy_price).json()
    day_prices = whole_day_energy_price_info['data']["ee"]

    return day_prices

def get_current_time():
    current_time_unformated = datetime.datetime.now()
    current_time = current_time_unformated.strftime("%H:%M")

    return current_time

# Praegune kellaaeg
current_time = get_current_time()

# Küsime eleringi API käest ühe päeva elektri börsihinnad
day_prices = get_whole_day_price_info_estonia_dictionary()

# Määrame praeguse hinna/aja väärtused parameetrile
current_energy_price, current_price_time = get_current_energy_price()

# Määrame päeva min ja max hinna/aja
day_min_price, day_min_price_time = get_day_min_price_and_time()
day_max_price, day_max_price_time = get_day_max_price_and_time()

# Kuvame info seoses tänase elektri hinnaga
print("Praegune kellaaeg", current_time)
print("Praegune elektri hind:", current_energy_price, "s/kWh kell", current_price_time)
print("Päeva kõrgeim elektri hind:", day_max_price, "s/kWh kell" ,day_max_price_time)
print("Päeva madalaim elektri hind:", day_min_price, "s/kWh kell", day_min_price_time)

# Kuvame 2h odavaima perioodi
period_average_price, energy_price_time = calculate_lowest_period_cost(2)
print('Odavaim 2 tunnine periood:',period_average_price, 's/kWh' , energy_price_time)


# Päeva keskmine hind // URMO
def get_day_average_price():
    energy_price_sum = 0
    
    for entry in day_prices:
        energy_price_sum += calculate_price(entry["price"])
    energy_price_average = energy_price_sum / len(day_prices)

    return round(energy_price_average, 3)


day_average_price = get_day_average_price()
print("Päeva keskmine elektri hind:", day_average_price, "s/kWh")


# Salvestame päeva hindade info faili
save_day_prices(day_prices, PRICE_DATA_FILE)

# AI poolt graafiku kuva
times = []
price_values = []
for each in day_prices:
    times.append(convert_timestamp(each["timestamp"]))
    price_values.append(calculate_price(each["price"]))
price_charts.draw_price_chart(times, price_values, CHART_FILE)
