"""
To merge results from three domain to pantaxa
"""

import glob
import json


def merging_dist_degree_ec_class():

    list_eclass = ["1", "2", "3", "4", "5", "6"]

    deg_eclass = dict()
    for ec in list_eclass:
        deg_eclass[ec] = list()

    list_domain = ["Archaea", "Bacteria", "Eukaryota"]
    for domain in list_domain:
        path_file = "../results/topology/degree/degree_distribution_over_EC_%s.json"%domain
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
            for ec in list_eclass:
                deg_eclass[ec] = deg_eclass[ec] + a[ec]
    path_merged = "../results/topology/degree/degree_distribution_over_EC_Pantaxa.json"
    with open(path_merged, 'w') as f:
        json.dump(deg_eclass, f)



def merging_dist_betweenness_ec_class():

    list_eclass = ["1", "2", "3", "4", "5", "6"]

    bet_eclass = dict()
    for ec in list_eclass:
        bet_eclass[ec] = list()

    list_domain = ["Archaea", "Bacteria", "Eukaryota"]
    for domain in list_domain:
        path_file = "../results/topology/betweenness/betweenness_distribution_over_EC_%s.json"%domain
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
            for ec in list_eclass:
                bet_eclass[ec] = bet_eclass[ec] + a[ec]
    path_merged = "../results/topology/betweenness/betweenness_distribution_over_EC_Pantaxa.json"
    with open(path_merged, 'w') as f:
        json.dump(bet_eclass, f)




if __name__ == "__main__":
    merging_dist_degree_ec_class()