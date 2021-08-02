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


def betweenness_enz_domain(domain):
    """
    ### To compute betweenness of every enzyme in each network
    :param domain:
    :return: list of dictionary of betweenness for a given domain
    """
    path_nets = "../data/Network/EnzNet/%s/*.gpickle" % domain
    list_dict_betweenness = list()
    for f in glob.glob(path_nets):
        G = load_ezn_net(f)
        list_dict_betweenness.append(nx.betweenness_centrality(G))
    return list_dict_betweenness


def betweenness_EC_net(G):
    list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]

    bet_eclass = dict()
    for ec in range(1, len(list_eclass) + 1):
        bet_eclass[ec] = list()

    dict_bet = nx.betweenness_centrality(G)

    for n in G.nodes():
        first_digit = int(n.split(".")[0])
        for ec in range(1, len(list_eclass) + 1):
            if first_digit == ec:
                bet_eclass[ec].append(dict_bet[n])
                continue

    return bet_eclass



def betweenness_EC_domain(domain):
    path_nets = "../data/Network/EnzNet/%s/*.gpickle"%domain

    list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]

    bet_eclass_domain = dict()
    for ec in range(1, len(list_eclass) + 1):
        bet_eclass_domain[ec] = list()

    for f in glob.glob(path_nets):
        G = load_ezn_net(f)
        distribution_betweenness = betweenness_EC_net(G)
        for ec in range(1, len(list_eclass) + 1):
            bet_eclass_domain[ec] = bet_eclass_domain[ec] + distribution_betweenness[ec]

    return bet_eclass_domain

def write_results(file_name, result):

    dir_results = "../results"
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    dir_topology = os.path.join(dir_results, "topology")
    if not os.path.exists(dir_topology):
        os.mkdir(dir_topology)

    dir_betweenness = os.path.join(dir_topology, "betweenness")
    if not os.path.exists(dir_betweenness):
        os.mkdir(dir_betweenness)

    #path_file  = os.path.join(dir_betweenness, "betweenness_distribution_over_EC_%s.json"%domain)
    path_file = os.path.join(dir_betweenness, file_name)
    with open(path_file, "w") as file:
        json.dump(result, file)


# def test():
#     print("this is test")
#     bt = time.time()
#     domain = "LUCA"
#     betweenness_dist = betweenness_EC_domain(domain)
#     write_results(domain, betweenness_dist)
#     et = time.time()
#     t = et - bt
#     print(t)


def betweenness_distribution_over_ec_class(list_domain):
    # name_eclass = ["oxidoreductase", "transferase", "hydrolase", "lysase", "isomerase", "ligase"]
    for domain in list_domain:
        print(domain)
        betweenness_dist = betweenness_EC_domain(domain)
        file_name = "betweenness_distribution_over_EC_%s.json"%domain
        write_results(file_name, betweenness_dist)

def betweenness_for_every_enzyme(list_domain):
    for domain in list_domain:
        print(domain)
        betweenness_data = betweenness_enz_domain(domain)
        file_name = "betweenness_list_dict_enz_%s.json"%domain
        write_results(file_name, betweenness_data)

if __name__ == "__main__":
    # list_domain = ["Archaea", "Bacteria", "Eukaryota", "Metagenome", "Biosphere", "LUCA"]
    list_domain = ["Bacteria"]
    #betweenness_distribution_over_ec_class(list_domain)
    betweenness_for_every_enzyme(list_domain)