import sys
import os
import networkx as nx
import glob
import json
import time


"""
11955 metagenomes
1282 archaea
11759 bacteria
200 eukaryotic taxa
"""

def load_ezn_net(path_net):
    G = nx.read_gpickle(path_net)
    return G


def degree_EC_net(G):
    list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]

    deg_eclass = dict()
    for ec in range(1, len(list_eclass) + 1):
        deg_eclass[ec] = list()

    for n, d in G.degree():
        first_digit = int(n.split(".")[0])
        for ec in range(1, len(list_eclass) + 1):
            if first_digit == ec:
                deg_eclass[ec].append(d)
                continue
    return deg_eclass


def degree_EC_domain(domain):
    path_nets = "../data/Network/EnzNet/%s/*.gpickle"%domain

    list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]

    deg_eclass_domain = dict()
    for ec in range(1, len(list_eclass) + 1):
        deg_eclass_domain[ec] = list()

    for f in glob.glob(path_nets):
        G = load_ezn_net(f)
        distribution_degree = degree_EC_net(G)
        for ec in range(1, len(list_eclass) + 1):
            deg_eclass_domain[ec] = deg_eclass_domain[ec] + distribution_degree[ec]

    return deg_eclass_domain

def write_results(domain, result):

    dir_results = "../results"
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    dir_topology = os.path.join(dir_results, "topology")
    if not os.path.exists(dir_topology):
        os.mkdir(dir_topology)

    dir_degree = os.path.join(dir_topology, "degree")
    if not os.path.exists(dir_degree):
        os.mkdir(dir_degree)

    path_file  = os.path.join(dir_degree, "degree_distribution_over_EC_%s.json"%domain)
    with open(path_file, "w") as file:
        json.dump(result, file)


def test():
    print("this is test")
    bt = time.time()
    domain = "Archaea"
    degree_dist = degree_EC_domain(domain)
    write_results(domain, degree_dist)
    et = time.time()
    t = et - bt
    print(t)


def main():
    # name_eclass = ["oxidoreductase", "transferase", "hydrolase", "lysase", "isomerase", "ligase"]

    # list_domain = ["Archaea", "Bacteria", "Eukaryota", "Metagenome", "Biosphere", "LUCA"]
    list_domain = ["Archaea", "Eukaryota", "Biosphere", "LUCA"]
    for domain in list_domain:
        print(domain)
        degree_dist = degree_EC_domain(domain)
        write_results(domain, degree_dist)

if __name__ == "__main__":
    main()







### LUCA ==> 0.057
### Biosphere ==> 845

