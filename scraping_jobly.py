

import requests  # Används för att skicka HTTP-förfrågningar
from bs4 import BeautifulSoup  # Används för att analysera HTML-sidor
import pandas as pd  # Används för att hantera och spara data i en tabell
import os  # Används för att hantera fil- och katalogoperationer

# URL till Jobly
URL = "https://www.jobly.fi/tyopaikat?search=it&job_geo_location=&Etsi+ty%C3%B6paikkoja=Etsi+ty%C3%B6paikkoja&lat=&lon=&country=&administrative_area_level_1="

# Skicka en HTTP-förfrågan till webbsidan med en User-Agent för att efterlikna en webbläsare
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)

# Kontrollera om begäran lyckades
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")  # Analysera HTML-innehållet
    job_list = []  # Lista för att lagra jobbinformation
    
    # Hitta alla jobbannonser genom att söka efter h2-taggar med klassen "node__title"
    job_posts = soup.find_all("h2", class_="node__title")
    
    for job in job_posts:
        # Hämta jobbtitel och URL
        title_tag = job.find("a", class_="recruiter-job-link")
        title = title_tag.text.strip() if title_tag else "Ej tillgängligt"
        job_url = title_tag["href"] if title_tag else "Ingen URL"
        
        # Hämta företagsnamn
        company_tag = job.find_next("a")
        company = company_tag.text.strip() if company_tag else "Ej tillgängligt"
        
        # Hämta plats från <span> inuti <div class="location">
        location_tag = job.find_next("div", class_="location").find("span")
        location = location_tag.text.strip() if location_tag else "Ej tillgängligt"
        
        # Hämta publiceringsdatum
        date_tag = job.find_next("span", class_="date")
        date = date_tag.text.strip() if date_tag else "Ej tillgängligt"
        
        # Hämta endast företagslogotypens URL från data-src-attributet
        logo_tag = job.find_next("div", class_="location").find("img", class_="lazyloaded")
        logo_url = logo_tag["data-src"] if logo_tag and "data-src" in logo_tag.attrs else "Ingen bild"
        
        # Lägg till all information i listan
        job_list.append([title, job_url, date, company, location, logo_url])
    
    # Skapa en Pandas DataFrame
    df = pd.DataFrame(job_list, columns=["Jobbtitel", "URL", "Publiceringsdatum", "Företagsnamn", "Plats", "Företagets logotyp URL"])
    
    # Spara DataFrame till en Excel-fil
    output_file = "IT-jobb.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data sparad i {output_file}")
else:
    print("Kunde inte hämta sidan.")
