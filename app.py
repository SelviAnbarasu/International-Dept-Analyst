import streamlit as st
import pandas as pd
import mysql.connector

st.set_page_config(
    page_title="International Debt Analysis",
    layout="wide"
)

st.title("🌍 International Debt Analysis using SQL")
st.write("Select a query and view the result.")
st.sidebar.write("Sidebar Working")
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Hannahjona@22",
    database="international_debt"
)

queries = {

    "1. Total Records": "SELECT COUNT(*) AS total_records FROM debt_data;",

    "2. Distinct Countries": "SELECT DISTINCT country_name FROM debt_data;",

    "3. Total Countries": "SELECT COUNT(DISTINCT country_name) AS total_countries FROM debt_data;",

    "4. Total Indicators": "SELECT COUNT(DISTINCT indicator_name) AS total_indicators FROM debt_data;",

    "5. First 10 Records": "SELECT * FROM debt_data LIMIT 10;",

    "6. Total Global Debt": "SELECT SUM(debt) AS total_global_debt FROM debt_data;",

    "7. Top 10 Countries by Debt": """
    SELECT country_name,
           SUM(debt) AS total_debt
    FROM debt_data
    GROUP BY country_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """,

    "8. Lowest 10 Countries by Debt": """
    SELECT country_name,
           SUM(debt) AS total_debt
    FROM debt_data
    GROUP BY country_name
    ORDER BY total_debt
    LIMIT 10;
    """,

    "9. Top Debt Indicators": """
    SELECT indicator_name,
           SUM(debt) AS total_debt
    FROM debt_data
    GROUP BY indicator_name
    ORDER BY total_debt DESC
    LIMIT 10;
    """,

    "10. Debt By Year": """
    SELECT year,
           SUM(debt) AS yearly_debt
    FROM debt_data
    GROUP BY year
    ORDER BY year;
    """,
    "11. Average Debt": "SELECT AVG(debt) AS average_debt FROM debt_data;",

    "12. Maximum Debt": "SELECT MAX(debt) AS max_debt FROM debt_data;",

    "13. Minimum Debt": "SELECT MIN(debt) AS min_debt FROM debt_data;",

    "14. Total Debt for Benin": """
SELECT SUM(debt) AS Benin_debt
FROM debt_data
WHERE country_name='Benin';
""",

    "15. Total Debt for Tanzania": """
SELECT SUM(debt) AS Tanzania_debt
FROM debt_data
WHERE country_name='Tanzania';
""",

"16. Data for Year 2020": """
SELECT *
FROM debt_data
WHERE year=2020;
""",

"17. Count Records in 2021": """
SELECT COUNT(*) AS total_records_2021
FROM debt_data
WHERE year=2021;
""",

"18. Debt Greater than 1 Billion": """
SELECT *
FROM debt_data
WHERE debt > 1000000000;
""",

"19. Countries Starting with I": """
SELECT DISTINCT country_name
FROM debt_data
WHERE country_name LIKE 'I%';
""",

"20. Indicators Containing External Debt": """
SELECT DISTINCT indicator_name
FROM debt_data
WHERE indicator_name LIKE '%External debt%';
""",

"21. Total Debt by Year": """
SELECT year,
SUM(debt) AS total_debt
FROM debt_data
GROUP BY year;
""",

"22. Average Debt by Year": """
SELECT year,
AVG(debt) AS average_debt
FROM debt_data
GROUP BY year;
""",

"23. Total Debt by Indicator": """
SELECT indicator_name,
SUM(debt) AS total_debt
FROM debt_data
GROUP BY indicator_name;
""",

"24. Count of Indicators by Country": """
SELECT country_name,
COUNT(DISTINCT indicator_name) AS total_indicators
FROM debt_data
GROUP BY country_name;
""",

"25. Top 5 Years by Debt": """
SELECT year,
SUM(debt) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY total_debt DESC
LIMIT 5;
""",

"26. Lowest 5 Years by Debt": """
SELECT year,
SUM(debt) AS total_debt
FROM debt_data
GROUP BY year
ORDER BY total_debt
LIMIT 5;
""",

"27. Total Records by Country": """
SELECT country_name,
COUNT(*) AS total_records
FROM debt_data
GROUP BY country_name;
""",

"28. Debt Records Sorted Descending": """
SELECT *
FROM debt_data
ORDER BY debt DESC;
""",

"29. Top 10 Highest Debt Records": """
SELECT *
FROM debt_data
ORDER BY debt DESC
LIMIT 10;
""",

"30. Top 10 Lowest Debt Records": """
SELECT *
FROM debt_data
ORDER BY debt
LIMIT 10;
"""
}
selected_query = st.sidebar.selectbox(
    "Select SQL Query",
    list(queries.keys())
)
query = queries[selected_query]

df = pd.read_sql(query, conn)

st.subheader(selected_query)

st.dataframe(df)