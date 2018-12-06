from bs4 import BeautifulSoup
from requests import get
from re import search
from tqdm import trange, tqdm


bills, sponsors = {}, {}

def check_sponsor(card):
    name = card.find('div', {'class': 'title'}).text.strip().replace(' ','')

    if name in sponsors:
        sponsors[name]['num_bill'] += 1
    else:
        sponsors[name] = {
            'name': name,
            'party': card.find('div', {'class': 'party'}).text.strip().replace(' ',''),
            'num_bill': 1
        }
    return sponsors[name]

def check_bill(card):
    bill = {}

    # general information
    bill['number'] = card.find('div', {'class': 'number'}).div.text.strip()
    bill['title'] = card.find('div', {'class': 'title'}).text.strip()
    bill['primary'] = card.find('div', {'class': 'member-name'}).text.strip().replace(' ', '')
    
    # detailed information
    details = BeautifulSoup(get(uri + card['href']).text, "html5lib")

    date_info = details.find('div', {'class': 'date-info'}).text.strip()
    parsed = search(r'(\d{2} \w+ \d{4})\s+(\d{4}-\d{2}) Session', date_info)

    bill['date'] = parsed.group(1)
    bill['session'] = parsed.group(2)

    bill['text'] = details.find('div', {'class': 'motion-text'}).text.strip()

    # sponsor information
    sponsor_list = details.find('div', {'class': 'member-list'}).find_all('a')
    bill['sponsors'] = [check_sponsor(card)['name'] for card in sponsor_list]

    # add to bills
    bills[bill['number']] = bill


uri = 'http://edm.parliament.uk'
page = BeautifulSoup(get(uri).text, "html5lib")

num_pages = int(search(r'page \d+ of (\d+)', page.find('p', {'class': 'pagination-total'}).text).group(1))

for i in trange(num_pages, desc='Scraping'):
    # process bills
    for bill in tqdm(page.find_all('a', {'class': 'details-card-edm'})):
        check_bill(bill)
    # go to next page
    if i < num_pages - 1:
        next_uri = uri + page.find('ul', {'class': 'pagination'}) \
                            .find('li', {'class': 'next'}).a['href']
        page = BeautifulSoup(get(next_uri).text, "html5lib")

# write sponsors
with open('../../data/uk/raw/sponsors.csv', 'w+') as f:
    f.write('name;party;num_bill\n')
    for name, sponsor in tqdm(sponsors.items(), desc='Writing Sponsors'):
        f.write(f"{name};{sponsor['party']};{sponsor['num_bill']}\n")

# write bills
with open('../../data/uk/raw/bills.json', 'w') as f:
    with tqdm(desc='Writing Bills') as pbar:
        from json import dumps as to_json
        f.write(to_json(bills))
        pbar.update()

# write cosponsorship edges
with open('../../data/uk/raw/cosponsorships.csv', 'w+') as f:
    for number, bill in tqdm(bills.items(), desc='Writing Cosponsors'):
        sponsors = bill['sponsors']
        primary, cosponsors = sponsors[0], sponsors[1:]
        
        for cosponsor in tqdm(cosponsors, desc=f'Bill {number}'):
            f.write(f"{primary};{cosponsor}\n")