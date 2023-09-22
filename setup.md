### PROJECT SETUP       

1. Install python dependencies.
    `pip install -r requirements.txt`

2. Define the environment variables. Refer the `.env-sample`, add url & rename the file to `.env`
    `export $(xargs < .env)`

3. Run scripts to download the ensembl metadata & taxonomy data into json files (fixtures).
    `python3 scripts/get_ensembl_metadata.py`
    `python3 scripts/get_taxon_flat.py`

4. Move to source directory `cd src` and Run Django model migrations.
    `python3 manage.py migrate`

5. Load fixtures (taxonflat & ensembl metadata jsons) into django models.
    `python3 manage.py loaddata ensembl_metadata.json`
    `python3 manage.py loaddata ncbi_taxon_flat.json`

6. Setup elastic cluster & update settings if required. The current app is configured to use [bonsai](https://app.bonsai.io/login) free tier. Make sure you update the `BONSAI_URL` env variable in the Step 2.

7. Index documents into elastic search.
    `python3 manage.py search_index --rebuild`

8. Open the localhost url (http://127.0.0.1:8000/) in your browser.