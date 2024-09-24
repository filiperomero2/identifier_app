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

    parser.add_argument('--output', 
    help='Complete path for output file where the closest hits report files will be saved.',
    required = True)

    parser.add_argument('--target',type = int,
    help='Number of hits to be included in fasta file (Default = 30)',
    nargs='?',const=1, default=30)

    args = vars(parser.parse_args())

    if os.path.isfile(args['input']) and os.path.isfile(args['db']):
        return args

def read_database(db,query):
    data = {}
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
    return data

def parse_output(args):
    data = read_database(args['db'],args['query'])
    #df = pd.read_csv(args['input'],header=None,sep="\t")
    df = pd.read_csv(args['input'],sep="\t")
    #queries = list(df[0].unique())
    queries = list(df['qseqid'].unique())

    outdir = '/'.join(args['output'].split('/')[:-1])
    if os.path.isdir(outdir) is False:
        os.mkdir(outdir)

    report = open(args['output'],"w")

    for query in queries:
        #hits = list(df[1][df[0] == query].unique())
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
                    report.write(f"Query: {query}; Hit: {query}\n")
                else:
                    print(f"Hit {hit} NOT available in the reference file...")

    report.close()

def main():
    args = get_args()
    parse_output(args)

if __name__ == '__main__':
    main()
