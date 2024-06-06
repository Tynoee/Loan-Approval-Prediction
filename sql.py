import sqlite3
import pandas as pd
import uuid

database_name = "LoanApprovalPrediction.db"  # SQLite database name

def connect():
    return sqlite3.connect(database_name)

def create_tables():
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id TEXT PRIMARY KEY, 
                no_of_dependents INT, 
                income_annum INT, 
                loan_amount INT, 
                loan_term INT, 
                cibil_score INT, 
                residential_assets_value INT, 
                commercial_assets_value INT, 
                luxury_assets_value INT, 
                bank_asset_value INT, 
                education_Not_Graduate INT, 
                self_employed_Yes INT
            )
        """)
        cur.execute("CREATE TABLE IF NOT EXISTS classification_results (client_id INTEGER, prediction TEXT)")
        con.commit()
        
def insert_client(form_data):
    con = connect()
    cur = con.cursor()
    client_id = str(uuid.uuid4())
    
    cur.execute("""
        INSERT INTO clients (
            client_id,
            no_of_dependents, 
            income_annum, 
            loan_amount, 
            loan_term, 
            cibil_score, 
            residential_assets_value, 
            commercial_assets_value, 
            luxury_assets_value, 
            bank_asset_value, 
            education_Not_Graduate, 
            self_employed_Yes
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        client_id,
        form_data[' no_of_dependents'], 
        form_data[' income_annum'], 
        form_data[' loan_amount'], 
        form_data[' loan_term'], 
        form_data[' cibil_score'], 
        form_data[' residential_assets_value'], 
        form_data[' commercial_assets_value'], 
        form_data[' luxury_assets_value'], 
        form_data[' bank_asset_value'], 
        form_data[' education_ Not Graduate'], 
        form_data[' self_employed_ Yes']
    ))
    con.commit()
    con.close()
    return client_id
    
def insert_result(client_id, result):
    con = connect()
    cur = con.cursor()
    cur.execute("INSERT INTO classification_results (client_id, prediction) VALUES (?, ?)", (client_id, result))
    con.commit()
    con.close()
    

def fetch_results():
    con = connect()
    results = pd.read_sql("SELECT * FROM classification_results", con)
    con.close()
    return results


if __name__ == "__main__":
    create_tables()  # Create database tables if they don't exist
