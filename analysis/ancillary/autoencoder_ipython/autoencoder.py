import json
import csv
import numpy as np
from collections import defaultdict
from model import MoleculeVAE
from utils import encode_smiles, decode_latent_molecule, interpolate, get_unique_mols
# since getting ipynb's up and running on servers is painful, do it the oldfashioned way


# number of dimensions to represent the molecules
# as the model was trained with this number, any operation made with the model must share the dimensions.
latent_dim = 292

# trained_model 0.99 validation accuracy
# trained with 80% of ALL chembl molecules, validated on the other 20.
trained_model = 'chembl_23_model.h5'
charset_file = 'charset.json'

# load charset and model
with open('charset.json', 'r') as outfile:
    charset = json.load(outfile)

model = MoleculeVAE()
model.load(charset, trained_model, latent_rep_size = latent_dim)

# load the smiles
with open('../final-chems.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) # skip header
    name_ma = {store[0]:store[1] for store in reader if len(store[2]) > 2}
