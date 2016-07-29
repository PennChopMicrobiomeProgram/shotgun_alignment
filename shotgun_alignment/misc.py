def parse_taxa_cts(f):
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        vals = line.split()
        counts = int(vals[0])
        taxa = vals[1:]
        yield (counts, taxa)

def parse_lca_cts(f):
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        vals = line.split("\t")
        name = vals[0]
        taxon = vals[1]
        counts = int(vals[2])
        yield (name, taxon, counts)

