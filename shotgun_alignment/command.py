import argparse
import collections
import sys

from shotgun_alignment.ncbi_taxonomy import (
    read_nodes_dmp, read_names_dmp, standardize_lineage,
)
from shotgun_alignment.algorithm import reduce_taxa
from shotgun_alignment.misc import parse_taxa_cts, parse_lca_cts


def replace_falsy(x, replacement="NA"):
    if x:
        return x
    else:
        return replacement


def standardize_taxa_main(argv=None):
    p = argparse.ArgumentParser(argv)
    p.add_argument("taxonomy_dir")
    args = p.parse_args(argv)

    ncbi_parents = read_nodes_dmp(args.taxonomy_dir + "/nodes.dmp")
    ncbi_names = read_names_dmp(args.taxonomy_dir + "/names.dmp")
    standard_lineage_cts = collections.defaultdict(int) 
    for name, taxon_id, cts in parse_lca_cts(sys.stdin):
        standard_lineage = standardize_lineage(
            taxon_id, ncbi_parents, ncbi_names)
        standard_lineage_cts[standard_lineage] += cts
    for standard_lineage, cts in sorted(standard_lineage_cts.items()):
        lineage_str = "\t".join(replace_falsy(x) for x in standard_lineage)
        sys.stdout.write("{0}\t{1}\n".format(cts, lineage_str))


def apply_lca_main(argv=None):
    p = argparse.ArgumentParser(argv)
    p.add_argument("taxonomy_dir")
    args = p.parse_args(argv)

    ncbi_parents = read_nodes_dmp(args.taxonomy_dir + "/nodes.dmp")
    ncbi_names = read_names_dmp(args.taxonomy_dir + "/names.dmp")
    taxon_counts = collections.defaultdict(int)
    for cts, taxa in parse_taxa_cts(sys.stdin):
        taxon = reduce_taxa(taxa, ncbi_parents)
        taxon_counts[taxon] += cts
    for taxon, counts in taxon_counts.items():
        name = ncbi_names[taxon]
        sys.stdout.write("\t".join(map(str, (name, taxon, counts))))
        sys.stdout.write("\n")


from shotgun_alignment.sam import parse_sammin, group_taxids
from shotgun_alignment.ncbi_refseq import parse_assembly_summary


def resolve_taxa_main(argv=None):
    p = argparse.ArgumentParser(argv)
    p.add_argument("assembly_summary_file", type=argparse.FileType("r"))
    args = p.parse_args(argv)

    tax_ids = dict(parse_assembly_summary(args.assembly_summary_file))

    for read_id, assembly_ids in group_taxids(parse_sammin(sys.stdin)):
        read_tax_ids = [tax_ids[a] for a in assembly_ids]
        sys.stdout.write(read_id)
        sys.stdout.write("\t")
        sys.stdout.write("\t".join(read_tax_ids))
        sys.stdout.write("\n")
