b <- read.delim(
  snakemake@input[[1]],
  skip=1, stringsAsFactors=F,
  na.strings = c("NA", "na", ""))
colnames(b)[[1]] <- "assembly_accession"
b$assembly_level <- factor(
  b$assembly_level,
  levels=c("Complete Genome", "Chromosome", "Scaffold", "Contig"))

reps <- b[!is.na(b$refseq_category),]

b_species <- split(b, b$species_taxid)
has_no_reps <- function (df) all(is.na(df$refseq_category))
b_species_norep <- Filter(has_no_reps, b_species)
reorder_by_assembly_level <- function (df) df[order(df$assembly_level),]
b_species_norep <- lapply(b_species_norep, reorder_by_assembly_level)
b_species_norep_selection <- lapply(b_species_norep, head, n=1)
additional_reps <- do.call(rbind, b_species_norep_selection)

b_reduced <- rbind(reps, additional_reps)

write.table(
    b_reduced, snakemake@output[[1]],
    quote = F, sep="\t", row.names = F)
