import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("dataset/IDS_ALLCountries_Data.csv", encoding='latin1')

print(df.head())

print("\nNull Values:\n")
print(df.isnull().sum())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

df = df.drop(columns=[
    'Country Code',
    'Counterpart-Area Name',
    'Counterpart-Area Code',
    'Series Code'
])

print("\nRemaining Columns:")
print(df.columns)

df_long = df.melt(
    id_vars=['Country Name', 'Series Name'],
    var_name='Year',
    value_name='Debt'
)

print("\nLong Format Data:\n")
print(df_long.head())
print("\nNull Values in Long Format:\n")
print(df_long.isnull().sum())
df_long = df_long.dropna()
print("\nNull Values After Cleaning:\n")
print(df_long.isnull().sum())
df_long.columns = [
    'country_name',
    'indicator_name',
    'year',
    'debt'
]

print(df_long.head())

df_long['debt'] = pd.to_numeric(df_long['debt'], errors='coerce')

df_long = df_long.dropna()

df_long = df_long.drop_duplicates()

print("\nFinal Shape:")
print(df_long.shape)
df_long.to_csv("cleaned_debt_data.csv", index=False)

print("Cleaned dataset saved successfully!")
country_meta = pd.read_csv("dataset/IDS_CountryMetaData.csv", encoding="latin1")

print("\nCountry Metadata Null Values:\n")
print(country_meta.isnull().sum())

country_meta_clean = country_meta[
    ['Table Name', 'Region', 'Income Group', 'Lending category']
]

country_meta_clean = country_meta_clean.dropna()

country_meta_clean = country_meta_clean.rename(columns={
    'Table Name': 'country_name',
    'Region': 'region',
    'Income Group': 'income_group',
    'Lending category': 'lending_category'
})

df_final = pd.merge(
    df_long,
    country_meta_clean,
    on='country_name',
    how='left'
)

print("\nFinal Merged Dataset Null Values:\n")
print(df_final.isnull().sum())

df_final = df_final.dropna()

print("\nNull Values After Final Cleaning:\n")
print(df_final.isnull().sum())

df_final.to_csv("final_debt_data_with_metadata.csv", index=False)

print("Final metadata merged dataset saved successfully!")
print(df_long.head())

print("\nTotal Global Debt:")
print(df_long['debt'].sum())

top_countries = df_long.groupby('country_name')['debt'].sum().sort_values(ascending=False).head(10)

print("\nTop 10 Countries by Debt:\n")
print(top_countries)

low_countries = df_long.groupby('country_name')['debt'].sum().sort_values().head(10)

print("\nLowest 10 Countries by Debt:\n")
print(low_countries)

top_indicators = df_long.groupby('indicator_name')['debt'].sum().sort_values(ascending=False).head(10)

print("\nTop Indicators:\n")
print(top_indicators)
plt.figure(figsize=(12,6))

sns.barplot(
    x=top_countries.values,
    y=top_countries.index
)

plt.title("Top 10 Countries by Debt")
plt.xlabel("Debt")
plt.ylabel("Country")

plt.savefig("top10_countries_debt.png")
plt.show()
plt.figure(figsize=(12,6))

sns.barplot(
    x=top_indicators.values,
    y=top_indicators.index
)

plt.title("Top Debt Indicators")
plt.xlabel("Debt")
plt.ylabel("Indicator")

plt.savefig("top_indicators.png")

plt.show()
plt.figure(figsize=(12,6))

sns.barplot(
    x=top_indicators.values,
    y=top_indicators.index
)

plt.title("Top Debt Indicators")
plt.xlabel("Debt")
plt.ylabel("Indicator")

plt.savefig("top_indicators.png")

print("Top indicators chart saved")

plt.show()
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hannahjona@22",
    database="international_debt"
)

cursor = conn.cursor()

sql = """
INSERT INTO debt_data(country_name, indicator_name, year, debt)
VALUES (%s, %s, %s, %s)
"""

data = list(
    df_long[
        ['country_name', 'indicator_name', 'year', 'debt']
    ].itertuples(index=False, name=None)
)

chunk_size = 10000

for i in range(0, len(data), chunk_size):
    chunk = data[i:i + chunk_size]

    cursor.executemany(sql, chunk)
    conn.commit()

    print(f"{i + len(chunk)} rows inserted")

print("Data inserted successfully into MySQL!")