import pandas as pd
import pymysql
from sqlalchemy import create_engine, text as sql_text


pymysql.install_as_MySQLdb()


def get_taxon_metadata(db_connection):
    """
    The function connects with ensembl My sql database
    and runs a sql query to retrieve data needed to load
    into django models as fixtures. 

    Parameters:
    db_connection (sqlalchemy.create_engine): A sqlalchemy engine.

    Returns:
    pandas dataframe (pd.DataFrame): tabluar data.

    """
    
    query = f"""select distinct taxonomy_id ,o.name ,url_name 
                    ,display_name ,scientific_name ,strain
                    from organism o
                    left join genome g
                    on o.organism_id = g.organism_id 
                    left join division d 
                    on g.division_id = d.division_id
                    LEFT JOIN data_release USING (data_release_id)
                    where d.short_name = 'EM'
                    AND is_current = 1
                    """

    org_df = pd.read_sql_query(sql_text(query), db_connection)
    org_df = org_df.sort_values(by=["taxonomy_id"])
    org_df.to_csv("metazoa_metadata.csv", index=False)

    return org_df


if __name__ == "__main__":
    ncbi_engine = create_engine("mysql://anonymous@ensembldb.ensembl.org:3306/ensembl_metadata_109")
    db_conn = ncbi_engine.connect()

    metadata_df = get_taxon_metadata(db_conn)

    # the below code converts the dataframe into json format
    # required by django to load as fixtures.

    pk_col = []
    field_col = ["taxonomy_id", "url_name", "display_name", "scientific_name", "strain"]
    m2_df = metadata_df[pk_col + field_col].drop_duplicates()

    m2_df["model"] = "taxon_search.EnsemblMetadata"
    m2_df["fields"] = m2_df[field_col].to_dict(orient="records")
    json_str = m2_df[["model", "fields"]].to_json(orient="records")

    OUT_FOLDER = f"src/taxon_search/fixtures"
    SAVE_PATH = f"{OUT_FOLDER}/ensembl_metadata.json"
    with open(SAVE_PATH, "w") as outfile:
        outfile.write(json_str)
    print("fixture file saved to {SAVE_PATH}")
