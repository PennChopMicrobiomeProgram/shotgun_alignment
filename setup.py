#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Shotgun Alignment',
    version='0.0.1',
    description='Alignment-based methods for shotgun metagenomics data',
    author='Kyle Bittinger',
    author_email='kylebittinger@gmail.com',
    url='https://github.com/PennChopMicrobiomeProgram/shotgun_alignment',
    packages=['shotgun_alignment'],
    entry_points={'console_scripts': [
        'standardize_taxa = shotgun_alignment.command:standardize_taxa_main',
        'apply_lca = shotgun_alignment.command:apply_lca_main',
        'resolve_taxa = shotgun_alignment.command:resolve_taxa_main',
        'clean_fasta = shotgun_alignment.command:clean_fasta_main',
        'convert_sam = shotgun_alignment.command:convert_sam_main',
        'download_assembly_stats = shotgun_alignment.download:main',
    ]},
)
