# =====================================================================
# AI GENEREERITUD KOOD (Claude) - ülesanne C: hinnagraafikud
# Kogu selle faili sisu on kirjutatud AI poolt.
#
# Kasutamine smart-home.py failis:
#   import price_charts
#   price_charts.draw_price_chart(times, price_values, "hinnagraafik.png")
#
# times        - list kellaaegadest (datetime), nt convert_timestamp() tulemused
# price_values - list hindadest s/kWh, nt calculate_price() tulemused
# =====================================================================
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def draw_price_chart(times, price_values, filename):
    # Päeva max ja min asukoht listis
    max_index = price_values.index(max(price_values))
    min_index = price_values.index(min(price_values))

    plt.figure(figsize=(12, 5))
    # step: hind püsib terve 15 min sama ja muutub hüppega
    plt.step(times, price_values, where="post", label="Hind")
    plt.axvline(datetime.datetime.now(), color="gray", linestyle="--", label="Praegu")
    plt.scatter(times[max_index], price_values[max_index], color="red", zorder=3,
                label=f"Max {price_values[max_index]} s/kWh")
    plt.scatter(times[min_index], price_values[min_index], color="green", zorder=3,
                label=f"Min {price_values[min_index]} s/kWh")

    plt.title("Elektri börsihind " + times[0].strftime("%d.%m.%Y"))
    plt.xlabel("Kellaaeg")
    plt.ylabel("Hind (s/kWh, km-ga)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


# ===== AI GENEREERITUD KOODI LÕPP =====
