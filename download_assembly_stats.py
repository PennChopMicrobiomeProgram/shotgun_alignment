import itertools
import sys
import urllib.request

def parse_full_assembly_summary(f):
    next(f) # First line is a comment, skip
    keys = next(f).lstrip("# ").rstrip().split()
    for line in f:
        vals = line.rstrip().split("\t")
        yield dict(zip(keys, vals))


def base_url(assembly):
    long_id = assembly["ftp_path"].split("/")[-1]
    return "{0}/{1}".format(assembly["ftp_path"], long_id)


def parse_assembly_stats(f):
    retval = {}
    for line in f:
        line = line.decode("utf-8")
        if line.startswith("all"):
            toks = line.rstrip().split("\t")
            key = toks[4].replace("-", "_")
            val = toks[5]
            retval[key] = val
    return retval

STATS_KEYS = [
    'contig_count', 'contig_N50', 'molecule_count', 'total_length',
    'total_gap_length', 'top_level_count', 'unspanned_gaps', 'region_count',
    'spanned_gaps']

def main(argv=None):
    header_keys = None
    for assembly in parse_full_assembly_summary(sys.stdin):

        # Get url for assembly stats
        stats_url = base_url(assembly) + "_assembly_stats.txt"

        sys.stderr.write("{0}\t{1}\n".format(
            assembly["assembly_accession"],
            assembly["organism_name"]))
        
        # Download assembly stats
        stats_resp = urllib.request.urlopen(stats_url)

        # Parse assembly stats
        stats = parse_assembly_stats(stats_resp)

        sys.stderr.write("{0}\n".format(stats))
        
        # Arrange assembly data for output
        # Write header line if none is present
        if header_keys is None:
            header_keys = list(sorted(assembly.keys())) + STATS_KEYS
            sys.stdout.write("\t".join(header_keys))
            sys.stdout.write("\n")

        # Write values
        output_data = assembly.copy()
        output_data.update(stats)
        output_vals = [output_data.get(k, "NA") for k in header_keys]
        sys.stderr.write("{0}\n".format(output_vals))
        sys.stdout.write("\t".join(output_vals))
        sys.stdout.write("\n")


main()
