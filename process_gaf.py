#!/usr/bin/env python3

"""Process the PHI-base GO Annotation File.

This script processes the PHI-base GO Annotation File (GAF) to be compliant
with the checks done by the GO Annotation Database. Specifically, it removes
annotation extensions that are used only by PHI-base and transfers the
information captured by the extensions to other columns in the GAF.
"""

__author__ = "James Seager"
__email__ = "james.seager@rothamsted.ac.uk"
__license__ = "GNU GPLv3"
__version__ = "1.0.1"

import csv
import re


def read_gaf_file(path):
    def read_header_lines(gaf_file):
        header_lines = []
        last_pos = gaf_file.tell()
        line = gaf_file.readline()
        while line.startswith('!'):
            header_lines.append(line)
            last_pos = gaf_file.tell()
            line = gaf_file.readline()
        # Seek to previous line to not skip the first row on the next read
        gaf_file.seek(last_pos)
        return (header_lines, gaf_file)

    rows = []
    with open(path) as gaf_file:
        header_lines, gaf_file = read_header_lines(gaf_file)
        reader = csv.DictReader(gaf_file, fields, dialect='gaf')
        for row in reader:
            rows.append(row)
    return (header_lines, rows)


def process_gaf_data(gaf_data):
    taxon_template = 'taxon:{}'
    pattern = re.compile(r'with_(?:host|symbiont)_species\((\d+?)\),?')
    header_lines, rows = gaf_data
    for row in rows:
        taxon = row['taxon']
        extension = row['annotation_extension']
        if not extension:
            continue
        matches = pattern.findall(extension)
        if not matches:
            continue
        assert len(matches) == 1
        assert '|' not in taxon
        with_taxon = matches[0]
        assert with_taxon not in taxon
        with_taxon_id = taxon_template.format(with_taxon)
        row['taxon'] = '|'.join((taxon, with_taxon_id))
        row['annotation_extension'] = pattern.sub('', extension)
    return (header_lines, rows)


def write_gaf_file(path, header_lines, rows):
    with open(path, 'w+') as gaf_file:
        gaf_file.writelines(header_lines)
        writer = csv.DictWriter(gaf_file, fields, dialect='gaf')
        writer.writerows(rows)


def process_gaf_file(in_path, out_path):
    gaf_data = read_gaf_file(in_path)
    gaf_data = process_gaf_data(gaf_data)
    header_lines, rows = gaf_data
    write_gaf_file(out_path, header_lines, rows)


fields = [
    'db',
    'db_object_id',
    'db_object_symbol',
    'qualifier',
    'go_id',
    'db_reference',
    'evidence_code',
    'with_from',
    'aspect',
    'db_object_name',
    'db_object_synonym',
    'db_object_type',
    'taxon',
    'date',
    'assigned_by',
    'annotation_extension',
    'gene_product_form_id',
]

if __name__ == '__main__':
    def get_arg_parser():
        import argparse

        description = (
            'Process the PHI-base GAF file to ensure it passes the checks done '
            'by the GO Annotation Database.'
        )
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument(
            'input',
            metavar='GAF_FILE',
            type=str,
            help='the path to the PHI-base GAF file.'
        )
        parser.add_argument(
            '-o', '--output',
            metavar='OUT_FILE',
            type=str,
            help=(
                'the path to write the processed PHI-base GAF file. If not '
                'specified, the input file will be overwritten.'
            )
        )
        return parser

    parser = get_arg_parser()
    args = parser.parse_args()
    # Overwrite input file if no output file is specified
    out_path = args.output or args.input
    csv.register_dialect('gaf', delimiter='\t', lineterminator='\n', quoting=csv.QUOTE_NONE)
    process_gaf_file(args.input, out_path)
