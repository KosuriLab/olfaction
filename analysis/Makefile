#===============================================================================
SHELL := /bin/bash

# PATHS
DATA := data
SCRIPTS := ../scripts

THREADS := 12

#===============================================================================

# RECIPIES

clean:
	rm -f pipeline/*

.PRECIOUS: $(addprefix pipeline/, %.map.csv %.merge.fastq %.filter.fastq)

#===============================================================================
# FIGURE OUT HOW TO MAKE THE DEPS NICE
# maybe 2 files of all qseqs?
pipeline/pilot-1_idx-bcs.txt.gz:
	parallel -j$(THREADS) --xapply bash $(SCRIPTS)/qseq2txt.sh {1} {2} ::: data/pilot-1/s_2_1_*.gz ::: data/pilot-1/s_2_2_*.gz | \
	    awk '{print $$1, substr($$2, 1, 15)}' | \
	    pigz -c -p20 > $@

pipeline/pilot-2_idx-bcs.txt.gz:
	parallel -j$(THREADS) --xapply bash $(SCRIPTS)/qseq2txt.sh {1} {2} ::: data/pilot-2/s_1_1_*.gz ::: data/pilot-2/s_1_2_*.gz | \
	    awk '{print $$1, substr($$2, 1, 15)}' | \
	    pigz -c -p20 > $@

pipeline/pilot-2_96-well_idx-bcs.txt.gz:
	parallel -j$(THREADS) --xapply bash $(SCRIPTS)/qseq2txt.sh {1} {2} ::: data/pilot-2_96-well/s_1_1_*.gz ::: data/pilot-2_96-well/s_1_2_*.gz | \
	    awk '{print $$1, substr($$2, 1, 15)}' | \
	    pigz -c -p20 > $@
#-------------------------------------------------------------------------------

# count all indexes
output/idx-counts.txt: pipeline/pilot-1_idx-bcs.txt.gz pipeline/pilot-2_idx-bcs.txt.gz
	zcat $^ | \
	    awk '{a[$$1]++} END {for(idx in a) print idx, a[idx]}' | \
	    sort -rnk2 > $@

# filter reads to only be in the correct index
# then count all barcodes associated with it
output/idx-bcs-counts.txt: raw-indexes.txt pipeline/pilot-1_idx-bcs.txt.gz pipeline/pilot-2_idx-bcs.txt.gz
	parallel zcat $(filter-out $<, $^) \| awk -v idx=\"{}\" \''$$1 == idx {a[$$2]++} END {for(bc in a) print idx, bc, a[bc]}'\' :::: $< > $@

#-------------------------------------------------------------------------------
# 96-well stuff

# count all indexes
output/96-well_idx-counts.txt: pipeline/pilot-2_96-well_idx-bcs.txt.gz
	zcat $^ | \
	    awk '{a[$$1]++} END {for(idx in a) print idx, a[idx]}' | \
	    sort -rnk2 > $@

# filter reads to only be in the correct index
# then count all barcodes associated with it
output/96-well_idx-bcs-counts.txt: 96-well-indexes.txt pipeline/pilot-2_96-well_idx-bcs.txt.gz
	parallel zcat $(filter-out $<, $^) \| awk -v idx=\"{}\" \''$$1 == idx {a[$$2]++} END {for(bc in a) print idx, bc, a[bc]}'\' :::: $< > $@

