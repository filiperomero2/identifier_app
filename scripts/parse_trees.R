#!/usr/bin/env Rscript

# Load libraries
library(ape)
library(phytools)
library(stringr)
library(ggtree)


# Parse command line args
args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args) != 2) {
  stop("Exactly two positional arguments must be supplied:
  1 - path for blast output file.
  2 - path for the directory containing trees.\n",
  call.=FALSE)
}

# Get blast file path
blast_results <- args[1]

# Get tree files path
tree_files <- list.files(path = args[2],
                         pattern = ".treefile$")

parse_blast_results_from_phylogeny <- function(blast_results,tree_files){
  
  #Read blast table
  df <- read.table(file = blast_results,header=T,as.is=T)
  
  # Open results data frame
  results <- data.frame(matrix(nrow = 1,ncol = ncol(df)))
  names(results) <- names(df)
  
  for( i in 1:length(tree_files) ){
    
    my_tree <- paste(args[2],tree_files[i],sep="/")
    
    # Read and reroot tree
    tree <- read.tree(file = my_tree)
    tree <- midpoint_root(tree = tree)
    
    # prototype species id
    id <- grep(pattern = "_QUERY$",x = tree$tip.label)
    query <- tree$tip.label[id]
    id_ancestral <- which(tree$edge[,2] == id)
    ancestral_node <- tree$edge[id_ancestral,id]
    descendants <- tree$tip.label[getDescendants(tree = tree,node = ancestral_node)]
    closest_descendants <- setdiff(descendants,query)
    
    # merge with blast info
    clean_query <- str_remove(string = query,pattern = "_QUERY")
    id <- which(df$qseqid == clean_query & df$sseqid == closest_descendants)
    sub_df <- df[id,]
    results <- rbind(results,sub_df)
    
    # Plot tree
    plot_tree(tree,my_tree)
    
  }
  
  results <- results[-1,]

  # Write file
  partial_path <- str_replace(string = args[1],
                              "blast_results/.+",
                              replacement = "blast_results/")
  output_path <- paste(partial_path,
                       "blast_results_closest_phylo_references.tsv",
                       sep="")
  write.table(x = results,file = output_path,
              sep="\t",quote = F,row.names = F)
}

plot_tree <- function(tree,treefile_name){
  
  my_query <- tree$tip.label[grep(pattern = "_QUERY$",x = tree$tip.label)]
  my_putative <- tree$tip.label[grep(pattern = "_PUTATIVE$",x = tree$tip.label)]
  number_of_putative <- length(my_putative)
  
  if( number_of_putative == 0){
    others <- setdiff(tree$tip.label,my_query)
    tip <- c(my_query,others)
    type <- c("query",rep("other",length(others)))
    annotation <- data.frame(tip,type)
    my_tree <- ggtree(tree) + 
      geom_nodelab(hjust = -0.5,size=3) +
      geom_rootedge(rootedge = 0.01) +
      geom_treescale(y = -1)
    
    my_tree %<+% annotation + 
      geom_tiplab(aes(color = type),
                  linesize = 0.3,
                  size=3,
                  align = T) +
      scale_color_manual(values = c("black","#F24405")) +
      hexpand(1) +
      theme(legend.position = "none")
    
  }else{
    others <- setdiff(tree$tip.label,c(my_query,my_putative))
    tip <- c(my_query,my_putative,others)
    type <- c("query",
              rep("putative",length(my_putative)),
              rep("other",length(others)))
    annotation <- data.frame(tip,type)
    my_tree <- ggtree(tree) + 
      geom_nodelab(hjust = -0.5,size=3) +
      geom_rootedge(rootedge = 0.01) +
      geom_treescale(y = -1)
    
    my_tree %<+% annotation + 
      geom_tiplab(aes(color = type),
                  linesize = 0.3,
                  size=3,
                  align = T) +
      scale_color_manual(values = c("black","#22BABB","#F24405")) +
      hexpand(1) +
      theme(legend.position = "none")
  }
  
  treefile_name_2 <- paste(treefile_name,".png",sep="")
  ggsave(treefile_name_2,device = "png",dpi = 300)
  
}

parse_blast_results_from_phylogeny(blast_results = blast_results,
                                   tree_files = tree_files)
