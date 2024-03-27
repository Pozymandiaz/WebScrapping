import os
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine

# Création du driver Chrome
options = webdriver.ChromeOptions()
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)

# Définition de l'URL
url = "https://www.booking.com/searchresults.fr.html?ss=Paris%2C+%C3%8Ele-de-France%2C+France&efdco=1&label=gog235jc-1DCAEoggI46AdIDVgDaE2IAQGYAQ24ARfIAQ_YAQPoAQH4AQKIAgGoAgO4AuPdj7AGwAIB0gIkNGQ1Y2JhZjctNThkMC00MGQzLWE2OGUtYjAyZjlkODJmMzQ32AIE4AIB&aid=397594&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1456928&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=fr&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=0b5c46b196e200d3&ac_meta=GhAwYjVjNDZiMTk2ZTIwMGQzIAAoATICZnI6BXBhcmlzQABKAFAA&ltfd=5%3A1%3A4-2024%3A1%3A&group_adults=2&no_rooms=1&group_children=0"

# Scraping des hôtels
data = []
driver.get(url)
soup = BeautifulSoup(driver.page_source)
hotels = soup.find_all("div", class_="d6767e681c")
for hotel in hotels:
    name = hotel.find("div").text
    hotel_url = hotel.find("a")['href']
    driver.get(hotel_url)
    soup2 = BeautifulSoup(driver.page_source)

    adresse_element = soup2.find("span", class_="hp_address_subtitle js-hp_address_subtitle jq_tooltip")
    adresse = adresse_element.text if adresse_element else None

    note_element = soup2.find("div", class_="ac4a7896c7")
    note = note_element.text if note_element else None

    nbr_avis_element = soup2.find("span", class_="a3b8729ab1 f45d8e4c32 d935416c47")
    nbr_avis = nbr_avis_element.text if nbr_avis_element else None

    rang_elements = soup2.find_all("span", class_="a3b8729ab1 e6208ee469 cb2cbb3ccb")
    rang = rang_elements[0].text if rang_elements else None

    prix_element = soup2.find("span", class_="prco-valign-middle-helper")
    prix = prix_element.text if prix_element else None

    data.append({
        "name": name,
        "hotel_url": hotel_url,
        "adresse": adresse,
        "rang": rang,
        "nbr_avis": nbr_avis,
        "note": note,
        "prix": prix,
    })

    # Pause de 5 secondes
    time.sleep(5)

# Création du DataFrame
df = pd.DataFrame(data)

# Transformation en CSV
df.to_csv('./Hotels_Paris1.csv', index=False)

# Mise en base de données
# Définir les informations de connexion à la base de données MySQL
user = 'root'
password = ''
host = 'localhost'
port = '3306'
database = 'HOTEL'

# Créer une connexion à la base de données
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

# Créer la table dans la base de données et insérer les données
df.to_sql('hotel', con=engine, if_exists='replace', index=False)

# Fermer la connexion à la base de données
engine.dispose()
