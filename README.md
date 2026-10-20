# Programmeerimise Alused - Paaristöö Projekt

* **Paarilised:** Alo Kobin ja Urmo Kasela
* **Esitamise tähtaeg:** 8. november 2026, kell 23:59

## Ülesande kirjeldus
Mõtle läbi ja pane kirja oma projekti idee.

### Projekti nõuded:
1. **Paaristöö:** Lubatud teha ainult paaris (kuni 2 inimest).
2. **Koodi maht:** 60–90 rida iseseisvalt kirjutatud ja kordumatut koodi ühe inimese kohta.
3. **Struktuur:** Vähemalt üks tsükkel (kordus) ja vähemalt 2 enda loodud kasutajafunktsiooni.
4. **Töökindlus:** Programm peab töötama plaanipäraselt.
5. **Tehisintellekti (AI) kasutamine:** 
   * Dialoog peab olema dokumenteeritud (küsimused, vastused, promptid jmt).
   * Koodis peab olema kommentaaridega märgitud, millise osa kirjutas AI.
   * AI genereeritud kood ei lähe nõutud iseseisvalt kirjutatud rea hulka.
6. **Esitamine:** KRE rühmadel on kohustuslik lisada GitHubi link projektile.
7. **Kaitsmine:** Projekti suuline kaitsmine.

# Elektri börsihinna näidik

Programmeerimise Alused – paaristöö projekt

**Autorid:** _(nimed)_

## Projekti eesmärk

Programm küsib Eleringi avalikust API-st Eesti tänase päeva elektri börsihinnad ja kuvab väikesel ekraanil:

- praeguse hinna
- päeva maksimumhinna (ja selle kellaaja)

## Andmeallikas

Elering Dashboard API (avalik, registreerimist ega API võtit pole vaja):

- Praegune hind: `https://dashboard.elering.ee/api/nps/price/ee/current`
- Ajavahemiku hinnad: `https://dashboard.elering.ee/api/nps/price?start=...&end=...`

Olulised märkused:

- Hind on **€/MWh ja ilma käibemaksuta**. Sendid kWh kohta = hind / 10.
- Hinnad on **15-minutiliste vahemikena** (umbes 96 kirjet päevas).
- Ajad on **UTC-s**, Eesti aeg on UTC+2 (talvel) või UTC+3 (suvel).

## Vajalik tarkvara

- Python 3
- `requests` pakett: `pip install requests`

## Projekti plaan

Iga etapi lõpuks peab olema midagi, mis töötab ja mida saab katsetada.

### 1. etapp: andmete kättesaamine
- [ ] Teha päring Eleringi API-le
- [ ] Printida vastus ekraanile täpselt sellisena, nagu see tuleb

**Teemad:** paketi paigaldamine, `import`, muutujad

### 2. etapp: vastuse lahtiharutamine
- [ ] Saada vastusest kätte ainult praegune hind
- [ ] Printida hind eraldi välja

**Teemad:** sõnastikud (dict), listid, väärtuste kättesaamine

### 3. etapp: arvutamine ja vormindamine
- [ ] Teisendada hind €/MWh-st s/kWh-ks
- [ ] Otsustada, kas lisada käibemaks (24%)
- [ ] Võrrelda tulemust mõne elektrimüüja äpiga

**Teemad:** aritmeetika, ümardamine, f-stringid

### 4. etapp: terve päeva hinnad
- [ ] Küsida kogu tänase päeva hinnad
- [ ] Leida nende seast maksimum
- [ ] Leida, mis kell maksimum on

**Teemad:** `for`-tsükkel, `if`-tingimus, kuupäevad ja kellaajad (`datetime`)

### 5. etapp: koodi korrastamine
- [ ] Jagada kood funktsioonideks (nt hindade küsimine, maksimumi leidmine)

**Teemad:** funktsioonid, parameetrid, `return`

### 6. etapp: vigade käsitlemine
- [ ] Programm ei jookse kokku, kui internet on maas või Elering ei vasta

**Teemad:** `try` / `except`

### 7. etapp: ekraanile kuvamine
- [ ] Esialgu kuvamine terminalis
- [ ] Valida riistvara (nt Raspberry Pi, ESP32) ja ekraan
- [ ] Kuvada hinnad päris ekraanil

### 8. etapp: automaatne uuendamine (lisaülesanne)
- [ ] Programm uuendab hinda iga 15 minuti järel ise

**Teemad:** `while`-tsükkel, `time.sleep`

## Töökorraldus

Kasutame paarisprogrammeerimist:

- **Juht** kirjutab koodi.
- **Navigeerija** jälgib, mõtleb kaasa ja märkab vigu.
- Rolle vahetame iga etapi järel, et mõlemad saaksid kõigest aru.
- Pärast iga etappi teeme Gitis commiti.