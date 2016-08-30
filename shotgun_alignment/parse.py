import io

def parse_fasta(f):
    f = iter(f)
    desc = next(f).strip()[1:]
    desc = desc.split()[0]
    seq = io.StringIO()
    for line in f:
        line = line.strip()
        if line.startswith(">"):
            yield desc, seq.getvalue()
            desc = line[1:]
            desc = desc.split()[0]
            seq = io.StringIO()
        else:
            seq.write(line.replace(" ", "").replace("U", "T"))
    yield desc, seq.getvalue()
