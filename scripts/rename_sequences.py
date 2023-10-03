#!/usr/env python

# Silly script to rename mitochondrion refseq
# Probably there is an easier way to do it
# usage: python reanem_sequences.py input_file_with_dumb_seq_names.fasta output_with_cool_names.fasta

import sys

infile = sys.argv[1]
outfile = sys.argv[2]

data = {}
with open(infile,"r") as f:
    for line in f.readlines():
        line = line.strip()
        if line.startswith(">"):
            # Get and concatenate first three elements on sep by " "
            header = "_".join(line.split(" ",3)[:3])
            print(header)
            data[header] = ""
        else:
            data[header] += line

with open(outfile,"w") as out:
    for key in data.keys():
        out.write(f"{key}\n")
        out.write(f"{data[key]}\n")
