# Identifier

This is a generic snakemake workflow for integrated similarity search and phylogenetic inference. From a set of query sequences, it runs blastn against custom databases to get closest reference sequences. Subsets of the closest hits for each query are then retrieved and aligned for a phylogenetic reconstructions.

## Instalation

To make the pipeline available, clone the github repo, and create a conda environment from the environment file available:

    git clone link
    cd link
    mamba create -f envs/blast_app_env.yml

## Usage

To run the pipeline, simply activate the environment and run the identifier.py script. It requires multiple command line arguments:

* input: Path for an input fasta file (query sequences).
* database: Path for a fasta database file (reference sequences).
* config-file: Name of the output config file.
* output: Path for the output directory.
* threads: Number of threads for individual jobs.
* threads_total: Total number of threads available for processing.

Example usage:

    python scripts/identifier.py --input data/example.fasta --database resources/references.fasta --config-file /config/config.yml --output /Users/user/Desktop/output --threads 2 --threads-total 4

This leads to the execution of the complete workflow, which comprehends the creation of blastn database, similarity search, parsing of blast output files, alignments and phylogenetic analysis. 

## Comments

Future developments include:
  * Support for additional CLI options (examples: e-value/identity filters).
  * A script for automatic closest phylogenetic match identification.
  * An interface for generating figures / html reports.

## Citations

If you used this pipeline, cite this GitHub repository, as well the core dependencies:
* <a href="https://academic.oup.com/mbe/article/30/4/772/1073398">MAFFT</a>
* <a href="https://academic.oup.com/mbe/article/37/5/1530/5721363">IQ-Tree</a>



