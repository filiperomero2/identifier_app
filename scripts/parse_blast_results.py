#!/usr/env python

# Script for parsing blast table

import os
import pandas as pd
import argparse


def get_args():

    parser = argparse.ArgumentParser(
    description='A script to parse blast results and return fasta files with query and top hits.',
    usage='''parse_blast_results.py [args]''')
 
    parser.add_argument('--input', 
    help='Complete path for the input blast results in tabular format.',
    required = True)

    parser.add_argument('--query', 
    help='Complete path for the query fasta file.',
    required = True)

    parser.add_argument('--db', 
    help='Complete path for the blast db fasta file.',
    required = True)

    parser.add_argument('--putative', 
    help='Complete path for the putative id fasta file.')

    parser.add_argument('--output', 
    help='Complete path for output file where the closest hits report files will be saved.',
    required = True)

    parser.add_argument('--target',type = int,
    help='Number of hits to be included in fasta file (Default = 30)',
    nargs='?',const=1, default=30)

    args = vars(parser.parse_args())

    if args['putative'] == "NA" or os.path.isfile(args['putative']):
        print("Putative state identified.")
    else:
        print("Putative state not identified.")
        exit()

    if os.path.isfile(args['input']) and os.path.isfile(args['db']):
        return args

def read_database(db,query,putative):
    data = {}
    putative_headers = []
    with open(db,"r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith(">"):
                header = line.lstrip(">")
                data[header] = ""
            else:
                data[header] += line
    with open(query,"r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith(">"):
                header = (line.lstrip(">"))
                data[header] = ""
            else:
                data[header] += line
    if putative == "NA":
        return [data, putative_headers]
    with open(putative,"r") as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith(">"):
                header = (line.lstrip(">"))
                putative_headers.append(header)
                data[header] = ""
            else:
                data[header] += line
    return [data, putative_headers]

def parse_output(args):
    [data, putative_headers] = read_database(args['db'],args['query'],args['putative'])
    df = pd.read_csv(args['input'],sep="\t")
    queries = list(df['qseqid'].unique())

    outdir = '/'.join(args['output'].split('/')[:-1])
    if os.path.isdir(outdir) is False:
        os.mkdir(outdir)

    report = open(args['output'],"w")

    for query in queries:
        hits = list(df['sseqid'][df['qseqid'] == query].unique())  
        if len(hits) >= args['target']:
            my_hits = hits[:args['target']]
        else:
            my_hits = hits[:len(hits)]

        outfile_fasta = f"{outdir}/top_hits_{query}.fasta"
        with open(outfile_fasta,"w") as out:
            out.write(f">{query}_QUERY\n{data[query]}\n")
            for hit in my_hits:
                if hit in data.keys():
                    out.write(f">{hit}\n{data[hit]}\n")
                    report.write(f"Query: {query}; Hit: {hit}\n")
                else:
                    print(f"Hit {hit} not available in the reference file...")
            if putative_headers:
                for header in putative_headers:
                    if header in data.keys():
                        out.write(f">{header}_PUTATIVE\n{data[header]}\n")
                        report.write(f"Query: {query}; Putative: {header}\n")
                    else:
                        print(f"Putative {header} not available in the reference file...")
    report.close()

def main():
    args = get_args()
    parse_output(args)

if __name__ == '__main__':
    main()
