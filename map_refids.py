import gzip
import argparse
import pathlib
import io
import sys

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


def main(argv=None):
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

if __name__ == "__main__":
    main()
