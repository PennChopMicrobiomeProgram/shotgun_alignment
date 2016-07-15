from shotgun_alignment.ncbi_taxonomy import get_lineage

def all_equal(xs):
    assert len(xs) > 0
    return xs.count(xs[0]) == len(xs)

def lca(lineages):
    ancestor = None
    for ancestral_taxa in zip(*lineages):
        if all_equal(ancestral_taxa):
            ancestor = ancestral_taxa[0]
        else:
            break
    return ancestor

def reduce_taxa(taxa, parents):
    if len(taxa) == 1:
        return taxa[0]
    else:
        lineages = [get_lineage(t, parents) for t in taxa]
        return lca(lineages)

