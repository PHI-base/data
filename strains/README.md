PHI-Canto strain lists
=======================

This folder contains the pathogen and host strain lists that are used for
curation in the PHI-Canto community annotation tool.

The data has the following columns:

  * **ncbi_taxid**: the [NCBI Taxonomy][1] taxonomic identifier for the species of
    the strain.
  * **scientific_name**: the scientific name of the species of the strain, as it
    appears in PHI-base.
  * **strain**: the primary name of the strain.
  * **synonyms**: any synonyms of the primary strain name, as curated in PHI-base.
  * **cross_references**: cross-references to identifiers from other biological 
    databases or ontologies. This column is primarily used for cross-references to 
    cell lines in host species. Currently, the following types of identifiers are 
    used:
    * Identifiers that start with **CVCL_** are cross-references to [Cellosaurus][2].
    * Identifiers that start with **BTO:** are cross-references to the 
      [Brenda Tissue Ontology][3].
    * Identifiers that start with **WBStrain** are cross-references to [WormBase][4].
    * Identifiers that start with **MGI:** are cross-references to 
      [Mouse Genome Informatics][5].

[1]: https://www.ncbi.nlm.nih.gov/taxonomy
[2]: https://web.expasy.org/cellosaurus/
[3]: https://www.brenda-enzymes.org/ontology.php?ontology_id=3
[4]: https://wormbase.org/
[5]: http://www.informatics.jax.org/
