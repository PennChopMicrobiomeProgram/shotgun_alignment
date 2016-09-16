import argparse
import collections
import gzip
import pathlib
import sys

from shotgun_alignment.ncbi_taxonomy import (
    read_nodes_dmp, read_names_dmp, standardize_lineage,
)
from shotgun_alignment.algorithm import reduce_taxa
from shotgun_alignment.misc import parse_taxa_cts, parse_lca_cts
from shotgun_alignment.parse import parse_fasta

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


from shotgun_alignment.sam import parse_sammin, group_refids
from shotgun_alignment.ncbi_refseq import (
    parse_assembly_summary, parse_refid_summary,
    )


def resolve_taxa_main(argv=None):
    p = argparse.ArgumentParser(argv)
    # RefID -> AssemblyID
    p.add_argument("refid_summary_file", type=argparse.FileType("r"))
    # AsemblyID -> TaxonID
    p.add_argument("assembly_summary_file", type=argparse.FileType("r"))
    args = p.parse_args(argv)

    assembly_ids = dict(parse_refid_summary(args.refid_summary_file))
    tax_ids = dict(parse_assembly_summary(args.assembly_summary_file))

    for read_id, read_ref_ids in group_refids(parse_sammin(sys.stdin)):
        read_assembly_ids = [assembly_ids[r] for r in read_ref_ids]
        read_taxon_ids = [tax_ids[a] for a in read_assembly_ids]
        sys.stdout.write(read_id)
        sys.stdout.write("\t")
        sys.stdout.write("\t".join(read_taxon_ids))
        sys.stdout.write("\n")


def clean_fasta_main(argv=None):
    for line in sys.stdin:
        if line.startswith(">"):
            desc = line.split()[0]
            sys.stdout.write(desc)
            sys.stdout.write("\n")
        else:
            sys.stdout.write(line)

def convert_sam_main(argv=None):
    for line in sys.stdin:
        if line.startswith("@"):
            continue
        vals = line.rstrip().split("\t")
        if vals[2] == "*":
            continue
        query_id = vals[0]
        ref_id = vals[2]
        ref_pos = vals[3]
        cigar = vals[5]
        edit_dist = get_edit_dist(vals[11:])
        line_out = "\t".join((
            # Column numbers:
            #      0       1        2      3          4
            query_id, ref_id, ref_pos, cigar, edit_dist))
        sys.stdout.write(line_out)
        sys.stdout.write("\n")

def get_edit_dist(vals):
    for val in vals:
        if val.startswith("NM:i:"):
            return val[5:]
    return "NA"


def map_refids_main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("fasta_dir")
    args = p.parse_args(argv)

    fasta_dir = pathlib.Path(args.fasta_dir)

    fasta_fps = fasta_dir.glob("**/*.fna")
    for fp in fasta_fps:
        assembly_id = fp.name.replace("_genomic.fna", "")
        with fp.open() as f:
            for seq_id, seq in parse_fasta(f):
                sys.stdout.write("{0}\t{1}\n".format(assembly_id, seq_id))

    gzipped_fasta_fps = fasta_dir.glob("**/*.fna.gz")
    for fp in gzipped_fasta_fps:
        assembly_id = fp.name.replace("_genomic.fna.gz", "")
        with gzip.open(str(fp), "rt") as f:
            for seq_id, seq in parse_fasta(f):
                sys.stdout.write("{0}\t{1}\n".format(assembly_id, seq_id))
