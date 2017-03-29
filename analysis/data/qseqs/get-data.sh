#!/bin/bash
for f in ../../../raw-data/032217_Olfaction_Pilot/*qseq.txt.gz; do ln -s $f $(basename $f); done
# rename -v 's/s_1_([1-2])_([0-9]*).*/$2_$1.qseq.gz/' qseqs/*.gz > rename.err
