import os
import json

path = '../../data/us/raw/legislators'
sessions = ['113', '114', '115']
dates = {
    '113': (2013,2015),
    '114': (2015,2017),
    '115': (2017,2019)
}

def in_session(session, term):
    start, end = dates[session]
    tstart, tend = int(term["start"][:4]), int(term["end"][:4])
    return tstart <= start and end <= tend

legislators = {}

for file in ['legislators-current.json', 'legislators-historical.json']:
    with open(os.path.join(path, file), 'r') as f:
        data = json.load(f)
        for session in sessions:
            for member in data:
                id_ = member['id']['bioguide']
                for term in member['terms']:
                    if '2013' <= term['start'][:4]:
                        if session not in legislators:
                            legislators[session] = {}
                        if id_ not in legislators[session]:
                            legislators[session][id_] = term['party']


for session in sessions:
    with open(f'{path}/parties.{session}.csv', 'w+') as f:
        f.write('bioguide_id,party\n')
        for id_, party in legislators[session].items():
            f.write(f'{id_},{party}\n')