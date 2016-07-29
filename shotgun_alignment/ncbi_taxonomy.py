import itertools
import sys
import os.path
import pickle
import collections

NcbiNode = collections.namedtuple(
    "NcbiNode", ["taxon", "parent", "rank"])

def parse_names_dmp(f):
    for line in f:
        vals = line.split("\t|\t")
        taxon = vals[0]
        name = vals[1]
        if any(("scientific name" in v) for v in vals):
            yield (taxon, name)

def parse_nodes_dmp(f):
    for line in f:
        vals = line.split("\t|\t")
        taxon = vals[0]
        parent = vals[1]
        rank = vals[2]
        yield (taxon, NcbiNode(taxon, parent, rank))

def read_cached_file(fp, parser, cache_fp=None):
    if cache_fp is None:
        cache_fp = fp + ".pkl"
    if (os.path.exists(cache_fp)):
        with open(cache_fp, "rb") as f:
            res = pickle.load(f)
    else:
        with open(fp) as f:
            res = dict(parser(f))
        with open(cache_fp, "wb") as f:
            pickle.dump(res, f)
    return res


def read_nodes_dmp(fp):
    return read_cached_file(fp, parse_nodes_dmp)


def read_names_dmp(fp):
    return read_cached_file(fp, parse_names_dmp)

standard_ranks = [
    "superkingdom", "kingdom", "phylum", "class",
    "order", "family", "genus", "species",
]


def standardize_lineage(taxon_id, taxa, taxa_names):
    lineage = get_lineage(taxon_id, taxa)
    lineage_nodes = [taxa[taxon_id] for taxon_id in lineage]
    rank_to_taxon_id = dict(
        (node.rank, node.taxon) for node in lineage_nodes)
    rank_to_name = dict(
        (rank, taxa_names[taxon_id]) for rank, taxon_id in rank_to_taxon_id.items())
    return tuple(rank_to_name.get(rank, "") for rank in standard_ranks)


def get_lineage(taxon_id, taxa):
    lineage = [taxon_id]
    for i in range(500):
        taxon = taxa[taxon_id]
        if taxon.parent == taxon_id:
            lineage.reverse()
            return lineage
        else:
            lineage.append(taxon.parent)
            taxon_id = taxon.parent
    raise RuntimeError(
        "Lineage exceeded max.number of taxa: {0}".format(lineage))

def test_get_lineage():
    taxa = {
        "123": NcbiNode("123", "555", None),
        "555": NcbiNode("555", "984", None),
        "0": NcbiNode("0", "0", None),
    }
    assert get_lineage("123", taxa) == ["0", "555", "123"]
