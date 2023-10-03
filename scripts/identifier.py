#!/usr/env python

"""
This scripts dynamically creates config files and
run the blast/phylo species identifier. 
Filipe Moreira - 2023/10/03
"""

import os
import sys
import argparse
from snakemake import snakemake

def get_args():
    
    parser = argparse.ArgumentParser(
    description='A script to generate config files and run the indetifier workflow',
    usage='''identifier.py [args]''')

    parser.add_argument('--input',
    help='Complete path for the input fasta file (query sequences)',
    required = True)

    parser.add_argument('--database',
    help='Complete path for the database fasta file',
    required = True)

    parser.add_argument('--config-file', type = str, 
    help='Name for the config file (default: config.yml).',
    nargs='?',const=1, default='config.yml')
    
    parser.add_argument('--output', 
    help='Complete path for output directory.',
    required = True)

    parser.add_argument('--target',type = int,
    help="Number of sequences to be included in the phylogenetic analysis (Default = 30).",
    nargs='?',const=1, default=30)

    parser.add_argument('--threads',type = int,
    help='Number of available threads for individual jobs(Default = 1)',
    nargs='?',const=1, default=1)

    parser.add_argument('--threads-total',type = int,
    help='Number of available threads (Default = 1)',
    nargs='?',const=1, default=1)

    args = vars(parser.parse_args())
    return args

def validate_args(args):
    
    if os.path.isfile(args['input']):
        print(f"Input file identified -> {args['input']}")
    else:
        print(f"Input file not identified -> {args['input']}")
        exit()

    if os.path.isfile(args['database']):
        print(f"Database file identified -> {args['database']}")
    else:
        print(f"Database file not identified -> {args['database']}")
        exit()
    
    if(os.path.isfile("config/" + args['config_file'])):
        print("Config file already exists. Please specify a new one.")
        exit()

    if(os.path.isdir(args['output'])):
        print("Output directory already exists. Please specify a new one.")
        exit()

    print("All arguments were succesfully verified.")

    return(args)

def generate_config_file(args):

    with open("config/"+ args['config_file'], 'w') as f:
    
        input = "input_data: " + args['input'] + "\n"
        f.write(input)

        database = "input_fasta_db: " + args['database'] + "\n"
        f.write(database)

        target = "target: " + str(args['target']) + "\n"
        f.write(target)

        threads = "threads: " + str(args['threads']) + "\n"
        f.write(threads)

        output = "output: " + args['output'] + "/\n"
        f.write(output)

        print("The config file was generated. -> config/", args['config_file'])
        
    return

     

def main():
    args = get_args()
    validate_args(args)
    generate_config_file(args)

    target_rule = "all"
    config = "config/" + args['config_file']
    cores = args['threads_total']

    print(config)

    status_1 = snakemake('Snakefile', configfiles=[config], cores=cores,targets=[target_rule])
    status_2 = snakemake('Snakefile', configfiles=[config], cores=cores,targets=[target_rule])

    if status_1 == 0 and status_2 == 0:
        return 0
    else:
        return 1
    

if __name__  == '__main__':
    sys.exit(main())

