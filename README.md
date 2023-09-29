# taxon-search

## Expand the species search functionality for Ensembl beta website

The search engine of any website can be one of the most useful tools for users to help them easily retrieve the information they are looking for. Currently, Ensembl’s search tool works based on indexed fields of their databases, that mainly covers key information, e.g. genes, species, proteins, including several synonyms for most of them. Ensembl would like to extend their new [beta website](https://beta.ensembl.org) search engine capabilities so users can have an even better experience.

We want to expand Ensembl beta website’s search functionality to include and support searching based on taxonomic information. In particular:
1. Be able to find a species already present in Ensembl by searching by its scientific name or taxonomy (homotypic) synonym
2. Be able to search for taxonomy clades and obtain the list of species available within such clade
3. Return close relatives when the previous searches did not find any matches, i.e. if the term introduced is present in the taxonomic tree but no species are found in Ensembl, close-relative species available will be returned instead

The objective of this project is to provide a standalone Elasticsearch tool that can handle taxonomic-related requests.

## Installation and setup

Before you go ahead make sure you have [Python 3.10](https://www.python.org/downloads/) or higher version installed and activated in your system.

1. Install Python dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

2. Define the environment variables in `config/env_vars`, e.g. you can add the connection URL for your [Bonsai Elasticsearch cluster](https://bonsai.io/), and then activate those environment variables:
    ```bash
    export $(xargs < config/env_vars)
    ```

3. Run scripts to download the Ensembl metadata and NCBI taxonomy data into JSON files (as Django fixtures).
    ```bash
    python3 scripts/get_ensembl_metadata.py
    python3 scripts/get_taxon_flat.py
    ```

4. Move into the source directory and run Django model migrations:
    ```bash
    cd src
    python3 manage.py migrate
    ```

5. Load the previously downloaded fixtures into Django models:
    ```bash
    python3 manage.py loaddata ensembl_metadata.json
    python3 manage.py loaddata ncbi_taxon_flat.json
    ```

6. Setup the Elasticsearch cluster and update settings if required. The current app is configured to use [Bonsai](https://bonsai.io/) as seen in step 2.

7. Index documents into Elasticsearch:
    ```bash
    python3 manage.py search_index --rebuild
    ```

8. Start Elasticsearch server:
    ```bash
    python3 manage.py runserver
    ```

9. Open the localhost url (http://127.0.0.1:8000/) in your browser to access the search taxonomy page.

## Additional information


### Taxonomy Name classes in the scope
- `scientific name`, `synonym` and `equivalent name` (contains informal synonyms of formal scientific names) will be the primary focus during the initial stage of the project.
- We might want to also consider `misspelling` and `misnomer`, but only in the later stages (after above ones are completed). The same applies to `anamorph` and `teleomorph`, since these two are only applicable to Fungi.
- It seems `acronym` is primarily used for the viruses, so not applicable to Ensembl for the time being.


### How to install and setup an Elasticsearch server locally

Before you go ahead make sure you have [docker](https://docker.com/) installed and available in your system. The steps below are required only for the initial setup. To re-run an existing docker container, run `docker start my_es_server` and enter the previously saved password if prompted.

1. Create the elasticsearch server:
    ```bash
    docker network create elastic
    ```

2. Start the server and print the password (make a note of it, it will be printed only on the first run!):
    ```bash
    docker run --name my_es_server --net elastic -p 9200:9200 -p 9300:9300 \
        -e "discovery.type=single-node" \
        -t docker.elastic.co/elasticsearch/elasticsearch:8.8.0
    ```


### Testing Taxonomy Search Results

1. Get exact match of existing species (including synonyms):
    - _Ixodes scapularis_ should return _Ixodes scapularis_, _Ixodes scapularis_ ISE6 and _Ixodes scapularis_ PalLabHiFi
    - _Metaseiulus occidentalis_ should return _Galendromus occidentalis_
    - _Apis terrestris_ should return _Bombus terrestris_
2. Get species given the taxonomy clade:
    - _Culicinae_ should return _Aedes aegypti_, _Aedes albopictus_, _Culex quinquefasciatus_ and _Culex quinquefasciatus_ JHB
    - _Triatominae_ should return _Rhodnius prolixus_
    - _Hemichordata_ should return _Saccoglossus kowalevskii_
3. Get closest relatives when the search term is not part of Ensembl:
    - _Seisonidae_ should return _Adineta vaga_ (first common ancestor: Rotifera)
    - _Cenolia_ should return _Anneisia japonica_ (first common ancestor: Comatulinae)
    - _Culex maxi_ should return _Culex quinuefasciatus_ and _Culex quinquefasciatus_ JHB (first common ancestor: Culex)


### Useful commands

- Increase VM memory limit (on Windows WSL)
    ```bash
    sudo sysctl -w vm.max_map_count=262144
    ```
- See/query environment variables
    ```bash
    printenv <env-var-name>
    ```
- To query the database using Django models
    ```bash
    python3 manage.py dbshell
    ```
- Make Django migrations
    ```bash
    python3 manage.py makemigrations
    ```
- Apply Django migrations
    ```bash
    python3 manage.py migrate
    ```

