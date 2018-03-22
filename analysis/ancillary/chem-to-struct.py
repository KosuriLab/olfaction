import csv
from rdkit import Chem
# from chembl_webresource_client.unichem import unichem_client as unichem
from chembl_webresource_client.new_client import new_client

# see these two amazing blog posts from ChEMBL for help/inspiration
# https://chembl.blogspot.com/2016/03/this-python-inchi-key-resolver-will.html
# https://chembl.blogspot.com/2017/07/using-autoencoders-for-molecule.html

# read csv into dict
with open('./ChemicalList_InChl.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) # skip header
    name_map = {name:key for name,key in reader}

# process keys into InChI
molecule = new_client.molecule
records = molecule.get(name_map.values())

record = list()
for name, key in name_map.items():
    print name
    record.append(molecule.get(key))
