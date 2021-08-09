"""
To merge results from three domain to pantaxa
"""

import sys
import json


def merging_dist_centrality_ec_class(kind):

    if kind != "degree" and kind != "betweenness":
        sys.exit("kind should be either degree or betweenness")

    list_eclass = ["1", "2", "3", "4", "5", "6"]

    data_eclass = dict()
    for ec in list_eclass:
        data_eclass[ec] = list()

    list_domain = ["Archaea", "Bacteria", "Eukaryota"]
    for domain in list_domain:
        path_file = "../results/topology/%s/%s_distribution_over_EC_%s.json"%(kind, kind, domain)
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
            for ec in list_eclass:
                data_eclass[ec] = data_eclass[ec] + a[ec]
    path_merged = "../results/topology/%s/%s_distribution_over_EC_Pantaxa.json"%(kind, kind)
    with open(path_merged, 'w') as f:
        json.dump(data_eclass, f)



def merging_list_dict_ezn(kind):
    if kind != "degree" and kind != "betweenness":
        sys.exit("kind should be either degree or betweenness")

    result = list()

    list_domain = ["Archaea", "Bacteria", "Eukaryota"]
    for domain in list_domain:
        path_file = "../results/topology/%s/%s_list_dict_enz_%s.json"%(kind, kind, domain)
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
        result = result + a

    path_merged = "../results/topology/%s/%s_list_dict_enz_Pantaxa.json"%(kind, kind)
    with open(path_merged, 'w') as f:
        json.dump(result, f)


if __name__ == "__main__":
    # merging_dist_centrality_ec_class("degree")
    merging_list_dict_ezn("betweenness")