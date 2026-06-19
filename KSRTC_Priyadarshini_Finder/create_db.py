import sqlite3
import csv

conn = sqlite3.connect("buses.db")
cursor = conn.cursor()

# Delete old table
cursor.execute("DROP TABLE IF EXISTS buses")

# Create new table
cursor.execute("""
CREATE TABLE buses (
    bus_no TEXT,
    route_name TEXT,
    start_point TEXT,
    end_point TEXT,
    timing TEXT,
    bus_type TEXT,
    stops TEXT
)
""")

# Read CSV and insert rows
with open("palakkad_buses.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    for row in reader:
        cursor.execute("""
        INSERT INTO buses VALUES (?, ?, ?, ?, ?, ?, ?)
        """, row)

conn.commit()
conn.close()

print("Database created successfully!")