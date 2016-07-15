import sys
import os.path
import pickle
import collections

NcbiNode = collections.namedtuple(
    "NcbiNode", ["taxon", "parent", "rank"])

def parse_nodes_dmp(f):
    for line in f:
        vals = line.split("\t|\t")
        taxon = vals[0]
        parent = vals[1]
        rank = vals[2]
        yield NcbiNode(taxon, parent, rank)

def read_nodes_dmp(fp, cache_fp):
    if (os.path.exists(cache_fp)):
        with open(cache_fp, "rb") as f:
            taxa = pickle.load(f)
    else:
        with open(fp) as f:
            taxa = dict(
                (x.taxon, x) for x in parse_nodes_dmp(f))
        with open(cache_fp, "wb") as f:
            pickle.dump(taxa, f)
    return taxa

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
