import requests
from datetime import datetime, timedelta, timezone

current_energy_price_info = requests.get("https://dashboard.elering.ee/api/nps/price/ee/current").json()

convert_energy_price_to_kWh


print(current_energy_price_info)
