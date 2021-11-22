from typing import Dict, List

import sqlite3
from sqlite3 import Connection, Error

import pandas as pd


def create_db(database: str) -> None:
    connection = None
    try:
        connection = sqlite3.connect(database=database)
    except Error as e:
        print(f"ErrorMsg: {e}")
    finally:
        if connection is not None:
            connection.close()
    return None


def get_connection_object(database: str) -> Connection:
    return sqlite3.connect(database=database)


def get_all_records_from_table(
        table_name: str,
        connection_obj: Connection,
    ) -> pd.DataFrame:
    query = f"SELECT * FROM {table_name}"
    cursor_obj = connection_obj.execute(query)
    records = cursor_obj.fetchall()
    columns = list(map(lambda tuple_: tuple_[0], cursor_obj.description))
    df = pd.DataFrame(data=records, columns=columns)
    return df


def get_records_via_query(
        query: str,
        connection_obj: Connection,
    ) -> pd.DataFrame:
    cursor_obj = connection_obj.execute(query)
    records = cursor_obj.fetchall()
    columns = list(map(lambda tuple_: tuple_[0], cursor_obj.description))
    df = pd.DataFrame(data=records, columns=columns)
    return df


def create_table_via_query(
        query: str,
        connection_obj: Connection,
    ) -> None:
    _ = connection_obj.execute(query)
    return None


def list_tables_in_db(connection_obj: Connection) -> List[str]:
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor_obj.fetchall()
    return tables


def read_data_from_csv_file(
        filepath: str,
        expected_columns: List[str],
        separator: str,
    ) -> pd.DataFrame:
    df = pd.read_csv(filepath, sep=separator)
    df = df.loc[:, expected_columns]
    return df


def segregate_by_column(
        data: pd.DataFrame,
        column: str,
    ) -> Dict[str, pd.DataFrame]:
    """
    Returns dictionary having keys = unique value of mentioned column, and
    values = DataFrame segregated by said column.
    """
    dict_obj = {}
    column_values = data[column].dropna().unique().tolist()
    for column_value in column_values:
        dict_obj[column_value] = data[data[column] == column_value].reset_index(drop=True)
    return dict_obj


if __name__ == "__main__":
    """
    1) I would prefer to use a context manager to close the database connection in a production-level codebase.
    2) If you try to populate the database multiple times, it will fail. I have set it to fail for now. I can make sure it appends records in the demo.
    3) I would like to conduct a demo of the code for better clarity.
    """
    
    DATABASE = "thedatabase.db"
    EXPECTED_COLUMNS = ['H', 'Customer_Name', 'Customer_Id', 'Open_Date', 'Last_Consulted_Date', 'Vaccination_Id', 'Dr_Name', 'State', 'Country', 'DOB', 'Is_Active']

    create_db(database=DATABASE)
    connection_obj = get_connection_object(database=DATABASE)

    # # Query to create table
    # create_table_via_query(
    #     query="CREATE TABLE table_something (col1 int, col2 varchar(255), col3 float);",
    #     connection_obj=connection_obj,
    # )

    # # List tables in database
    # tables_in_db = list_tables_in_db(connection_obj=connection_obj)
    # print(f"tables_in_db: {tables_in_db}")

    # Populate the database
    df_customers = read_data_from_csv_file(
        filepath="data.csv",
        expected_columns=EXPECTED_COLUMNS,
        separator='|',
    )
    dict_customers_by_country = segregate_by_column(
        data=df_customers,
        column='Country',
    )
    for country, df_customers_by_country in dict_customers_by_country.items():
        table_name = f"table_{country.strip().lower()}"
        df_customers_by_country.to_sql(
            name=table_name,
            con=connection_obj,
            if_exists='fail', # append
            index=False,
        )
    
    # Fetch records from database
    df_all = get_all_records_from_table(
        table_name='table_ind',
        connection_obj=connection_obj,
    )
    df_subset = get_records_via_query(
        query=f"SELECT * FROM table_ind WHERE Customer_Id <> 7",
        connection_obj=connection_obj
    )
    print(
        f"All:\n{df_all}",
        f"Subset:\n{df_subset}",
        sep="\n\n",
    )
    
    connection_obj.close()