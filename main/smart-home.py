import datetime
import os
import requests
import csv
import price_charts

# Constants
income_tax = 24

# Lihtsustamis funktsioon timestampi konvertimiseks kuupäevaks
def convert_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)

# Funktsioon, et konverti MWh > s/kWh ja arvutada juurde käibemaks
def calculate_price(price):
    return round((price / 1000) * (income_tax/100 + 1) * 100, 3)

# Loop, läbimiseks päeva hinnad ja iga 15 min tagant tagastada 2 tunni keskmise hinde
def calculate_lowest_period_cost(hours):
    period = hours * 4
    lowest_energy_price_range = 99999
    lowest_energy_price_time = convert_timestamp(day_prices[0]["timestamp"])

    #AI aitas kuidas seda for loopi tuleks alustada
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
            datawriter.writerow(["timestamp", "time", "price", "income_tax"])

    if not already_saved:
        with open(filename, "a", newline='') as datafile:
            datawriter = csv.writer(datafile)
            for row in range(len(prices)):
                timestamp = int(prices[row]["timestamp"])
                datawriter.writerow([
                    timestamp,
                    convert_timestamp(prices[row]["timestamp"]),
                    prices[row]["price"],
                    int(income_tax)])

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

# Kuvame info seoses tänase elektri hinnaga
print("Praegune kellaaeg", current_time)
print("Praegune elektri hind:", current_energy_price, "s/kWh kell", convert_timestamp(current_price_time))
print("Päeva kõrgeim elektri hind:", max_day_energy_price_in_kWh, "s/kWh kell" ,convert_timestamp(max_price_time))
print("Päeva madalaim elektri hind:", min_day_energy_price_in_kWh, "s/kWh kell", convert_timestamp(min_price_time))

# Kuvame 2h odavaima perioodi
period_average_price, energy_price_time = calculate_lowest_period_cost(2)
print('Odavaim 2 tunnine periood:',period_average_price, 's/kWh' , energy_price_time)

save_day_prices(day_prices, "./data/energy.csv")

#AI poolt graafiku kuva
times = []
price_values = []
for each in day_prices:
    times.append(convert_timestamp(each["timestamp"]))
    price_values.append(calculate_price(each["price"]))
price_charts.draw_price_chart(times, price_values, "hinnagraafik.png")
