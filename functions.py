import re
import csv
from io import StringIO
from pathlib import Path


def parse_assembly_summary(f):
    f.readline() # skip garbage line
    header = f.readline().lstrip("# ").rstrip().split('\t')
    return csv.DictReader(f, fieldnames=header, delimiter='\t')


def test_parse_assembly_summary():
    f = StringIO(ASSEMBLY_SUMMARY)
    recs = parse_assembly_summary(f)
    r0 = next(recs)
    assert r0["assembly_accession"] == "GCF_000002945.1"
    assert r0["organism_name"] == "Schizosaccharomyces pombe"
    assert r0["excluded_from_refseq"] == ""
    assert(len(list(recs)) == 3)


def write_genome_urls(f, rows):
    writer = csv.DictWriter(
        f, fieldnames=['assembly_id', 'url'],
        delimiter='\t', lineterminator="\n")
    for row in rows:
        if row.get('ftp_path'):
            assembly_id = get_assembly_id(row['ftp_path'])
            genome_url = get_fna_url(row['ftp_path'])
            writer.writerow(
                {'assembly_id': assembly_id, 'url':genome_url})


def test_write_genome_urls():
    f = StringIO()
    paths = [
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000002945.1_ASM294v2",
    ]
    rows = [{"ftp_path": p} for p in paths]
    write_genome_urls(f, rows)
    assert f.getvalue() == GENOME_URLS


def generate_list(genome_urls_fp):
    if not Path(genome_urls_fp).exists():
        return []
    urls = csv.DictReader(
        open(genome_urls_fp), fieldnames=['assembly_id','url'], delimiter='\t')
    return [r['assembly_id'] for r in urls]


def get_fna_url(ftp_path):
    long_assembly_id = ftp_path.split("/")[-1]
    return "{0}/{1}_genomic.fna.gz".format(ftp_path, long_assembly_id)


def test_get_fna_url():
    observed = get_fna_url(
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000010525.1_ASM1052v1")
    expected = (
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000010525.1_ASM1052v1"
        "/GCF_000010525.1_ASM1052v1_genomic.fna.gz")
    assert observed == expected


GENOME_URLS = """\
GCF_000002945.1_ASM294v2	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000002945.1_ASM294v2/GCF_000002945.1_ASM294v2_genomic.fna.gz
"""


ASSEMBLY_SUMMARY = """\
#   See ftp://ftp.ncbi.nlm.nih.gov/genomes/README_assembly_summary.txt for a description of the columns in this file.
# assembly_accession	bioproject	biosample	wgs_master	refseq_category	taxid	species_taxid	organism_name	infraspecific_name	isolate	version_status	assembly_level	release_type	genome_rep	seq_rel_date	asm_name	submitter	gbrs_paired_asm	paired_asm_comp	ftp_path	excluded_from_refseq
GCF_000002945.1	PRJNA127	SAMEA3138176		representative genome	4896	4896	Schizosaccharomyces pombe	strain=972h-		latest	Chromosome	Major	Full	2007/11/09	ASM294v2		GCA_000002945.2	identical	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000002945.1_ASM294v2	
GCF_000149845.2	PRJNA32667	SAMN02953668	AATM00000000.2	representative genome	402676	4897	Schizosaccharomyces japonicus yFS275	strain=yFS275		latest	Scaffold	Major	Full	2013/08/16	SJ5	Broad Institute	GCA_000149845.2	identical	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000149845.2_SJ5	
GCF_000150505.1	PRJNA264110	SAMN02953709	ABHY00000000.3	representative genome	483514	4899	Schizosaccharomyces octosporus yFS286	strain=yFS286		latest	Scaffold	Major	Full	2013/07/30	SO6	Broad Institute	GCA_000150505.2	identical	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000150505.1_SO6	
GCF_000315895.1	PRJNA188687	SAMEA2272767		representative genome	559304	4920	Millerozyma farinosa CBS 7064	strain=CBS 7064		latest	Chromosome	Major	Full	2011/11/10	ASM31589v1	Genolevures	GCA_000315895.1	identical	ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000315895.1_ASM31589v1	
"""

def test_get_assembly_id():
    observed = get_assembly_id(
        "ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF_000010525.1_ASM1052v1")
    expected = "GCF_000010525.1_ASM1052v1"
    assert observed == expected

