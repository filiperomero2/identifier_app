import glob
import datetime

def get_input_fasta_files(path):
    pattern = path + "/" + "top_hits*fasta"
    files = glob.glob(pattern)
    files = [file.split('/')[-1] for file in files]
    return(files)

rule all:
    input:
        config['output'] + "results/top_hits/report.txt",
        expand(config['output'] + "results/top_hits/aln.trim.{query}.treefile",query = get_input_fasta_files(config['output'] + 'results/top_hits/'))
        
rule create_blast_db:
    input:
        config['input_fasta_db']
    output:
        config['input_fasta_db'] + ".ndb"
    shell:
        "makeblastdb -in {input} -dbtype nucl " 
        "-parse_seqids -blastdb_version 5"

rule run_blast:
    input:
        query = config['input_data'],
        db = config['input_fasta_db'],
        dbn = config['input_fasta_db'] + ".ndb"
    output:
        config['output'] + "results/blast_results/blast_results_" + config['input_data'].split("/")[-1] + ".tsv"
    threads: config['threads']
    params:
        path = config['output'] + "results/blast_results/"
    shell:
        """
        blastn -db {input.db} -query {input.query} -num_threads {threads} -outfmt \"6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore\" > {params.path}temp.txt;
        echo \"qseqid\tsseqid\tpident\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\" > {params.path}temp_2.txt;
        cat {params.path}temp_2.txt {params.path}temp.txt > {output};
        rm {params.path}temp.txt; rm {params.path}temp_2.txt        
        """

rule parse_blast_results:
    input:
        blast_results = config['output'] + "results/blast_results/blast_results_" + config['input_data'].split("/")[-1] + ".tsv",
        query = config['input_data'],
        db = config['input_fasta_db']
    output:
        config['output'] + "results/top_hits/report.txt"
    params:
        target = str(config['target']),
        putative = config['putative']
    shell:
        "python scripts/parse_blast_results.py "
        "--input {input.blast_results} "
        "--query {input.query} "
        "--db {input.db} "
        "--putative {params.putative} "
        "--target {params.target} "
        "--output {output}"

rule align:
    input:
        fasta = config['output'] + "results/top_hits/{query}",
        report = config['output'] + "results/top_hits/report.txt"
    output:
        temp(config['output'] + "results/top_hits/aln.{query}")
    threads: config['threads']
    shell:
        "mafft --quiet --thread {threads} {input.fasta} > {output}"

rule trim:
    input:
        config['output'] + "results/top_hits/aln.{query}"
    output:
        config['output'] + "results/top_hits/aln.trim.{query}"
    shell:
        "trimal -in {input} -out {output} -gappyout"

rule infer_tree:
    input:
        config['output'] + "results/top_hits/aln.trim.{query}"
    output:
        config['output'] + "results/top_hits/aln.trim.{query}.treefile"
    threads: config['threads']
    shell:
        "iqtree -s {input} -T {threads} -m HKY+G4 -alrt 1000 --quiet"
