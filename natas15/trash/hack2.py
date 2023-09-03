import json
from pathlib import Path
from string import ascii_lowercase as ALC

trie = json.loads(Path('tmp3').read_text())

print(trie)

def list_words(trie):
    my_list = []
    for k,v in trie.items():
        for el in list_words(trie):                
            my_list.append(k+el)
    return my_list

print(list_words(trie))
