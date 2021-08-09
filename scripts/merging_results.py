"""
To combine the results of betweenness measures for metagenome from cluster

"""

import glob
import json



def merging_distribution_betweenness(domain):
    list_eclass = ["1", "2", "3", "4", "5", "6"]

    bet_eclass = dict()
    for ec in list_eclass:
        bet_eclass[ec] = list()

    path = "../results/topology/betweenness/%s_cluster/*.json"%domain
    for path_file in glob.glob(path):
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
            for ec in list_eclass:
                bet_eclass[ec] = bet_eclass[ec] + a[ec]
    # results/topology/betweenness/betweenness_distribution_over_EC_Archaea.json
    path_merged = "../results/topology/betweenness/betweenness_distribution_over_EC_%s.json"%domain
    with open(path_merged, 'w') as f:
        json.dump(bet_eclass, f)


def merging_list_dict_betweenness(domain):
    result = list()

    path = "../results/topology/betweenness/list_dict_%s_cluster/*.json"%domain
    for path_file in glob.glob(path):
        print(path_file)
        with open(path_file, 'r') as f:
            a = json.load(f)
        result = result + a

    path_merged = "../results/topology/betweenness/betweenness_list_dict_enz_%s.json" % domain
    with open(path_merged, 'w') as f:
        json.dump(result, f)



def main():

    merging_distribution_betweenness("Metagenome")

    for domain in ["Bacteria", "Metagenome"]:
        merging_list_dict_betweenness(domain)


if __name__ == "__main__":
    main()