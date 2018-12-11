import os
import json
from functools import reduce

path = '../../data/us/raw/legislators'
legislators = {}

for file in ['legislators-current.json', 'legislators-historical.json']:
    with open(os.path.join(path, file), 'r') as f:
        data = json.load(f)
        for member in data:
            id_ = member['id']['bioguide']
            if id_ not in legislators:
                legislators[id_] = member['terms']                

with open(f'{path}/terms.csv', 'w') as f:
    f.write('bioguide_id,party\n')
    for id_, terms in legislators.items():
        parties = []
        for i, term in enumerate(terms):
            if int(term['end'][:4]) >= 2013 or int(term['start'][:4]) >= 2013:
                party = term['party'] if 'party' in term else 'Independent'
                parties.append(party)
        if int(term['end'][:4]) >= 2013 or int(term['start'][:4]) >= 2013:
            f.write(f'{id_},{parties[-1]}\n')