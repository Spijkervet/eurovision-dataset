import requests
from bs4 import BeautifulSoup
from eurovision_entry import EurovisionEntry

def scrape_year(year):
    data = {
    'jahr': str(year),
    'details': '1'
    }

    response = requests.post('https://eschome.net/databaseoutput230.php', data=data)
    soup = BeautifulSoup(response.content, features="html.parser")
    table = soup.find('table', {'id': 'tabelle1'})
    entries = {}
    rows = iter(table.findAll('tr'))
    for table_row in rows:
        columns = table_row.findAll('td')
        if columns:
            idx = '{}_{}'.format(columns[1].text.rstrip().lower(), year)
            args = [c.text.rstrip() for c in columns[1:]]
            details = [c.text.rstrip() for c in rows.__next__().findAll('td')]
            broadcaster, composer, writer = details[1], details[2], details[3]
            ee = EurovisionEntry(*args, year=year, broadcaster=broadcaster, composer=composer, writer=writer)
            entries[idx] = ee
            
            if not columns[1].text.rstrip():
                return None

    return entries