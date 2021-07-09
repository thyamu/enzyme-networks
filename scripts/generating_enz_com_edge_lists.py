import os
import json
import networkx as nx


###
def load_file_of_kegg_enzyme_substrates_products():
    with open("/Users/hkim78/work/enzyme-networks/data/list_enzyme_substrate_product.json", "r") as f:
        a = json.load(f)
    return a

def load_list_enzyme_for_domain(path_enz_domain):
    with open(path_enz_domain, "r") as f:
        e = json.load(f)
    return e

def generate_unipartite_enz_net_for_domain(domain):

    dir_net = "../data/Network/EnzNet/" + domain #dirtectory for output

    path_enz_domain = "../data/ProcessedJGI/" + domain + "/No Glycan/" + domain + "_ec_clean_list_no_glycan.json"

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
        #nx.write_graphml(G, dir_net + "/enz_net_%s_%s.graphml"%(domain, taxa))



###########################################################################################
list_domain = ["Archaea", "Bacteria", "Eukaryota", "Metagenome", "Biosphere", "LUCA"]

domain = "Biosphere"

generate_unipartite_enz_net_for_domain(domain)



