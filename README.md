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

How to deploy
How to configure
How to arrange input data

accepts quality-filtered FASTQ data

How to run on a single machine
How to run on a cluster
