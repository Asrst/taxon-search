# taxon-search


##### Expand the species search functionality for ensembl beta website

The search engine of any website can be one of the most useful tools for users to help them easily retrieve the information they are looking for. Currently, Ensembl’s search tool works based on indexed fields of our databases, that mainly covers key information, e.g. genes, species, proteins, including many synonyms for every one of them. As we plan to move to our new beta website by the end of 2023, we want to make our search engine even better so our users can enjoy the experience of using Ensembl even more.

We would like to expand our Ensembl beta’s search functionality to include and support searching based on taxonomic information. In particular, we are interested in providing users a list of close relatives when a given species is requested and it is not part of Ensembl (yet), return the list of species available given a taxonomic clade instead of a species name, or find a species even when a (homotypic) synonym is provided instead of its current scientific name. The objective of this project is to create a standalone Elasticsearch tool that can handle taxonomic-related requests.

##### Expected results
- Search tool returns the actual species’ link when the species is in Ensembl, including checking for taxonomy synonyms
- Search tool returns options for close-relatives of introduced species (if any) when the species is not part of Ensembl
- Search tool returns options for species within the given taxonomy clade (if any)



