def parse_taxa_cts(f):
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        vals = line.split()
        counts = int(vals[0])
        taxa = vals[1:]
        yield (counts, taxa)
