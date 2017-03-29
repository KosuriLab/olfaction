#===============================================================================
SHELL := /bin/bash

# PATHS
DATA := data
SCRIPTS := ../scripts

#===============================================================================

# RECIPIES

clean:
	rm -f pipeline/*

.PRECIOUS: $(addprefix pipeline/, %.map.csv %.merge.fastq %.filter.fastq)

#===============================================================================
# FIGURE OUT HOW TO MAKE THE DEPS NICE
# maybe 2 files of all qseqs?
data/idx-bcs.txt.gz:
	parallel -j8 --xapply bash $(SCRIPTS)/qseq2txt.sh {1} {2} ::: data/qseqs/s_2_1_*.gz ::: data/qseqs/s_2_2_*.gz | \
	    awk '{print $$1, substr($$2, 1, 15)}' | \
	    pigz -c -p20 > $@

# count all indexes
output/idx-counts.txt: data/idx-bcs.txt.gz
	zcat $< | \
	    awk '{a[$$1]++} END {for(idx in a) print idx, a[idx]}' | \
	    sort -rnk2 > $@

# filter reads to only be in the correct index
# then count all barcodes associated with it
output/idx-bcs-counts.txt: data/idx-bcs.txt.gz raw-indexes.txt
	parallel zcat $< \| awk -v name=\"{}\" \''$$1 == name {a[$$2]++} END {for(bc in a) print name, bc, a[bc]}'\' :::: $(word 2, $^) > $@
