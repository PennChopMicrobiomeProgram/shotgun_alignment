import itertools

def partition_assemblies(assembly_ids, num_groups):
    buckets = dict((x, []) for x in range(num_groups))
    bucket_idx = itertools.cycle(range(num_groups))
    for n, a in zip(bucket_idx, assembly_ids):
        buckets[n].append(a)
    # Convert keys to string
    buckets = dict((str(k), v) for k, v in buckets.items())
    return buckets

def test_partition_assemblies():
    assert partition_assemblies("abcdefg", 3) == {
        "0": ["a", "d", "g"],
        "1": ["b", "e"],
        "2": ["c", "f"],
    }
