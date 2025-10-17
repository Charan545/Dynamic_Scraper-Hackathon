import pandas as pd
import sqlite3

def store_data(data, csv_file="data.csv", db_file="data.db"):
    # Store in CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    # Store in SQLite
    conn = sqlite3.connect(db_file)
    df.to_sql("articles", conn, if_exists="replace", index=False)
    conn.close()
