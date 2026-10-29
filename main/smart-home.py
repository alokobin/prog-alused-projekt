import datetime
import requests

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

#Võtame eleringi API JSON vastusest hinna väärtuse
current_energy_price_in_MWh = current_energy_price_info["data"][0]["price"]
max_day_energy_price_in_MWh = whole_day_energy_price_info["data"]["ee"][0]["price"]
min_day_energy_price_in_MWh = whole_day_energy_price_info["data"]["ee"][0]["price"]
current_price_time = datetime.datetime.fromtimestamp(current_energy_price_info["data"][0]["timestamp"])
max_price_time = whole_day_energy_price_info["data"]["ee"][0]["timestamp"]
min_price_time = whole_day_energy_price_info["data"]["ee"][0]["timestamp"]

#Tsükkel, et käia läbi whole_day_energy_price_info oleva hinna parameetrid ja leida kõige kõrgem elektri hind päevas
for timeslot in whole_day_energy_price_info["data"]["ee"]:
    energy_price = timeslot["price"]
    if energy_price > max_day_energy_price_in_MWh:
        max_day_energy_price_in_mWh = energy_price
        max_price_time = datetime.datetime.fromtimestamp(timeslot["timestamp"])
    if energy_price < min_day_energy_price_in_MWh:
        min_day_energy_price_in_mWh = energy_price
        min_price_time = datetime.datetime.fromtimestamp(timeslot["timestamp"])

max_day_energy_price_in_kWh = round(max_day_energy_price_in_MWh / 1000, 2)
min_day_energy_price_in_kWh = round(min_day_energy_price_in_MWh / 1000, 2)


#print(current_energy_price_info)
#print(whole_day_energy_price_info)
print("Praegune kellaaeg", current_time)
print("Praegune elektri hind:", current_energy_price_in_MWh, "mWh kell", current_price_time)
print("Päeva kõrgeim elektri hind:", max_day_energy_price_in_kWh, "eur/kWh kell" , max_price_time)
print("Päeva madalaim elektri hind:", min_day_energy_price_in_kWh, "eur/kWh kell", min_price_time)
