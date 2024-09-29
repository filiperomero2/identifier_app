# Identifier

This is a generic snakemake workflow for integrated similarity search and phylogenetic inference. From a set of query sequences, it runs blastn against custom databases to get closest reference sequences. Subsets of the closest hits for each query are then retrieved and aligned for maximum-likelihood phylogenetic reconstructions.

## Instalation

To make the pipeline available, clone the github repo, and create a conda environment from the environment file available:

    git clone https://github.com/filiperomero2/identifier_app.git
    cd identifier_app
    mamba create -n identifier
    mamba activate identifier
    # The following requires setting the bioconda channel
    mamba env update -n identifier envs/blast_app_env.yml

## Usage

To run the pipeline, simply activate the environment and run the identifier.py script. It requires multiple command line arguments:

* input: Path for an input fasta file (query sequences).
* database: Path for a fasta database file (reference sequences).
* putative: Path for a fasta file file with the putative closest sequences.
* config-file: Name of the output config file.
* output: Path for the output directory.
* model: Nucleotide substitution model, as available in IQ-Tree v2.
* support: Statistical support method for phylogenies (alrt or non-parametric bootstrap).
* threads: Number of threads for individual jobs.
* threads_total: Total number of threads available for processing.

Example usage:

    python scripts/identifier.py --input data/example.fasta --database resources/references.fasta --config-file /config/config.yml --output /Users/user/Desktop/output --threads 2 --threads-total 4

This leads to the execution of the complete workflow, which comprehends the creation of blastn database, similarity searches, parsing of blast output files, alignments and phylogenetic analysis. The latest version also generates a filtered blast table, including only the closest phylogenetic matches, and a figure for each tree.

## Comments

Future developments include:
  * Support for additional CLI options;
  * An interface for generating figures / html reports.

## Citations

If you used this pipeline, cite this GitHub repository, as well the core dependencies:
* <a href="https://academic.oup.com/mbe/article/30/4/772/1073398">MAFFT</a>
* <a href="https://academic.oup.com/mbe/article/37/5/1530/5721363">IQ-Tree</a>



