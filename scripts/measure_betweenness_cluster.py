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


def load_list_enzyme_for_domain(path_enz_domain):
    with open(path_enz_domain, "r") as f:
        e = json.load(f)
    return e


def assign_list_taxa_index_to_domain_data(dict_data, taxa_index, list_length):
    list_taxa = sorted(dict_data.keys())
    selected_taxa_list = list_taxa[taxa_index: taxa_index + list_length]
    return selected_taxa_list


# def betweenness_EC_domain(domain):
#     path_nets = "../data/Network/EnzNet/%s/*.gpickle"%domain
#
#     list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]
#
#     bet_eclass_domain = dict()
#     for ec in range(1, len(list_eclass) + 1):
#         bet_eclass_domain[ec] = list()
#
#     for f in glob.glob(path_nets):
#         G = load_ezn_net(f)
#         distribution_betweenness = betweenness_EC_net(G)
#         for ec in range(1, len(list_eclass) + 1):
#             bet_eclass_domain[ec] = bet_eclass_domain[ec] + distribution_betweenness[ec]
#
#     return bet_eclass_domain


def betweenness_EC_group_of_taxa(domain, taxa_index, list_length = 100):


    path_enz_domain = "../data/ProcessedJGI/" + domain + "/No-Glycan/" + domain + "_ec_clean_list_no_glycan.json"

    dict_taxa_enz_in_jgi = load_list_enzyme_for_domain(path_enz_domain)

    list_taxa = assign_list_taxa_index_to_domain_data(dict_taxa_enz_in_jgi, taxa_index, list_length)

    # path_nets = "../data/Network/EnzNet/%s/*.gpickle"%domain

    list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]

    bet_eclass_domain = dict()
    for ec in range(1, len(list_eclass) + 1):
        bet_eclass_domain[ec] = list()

    for taxa in list_taxa:
        f = "../data/Network/EnzNet/%s/enz_net_%s_%s.gpickle"%(domain, domain, taxa)
        G = load_ezn_net(f)
        distribution_betweenness = betweenness_EC_net(G)
        for ec in range(1, len(list_eclass) + 1):
            bet_eclass_domain[ec] = bet_eclass_domain[ec] + distribution_betweenness[ec]

    return bet_eclass_domain


# def betweenness_EC_domain(domain):
#     path_nets = "../data/Network/EnzNet/%s/*.gpickle"%domain
#
#     list_eclass = ["e1", "e2", "e3", "e4", "e5", "e6"]
#
#     bet_eclass_domain = dict()
#     for ec in range(1, len(list_eclass) + 1):
#         bet_eclass_domain[ec] = list()
#
#     for f in glob.glob(path_nets):
#         G = load_ezn_net(f)
#         distribution_betweenness = betweenness_EC_net(G)
#         for ec in range(1, len(list_eclass) + 1):
#             bet_eclass_domain[ec] = bet_eclass_domain[ec] + distribution_betweenness[ec]
#
#     return bet_eclass_domain


def write_results_group_of_taxa(domain, result, index):

    dir_results = "../results"
    if not os.path.exists(dir_results):
        os.mkdir(dir_results)

    dir_topology = os.path.join(dir_results, "topology")
    if not os.path.exists(dir_topology):
        os.mkdir(dir_topology)

    dir_betweenness = os.path.join(dir_topology, "betweenness")
    if not os.path.exists(dir_betweenness):
        os.mkdir(dir_betweenness)

    path_file  = os.path.join(dir_betweenness, "betweenness_distribution_over_EC_%s_%s.json"%(domain, index))
    with open(path_file, "w") as file:
        json.dump(result, file)


# def write_results(domain, result):
#
#     dir_results = "../results"
#     if not os.path.exists(dir_results):
#         os.mkdir(dir_results)
#
#     dir_topology = os.path.join(dir_results, "topology")
#     if not os.path.exists(dir_topology):
#         os.mkdir(dir_topology)
#
#     dir_betweenness = os.path.join(dir_topology, "betweenness")
#     if not os.path.exists(dir_betweenness):
#         os.mkdir(dir_betweenness)
#
#     path_file  = os.path.join(dir_betweenness, "betweenness_distribution_over_EC_%s.json"%domain)
#     with open(path_file, "w") as file:
#         json.dump(result, file)


# def test():
#     print("this is test")
#     bt = time.time()
#     domain = "LUCA"
#     betweenness_dist = betweenness_EC_group_of_taxa(domain)
#     write_results_group_of_taxa(domain, betweenness_dist)
#     et = time.time()
#     t = et - bt
#     print(t)


def main(arg):
    # name_eclass = ["oxidoreductase", "transferase", "hydrolase", "lysase", "isomerase", "ligase"]

    domain = "Metagenome"
    print(domain)
    array_index = int(sys.argv[1])
    array_gap = 100

    starting_taxa_index = array_index * array_gap
    array_size = 1
    if starting_taxa_index == 11900:
        array_size = 55

    betweenness_dist = betweenness_EC_group_of_taxa(domain, starting_taxa_index, array_size)
    write_results_group_of_taxa(domain, betweenness_dist, array_index)

if __name__ == "__main__":
    main(sys.argv[1])
