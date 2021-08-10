'''
Statistics of centrality  for every enzyme
'''


import sys
import pandas as pd
import numpy as np
import json
import time


class Domain:

    def __init__(self, name):
        self.name = name

        self.path_degree = "../results/topology/degree/degree_list_dict_enz_%s.json" % (self.name)

        self.path_betweenness = "../results/topology/betweenness/betweenness_list_dict_enz_%s.json" % (self.name)

        cb = {'black': [0, 0, 0], 'orange': [230 / 255, 159 / 255, 0], 'skyblue': [86 / 255, 180 / 255, 233 / 255],
              'bluishgreen': [0, 158 / 255, 115 / 255], 'yellow': [240 / 255, 228 / 255, 66 / 255],
              'blue': [0, 114 / 255, 178 / 255],
              'vermillion': [213 / 255, 94 / 255, 0], 'reddishpurple': [204 / 255, 121 / 255, 167 / 255],
              'brown': [109, 22, 3]}

        # 'brown': HEX #6D1603 RGB 109, 22, 3  HSL 11, 97%, 22%
        color = {'Metagenome': cb['bluishgreen'],
                 'Bacteria': cb['blue'],
                 'Archaea': cb['vermillion'],
                 'Eukaryota': cb['orange'],
                 'Pantaxa': cb['reddishpurple'],
                 'LUCA': cb['black'],
                 'Biosphere': cb['skyblue']}

        self.color = color[self.name]


def load_json(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def load_data(domain, kind="degree"):  # kind = "degree" or "betweenness"

    if kind == "degree":
        path = domain.path_degree
    elif kind == "betweenness":
        path = domain.path_betweenness
    else:
        sys.exit("kind should be either degree or betweenness")

    list_dict = load_json(path)

    df = pd.DataFrame()
    for n in range(0, len(list_dict)):
        new_data = pd.DataFrame.from_dict(list_dict[n], orient="index")  # Enzyme node becomes index
        df = pd.concat([df, new_data])

    df.columns = [kind]  # Assign the name of the column for degree
    df["enz"] = df.index  # Assign the name of the column for nodes aside from index
    df["ec_class"] = df["enz"].str.split('.').str[
        0]  # EC class determined by the first digit will be added as a separate column
    return df


def load_list_enzyme(df):
    return sorted(list(set(df["enz"])))


def stat_centrality(domain, kind="degree"):
    if kind != "degree" and kind != "betweenness":
        sys.exit("kind should be either degree or betweenness")

    df = load_data(domain, kind)
    list_enz = load_list_enzyme(df)

    ds = dict()
    for enz in list_enz:
        centrality = df[df["enz"] == enz][kind].values
        ave = np.mean(centrality)
        std = np.std(centrality)
        ds[enz] = [ave, std]# , ignore_index=True)
    return ds



def write_result(result, path):
    with open(path, 'w') as f:
        json.dump(result, f)


if __name__ == "__main__":


    archaea = Domain('Archaea')
    bacteria = Domain('Bacteria')
    eukaryota = Domain('Eukaryota')
    metagenome = Domain('Metagenome')
    luca = Domain("LUCA")
    biosphere = Domain("Biosphere")
    pantaxa = Domain("Pantaxa")


    # list_domain = [luca, archaea, bacteria, eukaryota, pantaxa, metagenome, biosphere]
    # pantaxa ==> 1500s
    # metagenome ==> 3000s
    # bacteria ==> 1200s

    list_domain = [archaea]
    for domain in list_domain:

        bt = time.time()
        print(domain.name, "degree")
        ds = stat_centrality(domain, "degree")
        ds_path = "../results/topology/degree/degree_stat_enz_%s.json"%(domain.name)
        write_result(ds, ds_path)

        et = time.time()
        print("time", et - bt)

    for domain in list_domain:

        bt = time.time()
        print(domain.name, "between")
        ds = stat_centrality(domain, "betweenness")
        ds_path = "../results/topology/betweenness/betweenness_stat_enz_%s.json"%(domain.name)
        write_result(ds, ds_path)

        et = time.time()
        print("time", et - bt)



