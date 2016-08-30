Shotgun Metagenomic Assignment
========

This software aligns reads from shotgun metagenomic sequencing
experiments to microbial genomes. It then summarizes the results by
assigning taxa to reads based on the alignments.

Output consists of the taxononomic summary as well as the genomic
alignment data.

We assume that the input data consists of unassembled short reads.  We
also assume that the reads are quality filtered, and that
contaminating sequences from the host or other sources have been
removed.

How to build the deployable package
--------

There are three steps to building a deployable package.  First, we
download data on available genomes.  Then in a second step, we curate
the reference genomes and create a list of what will be included in
the reference set.  Finally, the genomic data is arranged for
deployment.

To begin, we use the snakemake file, `query_available_refdata.snake`.

After the curation is finished, we use the snakemake file
`build_refdata_archive.snake` to build a deployable archive of genomes
and other data sources needed to process the reads.

How to deploy the reference set
---------

We begin by transferring the archive to the target computer and
unzipping.

The index files are prepared from the set of reference genomes using
the snakemake file `index_for_multialign.rules`.  This workflow
partitions the genomes into a small number of reference databases,
given by the configuration variable `split_db`.  It expects the
unzipped reference genomes to be in the directory `assembly_dir` and
will create the index files in the directory `index_dir`.

How to align input reads
---------

We are now ready to align input sequence reads.  For this, we use the
snakemake file `align_with_snap.rules`.  The workflow accepts
quality-filtered FASTQ data, which should be placed in the directory
given by `input_dir`.

