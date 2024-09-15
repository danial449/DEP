import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.scrapethissite.com/pages/simple/'

# Get the HTML content
r = requests.get(url)
htmlContent = r.content

# Parse the HTML 
soup = BeautifulSoup(htmlContent, 'html.parser')

# HTML Traversing to find country details
countries = soup.find_all('div', class_="country")

# Create or open the CSV file for writing
with open('countries_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    
    writer = csv.writer(csvfile)
    
    writer.writerow(['Country Name', 'Capital', 'Population', 'Area'])

    for country in countries:
        
        country_name = country.find('h3', class_='country-name').text.strip()

        capital = country.find('span', class_='country-capital').text.strip()

        population = country.find('span', class_='country-population').text.strip()

        area = country.find('span', class_='country-area').text.strip()

        writer.writerow([country_name, capital, population, area])

print("Data has been written to countries_data.csv")
