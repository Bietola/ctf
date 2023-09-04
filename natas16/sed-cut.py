import fire

def cli(pos, lng):
    pos = pos - 1
    print(rf'sed -e s/^{"."*pos}// -e s/{"."*(lng-pos-1)}\$//')

fire.Fire(cli)
