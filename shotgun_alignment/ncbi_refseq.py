def parse_refid_summary(f):
    for line in f:
        vals = line.strip().split("\t")
        assembly_id = vals[0]
        ref_id = vals[1]
        yield ref_id, assembly_id


def parse_assembly_summary(f):
    for line in f:
        if line.startswith("#"):
            continue
        vals = line.split("\t")
        assembly_id = vals[0]
        taxon_id = vals[5]
        yield (assembly_id, taxon_id)


def parse_full_assembly_summary(f):
    keys = next(f).lstrip("# ").rstrip().split()
    for line in f:
        vals = line.rstrip().split("\t")
        yield dict(zip(keys, vals))


def get_fna_url(ftp_path):
    long_assembly_id = ftp_path.split("/")[-1]
    return "{0}/{1}_genomic.fna.gz".format(ftp_path, long_assembly_id)


def parse_selected_assemblies(f):
    keys = next(f).rstrip().split("\t")
    for line in f:
        line = line.rstrip()
        if not line:
            continue
        vals = line.split("\t")
        print(list(zip(keys,vals)))
        yield dict(zip(keys, vals))

