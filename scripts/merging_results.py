"""
To combine the results of betweenness measures for metagenome

"""

import glob
import json

list_eclass = ["1", "2", "3", "4", "5", "6"]

bet_eclass = dict()
for ec in list_eclass:
    bet_eclass[ec] = list()

path = "../results/topology/betweenness/metagenome_cluster/*.json"
for path_file in glob.glob(path):
    print(path_file)
    with open(path_file, 'r') as f:
        a = json.load(f)
        for ec in list_eclass:
            bet_eclass[ec] = bet_eclass[ec] + a[ec]
# results/topology/betweenness/betweenness_distribution_over_EC_Archaea.json
path_merged = "../results/topology/betweenness/betweenness_distribution_over_EC_metagenome.json"
with open(path_merged, 'w') as f:
    json.dump(bet_eclass, f)