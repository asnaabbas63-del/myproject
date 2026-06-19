import pandas as pd

# Read the CSV file
df = pd.read_csv('palakkad_buses.csv')

# Save it as an Excel file
df.to_excel('palakkad_buses.xlsx', index=False)

print("✅ Excel file 'palakkad_buses.xlsx' created successfully!")