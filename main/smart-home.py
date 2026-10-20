import datetime
import requests

#API päringute jaoks kuupäevad, et oleks alati õige päev
current_date = datetime.datetime.now()
start_date = current_date.date()
end_date = start_date + datetime.timedelta(days=1)

#API päringute URLi variables
url_current_energy_price = "https://dashboard.elering.ee/api/nps/price/ee/current"
url_whole_day_energy_price = f"https://dashboard.elering.ee/api/nps/price?start={start_date}T21:00:00Z&end={end_date}T20:59:59Z"

#Küsime eleringi API käest praeguse ajahetke elektri börsihinna
current_energy_price_info = requests.get(url_current_energy_price).json()
#Küsime eleringi API käest ühe päeva elektri börsihinnad
whole_day_energy_price_info = requests.get(url_whole_day_energy_price).json()

#Võtame eleringi API JSON vastusest hinna väärtuse
current_energy_price_in_mWh = current_energy_price_info["data"][0]["price"]

#Tsükkel, et käia läbi whole_day_energy_price_info oleva hinna parameetrid ja leida kõige kõrgem elektri hind päevas


#Tsükkel, et käia läbi whole_day_energy_price_info oleva hinna parameetrid ja leida kõige madalam elektri hind päevas


print(current_energy_price_info)
print(current_energy_price_in_mWh)
print(whole_day_energy_price_info)
