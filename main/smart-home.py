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
current_energy_price = current_energy_price_info['data'][0]
#Küsime eleringi API käest ühe päeva elektri börsihinnad
whole_day_energy_price_info = requests.get(url_whole_day_energy_price).json()
day_prices = whole_day_energy_price_info['data']["ee"]

#Võtame eleringi API JSON vastusest hinna väärtuse
current_energy_price_in_MWh = calculate_price(current_energy_price["price"])
current_price_time = convert_timestamp(current_energy_price["timestamp"])
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
print("Praegune elektri hind:", current_energy_price_in_MWh, "s/kWh kell", current_price_time)
print("Päeva kõrgeim elektri hind:", max_day_energy_price_in_kWh, "s/kWh kell" , max_price_time)
print("Päeva madalaim elektri hind:", min_day_energy_price_in_kWh, "s/kWh kell", min_price_time)
