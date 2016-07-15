import argparse
import sys

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("assembly_id")
    args = p.parse_args(argv)
    assembly_id = args.assembly_id

    for line in sys.stdin:
        if line.startswith("@"):
            continue
        vals = line.rstrip().split("\t")
        if vals[2] == "*":
            continue
        query_id = vals[0]
        ref_id = vals[2]
        ref_pos = vals[3]
        cigar = vals[5]
        edit_dist = get_edit_dist(vals[11:])
        line_out = "\t".join((
            query_id, assembly_id, ref_id, ref_pos, cigar, edit_dist))
        sys.stdout.write(line_out)
        sys.stdout.write("\n")

def get_edit_dist(vals):
    for val in vals:
        if val.startswith("NM:i:"):
            return val[5:]
    return "NA"

main()
