import os
import json
import glob

### To import all files in enzyme entries of KEGG and put them as a dictionary in a file
### {enz1: {"s":[comp1, comp2, ... ], "p":[comp1, comp3, ...]}, enz2: .... }

def convert_kegg_enzyme_entries_to_single_file(dir_data):

    output = dict()

    path_input = os.path.join(dir_data, "*.json")
    for file in glob.glob(path_input):
        with open(file, "r") as f:
            a = json.load(f)

        s = a[0].get("substrates")
        p = a[0].get("products")
        if s is None or p is None:
            continue

        subs = list()
        for c in a[0]["substrates"]:
            if "CPD:C" not in c:
                continue
            comp = c.split("CPD:")[1][:6]
            subs.append(comp)

        prod = list()
        for c in a[0]["products"]:
            if "CPD:C" not in c:
                continue
            comp = c.split("CPD:")[1][:6]
            prod.append(comp)

        enz = a[0]["entry_id"]
        output[enz] = dict()
        output[enz]["subs"] = subs
        output[enz]["prod"] = prod

    return output



dir_data ="/Users/hkim78/work/enzyme-networks/data/KEGG_enzyme_entries"

enz_subs_prod = convert_kegg_enzyme_entries_to_single_file(dir_data)

dir_output = "/Users/hkim78/work/enzyme-networks/data"
path_output = os.path.join(dir_output, "list_enzyme_substrate_product.json")
with open(path_output, 'w') as f:
    json.dump(enz_subs_prod, f)
