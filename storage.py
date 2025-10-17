import pandas as pd
import sqlite3

def store_data(data, csv_file="scraped_data.csv", db_file="scraper.db"):
    if not data:
        print("No data to store!")
        return

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)
    print(f"✅ Data saved to CSV file: {csv_file}")

    # Save to SQLite
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Dynamically create table columns based on data keys
    columns = ", ".join([f"{key} TEXT" for key in data[0].keys()])
    c.execute(f"CREATE TABLE IF NOT EXISTS headlines ({columns})")

    placeholders = ", ".join(["?" for _ in data[0].keys()])
    for item in data:
        c.execute(f"INSERT INTO headlines VALUES ({placeholders})", tuple(item.values()))

    conn.commit()
    conn.close()
    print(f"✅ Data saved to SQLite database: {db_file}")
