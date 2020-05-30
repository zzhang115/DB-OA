import re
import requests
from bs4 import BeautifulSoup

url = 'https://dot.ca.gov/contact-us'

def get_office_info(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    tables = soup.find_all('tbody')
    office_table = tables[0]
    offices = []
    for tr in office_table.find_all('tr'):
        office = {}
        tds = tr.find_all('td')
        office['office_name'] = tds[0].getText()
        office_link_a = tds[0].find('a')
        office_link = None
        if office_link_a:
            office_link = url + office_link_a['href']
        office['office_link'] = office_link

        office_full_addr = tds[1].find('a').getText()
        if office_full_addr:
            match = re.search(r'(.+?)[\\\n](.+)', office_full_addr)
            if match:
                office['office_address'] = match.group(1).strip()
                office_city_state_zip = match.group(2)
                city_state_zip_match = re.search(r'(.+?)([A-Z]+)\s([0-9]+)', office_city_state_zip)
                if city_state_zip_match:
                    office['office_city'] = city_state_zip_match.group(1).replace(',', '').strip()
                    office['office_state'] = city_state_zip_match.group(2).strip()
                    office['office_zip'] = city_state_zip_match.group(3).strip()

        office_mail_addr = tds[2].getText()
        if office_mail_addr:
            match = re.search(r'(.+?)[\\\n](.+)', office_mail_addr)
            if match:
                office['mail_address'] = match.group(1).strip()
                mail_city_state_zip = match.group(2)
                mail_state_zip_match = re.search(r'(.+?)([A-Z]+)\s([0-9]+)', mail_city_state_zip)
                if mail_state_zip_match:
                    office['mail_city'] = mail_state_zip_match.group(1).replace(',', '').strip()
                    office['mail_state'] = mail_state_zip_match.group(2).strip()
                    office['mail_zip'] = mail_state_zip_match.group(3).strip()

        offices.append(office)
    return offices

print(get_office_info(url))