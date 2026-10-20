import requests
from datetime import datetime, timedelta, timezone

print(requests.get("https://dashboard.elering.ee/api/nps/price/ee/current").json())
