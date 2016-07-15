import collections
import sys

from shotgun_alignment.ncbi_taxonomy import read_nodes_dmp
from shotgun_alignment.algorithm import reduce_taxa
from shotgun_alignment.misc import parse_taxa_cts


def apply_lca_main():
    ncbi_parents = read_nodes_dmp("nodes.dmp", "nodes.pkl")
    taxon_counts = collections.defaultdict(int)
    for cts, taxa in parse_taxa_cts(sys.stdin):
        taxon = reduce_taxa(taxa, ncbi_parents)
        taxon_counts[taxon] += cts
    for taxon, counts in taxon_counts.items():
        sys.stdout.write("{0}\t{1}\n".format(taxon, counts))


from shotgun_alignment.sam import parse_sammin, group_taxids
from shotgun_alignment.ncbi_refseq import parse_assembly_summary


def resolve_taxa_main():
    tax_ids = {}
    with open("assembly_summary.txt") as f:
        for assembly_id, tax_id in parse_assembly_summary(f):
            tax_ids[assembly_id] = tax_id
        
    for read_id, assembly_ids in group_taxids(parse_sammin(sys.stdin)):
        read_tax_ids = [tax_ids[a] for a in assembly_ids]
        sys.stdout.write(read_id)
        sys.stdout.write("\t")
        sys.stdout.write("\t".join(read_tax_ids))
        sys.stdout.write("\n")
