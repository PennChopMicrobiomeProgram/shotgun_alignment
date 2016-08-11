import itertools

# SAMMIN files: Minimized SAM format

def parse_sammin(f):
    for line in f:
        vals = line.split("\t")
        # ReadID, RefID
        yield (vals[0], vals[1])

def group_refids(alignments):
    groups = itertools.groupby(alignments, lambda x: x[0])
    for read_id, items in groups:
        ref_ids = set([x[1] for x in items])
        yield read_id, ref_ids
