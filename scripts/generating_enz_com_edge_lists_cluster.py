import sys
import json
import networkx as nx
import time

###
def load_file_of_kegg_enzyme_substrates_products():
    with open("../data/list_enzyme_substrate_product.json", "r") as f:
        a = json.load(f)
    return a


def load_list_enzyme_for_domain(path_enz_domain):
    with open(path_enz_domain, "r") as f:
        e = json.load(f)
    return e


def generate_unipartite_enz_net_for_domain(domain):

    dir_net = "../data/Network/EnzNet/" + domain #dirtectory for output

    path_enz_domain = "../data/ProcessedJGI/" + domain + "/No-Glycan/" + domain + "_ec_clean_list_no_glycan.json"

    dict_taxa_enz_in_jgi = load_list_enzyme_for_domain(path_enz_domain)

    dict_enz_com_in_kegg = load_file_of_kegg_enzyme_substrates_products()


    for taxa in dict_taxa_enz_in_jgi:

        B = nx.DiGraph()
        list_comp = list()
        for enz in dict_taxa_enz_in_jgi[taxa]:

            if enz not in dict_enz_com_in_kegg:
                continue

            for subs in dict_enz_com_in_kegg[enz]["subs"]:
                B.add_edge(subs,enz)
                list_comp.append(subs)

            for prod in dict_enz_com_in_kegg[enz]["prod"]:
                B.add_edge(enz, prod)
                list_comp.append(prod)


        G = nx.DiGraph()
        for n in list_comp:
            for e1 in B.predecessors(n):
                for e2 in B.successors(n):
                    G.add_edge(e1,e2)

        nx.write_gpickle(G, dir_net + "/enz_net_%s_%s.gpickle"%(domain, taxa))


def assign_taxa_index_to_domain_data(dict_data, taxa_index):
    list_taxa = sorted(dict_data.keys())
    selected_taxa = list_taxa[taxa_index]
    return selected_taxa

def generate_unipartite_enz_net_for_taxa(domain, taxa_index):

    dir_net = "../data/Network/EnzNet/" + domain #dirtectory for output

    path_enz_domain = "../data/ProcessedJGI/" + domain + "/No-Glycan/" + domain + "_ec_clean_list_no_glycan.json"

    dict_taxa_enz_in_jgi = load_list_enzyme_for_domain(path_enz_domain)

    taxa = assign_taxa_index_to_domain_data(dict_taxa_enz_in_jgi, taxa_index)

    dict_enz_com_in_kegg = load_file_of_kegg_enzyme_substrates_products()

    B = nx.DiGraph()
    list_comp = list()
    for enz in dict_taxa_enz_in_jgi[taxa]:

        if enz not in dict_enz_com_in_kegg:
            continue

        for subs in dict_enz_com_in_kegg[enz]["subs"]:
            B.add_edge(subs,enz)
            list_comp.append(subs)

        for prod in dict_enz_com_in_kegg[enz]["prod"]:
            B.add_edge(enz, prod)
            list_comp.append(prod)


    G = nx.DiGraph()
    for n in list_comp:
        for e1 in B.predecessors(n):
            for e2 in B.successors(n):
                G.add_edge(e1,e2)

    nx.write_gpickle(G, dir_net + "/enz_net_%s_%s.gpickle"%(domain, taxa))


def assign_list_taxa_index_to_domain_data(dict_data, taxa_index, list_length):
    list_taxa = sorted(dict_data.keys())
    selected_taxa_list = list_taxa[taxa_index: taxa_index + list_length]
    return selected_taxa_list


def generate_unipartite_enz_net_for_group_of_taxa(domain, taxa_index, list_length = 100):

    dir_net = "../data/Network/EnzNet/" + domain #dirtectory for output

    path_enz_domain = "../data/ProcessedJGI/" + domain + "/No-Glycan/" + domain + "_ec_clean_list_no_glycan.json"

    dict_taxa_enz_in_jgi = load_list_enzyme_for_domain(path_enz_domain)

    list_taxa = assign_list_taxa_index_to_domain_data(dict_taxa_enz_in_jgi, taxa_index, list_length)

    dict_enz_com_in_kegg = load_file_of_kegg_enzyme_substrates_products()

    for taxa in list_taxa:
        B = nx.DiGraph()
        list_comp = list()
        for enz in dict_taxa_enz_in_jgi[taxa]:

            if enz not in dict_enz_com_in_kegg:
                continue

            for subs in dict_enz_com_in_kegg[enz]["subs"]:
                B.add_edge(subs,enz)
                list_comp.append(subs)

            for prod in dict_enz_com_in_kegg[enz]["prod"]:
                B.add_edge(enz, prod)
                list_comp.append(prod)


        G = nx.DiGraph()
        for n in list_comp:
            for e1 in B.predecessors(n):
                for e2 in B.successors(n):
                    G.add_edge(e1,e2)

        nx.write_gpickle(G, dir_net + "/enz_net_%s_%s.gpickle"%(domain, taxa))


###########################################################################################

def main(arg):
    # list_domain = ["Archaea", "Bacteria", "Eukaryota", "Metagenome", "Biosphere", "LUCA"]

    # domain = "Metagenome"
    #
    # array_index = int(sys.argv[1])
    # array_gap = 100
    #
    # starting_taxa_index = array_index * array_gap
    # array_size = 1
    # if starting_taxa_index == 11900:
    #     array_size = 55

    #domain = "Metagenome" #SBATCH --array 1-120 ( 0 - 119)
    domain = "Bacteria"  #SBATCH --array 1-118 (0 - 117)
    print(domain)
    array_index = int(sys.argv[1])
    array_gap = 100 # for Agave

    starting_taxa_index = array_index * array_gap
    array_size = 1 # for test
    array_size = array_gap
    if domain == "Metagenome" and starting_taxa_index == 11900:
        array_size = 55
    if domain == "Bacteria" and starting_taxa_index == 11700:
        array_size = 59

    generate_unipartite_enz_net_for_group_of_taxa(domain, starting_taxa_index, array_size)

if __name__ == "__main__":
    main(sys.argv[1])


