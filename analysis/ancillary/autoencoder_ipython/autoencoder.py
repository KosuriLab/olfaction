import json
import gzip
import csv
import random
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from collections import defaultdict
from model import MoleculeVAE
from utils import encode_smiles, decode_latent_molecule, interpolate, get_unique_mols
# since getting ipynb's up and running on servers is painful, do it the oldfashioned way

# make sampling reproducible
random.seed(2813308004)


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

#-------------------------------------------------------------------------------

# load the smiles
with open('../final-chems.tsv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    next(reader) # skip header
    name_map = {store[0]:store[1:] for store in reader if len(store[2]) > 2}

# encode all smiles for all chemicals in our library
# load everything into a pandas dataframe for downstream procs
lib_chems, lib_vecs = zip(*[(key, encode_smiles(val[5], model, charset)) for key, val in name_map.items()])
df = pd.DataFrame(np.concatenate(lib_vecs), dtype='float32', index=lib_chems)
df.to_csv('../chem-vecs.csv')

#-------------------------------------------------------------------------------

# open all of chembl_23 and encode
with gzip.open('../chembl_23.txt.gz', 'rb') as f:
    next(f)
    chembl = [line.decode().split() for line in f]

# encoding will take a while
chems, vecs = zip(*[(key, encode_smiles(val, model, charset)) for key, val in random.sample(chembl, 250000) if len(val) <= 120])
pca = PCA(2)
combo = np.concatenate((np.concatenate(vecs), np.concatenate(lib_vecs)))
df = pd.DataFrame(pca.fit_transform(combo), dtype='float32', index=chems+lib_chems)
df.to_csv('../latent-space-pca.csv.gz', compression='gzip', header=['PC1', 'PC2'])

