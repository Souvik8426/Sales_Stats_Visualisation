import numpy as np
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ELECTRONICS;Trusted_Connection=yes;')
    cursor = cnxn.cursor()

    #############  QUERY-1:Number of purchases according to years ###############
    query1 = """
                    SELECT YEAR, COUNT(*) AS Purchase_Count
                    FROM PURCHASE
                    GROUP BY YEAR ORDER BY YEAR;
                    """
    # Execute SQL query and read data into DataFrame
    df1 = pd.read_sql_query(query1, cnxn)

    # Set the style of seaborn plots
    sns.set_style("whitegrid")

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='YEAR', y='Purchase_Count', data=df1, palette="viridis")
    plt.title('Purchase Count by Year')
    plt.xlabel('Year')
    plt.ylabel('Purchase Count')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add data labels to the bars
    for index, row in df1.iterrows():
        plt.text(row.name, row['Purchase_Count'] + 0.2, row['Purchase_Count'], ha='center', color='black')

    # Save the plot to a file
    Viz1 = 'static/Purchases_Per_Year.png'
    plt.tight_layout()
    plt.savefig(Viz1)
    plt.close()

    #############  QUERY-2: Number of purchases based on brand ###############
    query2 = """
                SELECT BRAND, COUNT(*) AS Purchase_Count 
                FROM PRODUCT GROUP BY BRAND;
                """
    df2 = pd.read_sql(query2, cnxn)
    
    # Define a custom color palette
    palette = sns.color_palette("muted", len(df2['BRAND']))
    
    plt.figure(figsize=(9 , 5))
    sns.barplot(x='BRAND', y='Purchase_Count', data=df2, palette=palette)
    plt.xlabel('Brand')
    plt.ylabel('Purchase Count')
    plt.title('Number of Purchases Based on Brand')
    plt.xticks(rotation=45)
    plt.legend(loc="best", fontsize=12)
    plt.grid(False)
    
    # Adjust the bottom margin to prevent the x-axis labels from getting cropped
    plt.subplots_adjust(bottom=0.2)
    
    Viz2 = 'static/Brand_Purchases.png'
    plt.savefig(Viz2, dpi=300)
    plt.close()

    #############  QUERY-3: Number of purchases based on item_id ###############
    query3 = """
                    SELECT ITEM_ID, COUNT(*) AS Purchase_Count 
                    FROM PRODUCT GROUP BY ITEM_ID 
                    ORDER BY Purchase_Count DESC;
                    """
    # Execute SQL query and read data into DataFrame
    df3 = pd.read_sql(query3, cnxn)

    # Set the style of seaborn plots
    sns.set_style("whitegrid")

    # Create the plot
    plt.figure(figsize=(12, 8))
    sns.barplot(x='ITEM_ID', y='Purchase_Count', data=df3.head(10), palette="viridis") # Showing only top 10 items for better readability
    plt.title('Top 10 Items by Purchase Count')
    plt.xlabel('Item ID')
    plt.ylabel('Purchase Count')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add data labels to the bars
    for index, row in df3.head(10).iterrows():
        plt.text(row.name, row['Purchase_Count'] + 0.2, row['Purchase_Count'], ha='center', color='black')

    # Save the plot to a file
    Viz3 = 'static/Purchases_Per_ItemID.png'
    plt.tight_layout()
    plt.savefig(Viz3)
    plt.close()

    #############  QUERY-4: Number of purchases based on User Atrribute ###############
    query4 = """
                SELECT USER_ATTR, COUNT(*) AS Purchase_Count 
                FROM USERS GROUP BY USER_ATTR;"""
    df4 = pd.read_sql(query4, cnxn)
    import matplotlib.cm as cm
    colors = cm.rainbow(np.linspace(0, 1, len(df4['USER_ATTR'])))
    plt.figure(figsize=(8, 8))
    plt.pie(df4['Purchase_Count'], labels=df4['USER_ATTR'], autopct='%1.1f%%', startangle=140, colors=colors, shadow=True)
    plt.legend(loc="best", fontsize=12)
    plt.grid(True, linestyle='--', linewidth=1.5, color='gray')
    plt.xlabel('')
    plt.ylabel('Number of Purchases')
    Viz4 = 'static/Purchases_Per_Attributes.png'
    plt.savefig(Viz4, dpi=400)
    plt.close()

    #############  QUERY-5: Number of products with different ratings ###############
    query5 = """
              SELECT RATING, COUNT(*) AS Purchase_Count 
              FROM PRODUCT GROUP BY RATING
              ORDER BY RATING;
              """
    df5 = pd.read_sql(query5, cnxn)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='RATING', y='Purchase_Count', data=df5, palette=sns.color_palette("husl", 5))
    plt.grid(axis='y', color='lightgray')
    plt.xlabel('Rating')
    plt.ylabel('Number of Products')
    plt.title('Product Ratings')
    Viz5 = 'static/Product_Ratings.png'
    plt.savefig(Viz5)
    plt.close()

    #############  QUERY-6: Number of purchases based on Model Attributes ###############
    query6 = """
                SELECT MODEL_ATTR, COUNT(*) AS Purchase_Count 
                FROM PRODUCT GROUP BY MODEL_ATTR 
                ORDER BY Purchase_Count DESC;
                """
    df6 = pd.read_sql(query6, cnxn)

    # Set a modern style using seaborn
    sns.set_style("whitegrid")

    # Create the bar plot
    plt.figure(figsize=(5, 4))
    sns.barplot(x='MODEL_ATTR', y='Purchase_Count', data=df6, palette='viridis')  # Adjust the palette for a modern look
    plt.xlabel('Model Attribute', fontsize=6)
    plt.ylabel('Purchase Count', fontsize=6)
    plt.xticks(rotation=45, ha='right', fontsize=5)
    plt.yticks(fontsize=5)
    plt.tight_layout()

    # Save the plot
    Viz6 = 'static/Products_Based_on_Model_Attribute.png'
    plt.savefig(Viz6, dpi=300)

    #############  QUERY-7: NUMBER OF PURCHASES MADE IN EACH MONTH BASED ON PARTICULAR YEAR ###############
    years = range(1999, 2007)  # Range of years to visualize

    fig, axes = plt.subplots(4, 2, figsize=(8,8))

    for i, year in enumerate(years):
        query7 = f"""SELECT MONTH, COUNT(*) AS Purchase_Count FROM PURCHASE 
                    WHERE YEAR = {year} GROUP BY YEAR, MONTH 
                    ORDER BY MONTH;"""
        df7 = pd.read_sql(query7, cnxn)
        
        # Check if the dataframe is empty
        if not df7.empty:
            row = i // 2
            col = i % 2
            ax = axes[row, col]
            ax.bar(df7['MONTH'], df7['Purchase_Count'])
            ax.set_title(f'Year {year}')
            ax.set_xlabel('Month')
            ax.set_ylabel('Purchase Count')
        else:
            # If dataframe is empty, set a placeholder title
            row = i // 2
            col = i % 2
            ax = axes[row, col]
            ax.set_title(f'Year {year} (No Data)')
            ax.axis('off')  # Turn off axis for empty plots
            
    plt.tight_layout()
    Viz7 = 'static/Monthly_Purchases_By_Year.png'
    plt.savefig(Viz7)
    plt.close()

    #############  QUERY-8: AVERAGE RATING BASED ON BRAND ###############
    query8 = """
                SELECT BRAND, AVG(RATING) AS Avg_Rating 
                FROM PRODUCT GROUP BY BRAND;
                """
    df8 = pd.read_sql(query8, cnxn)
    plt.figure(figsize=(9, 6))
    sns.barplot(x='BRAND', y='Avg_Rating', data=df8)
    plt.xlabel('Brand')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    Viz8 = 'static/AverageRatings_Based_On_Brand.png'
    plt.savefig(Viz8)
    plt.close()

    #############  QUERY-9: Identify the top 3 brands with the highest average rating ###############
    query9 = """
            SELECT *
            FROM (
                SELECT BRAND, AVG(RATING) AS Avg_Rating,
                    ROW_NUMBER() OVER (ORDER BY AVG(RATING) DESC) AS rank
                FROM PRODUCT
                GROUP BY BRAND
            ) AS ranked
            WHERE rank <= 3;
            """
    df9 = pd.read_sql(query9, cnxn)
    plt.figure(figsize=(4, 6))
    plt.bar(df9['BRAND'], df9['Avg_Rating'], color='skyblue')
    plt.xlabel('Brand')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45)
    plt.tight_layout()
    Viz9 = 'static/Top_3_Brands_With_Highest_Avg_Rating.png'
    plt.savefig(Viz9)
    plt.close()

    #############  QUERY-10: IDENTIFYING THE SALES PER YEAR IN QUARTERS ###############
    years = range(1999, 2007)  # Range of years to visualize

    fig, axes = plt.subplots(8, 1, figsize=(9, 16))  # 8 rows, 1 column for vertical arrangement

    for i, year in enumerate(years):
        ax = axes[i]  # Select the axis for the current year
        
        # Query to select data for each year
        query10 = f"""
                SELECT CASE
                        WHEN MONTH IN (1, 2, 3) THEN 'Q1'
                        WHEN MONTH IN (4, 5, 6) THEN 'Q2'
                        WHEN MONTH IN (7, 8, 9) THEN 'Q3'
                        ELSE 'Q4'
                    END AS Quarter,
                    COUNT(*) AS Purchase_Count
                FROM PURCHASE
                WHERE YEAR = {year}
                GROUP BY YEAR, 
                        CASE
                        WHEN MONTH IN (1, 2, 3) THEN 'Q1'
                        WHEN MONTH IN (4, 5, 6) THEN 'Q2'
                        WHEN MONTH IN (7, 8, 9) THEN 'Q3'
                        ELSE 'Q4'
                        END;
                """
        df10 = pd.read_sql(query10, cnxn)
        ax.bar(df10['Quarter'], df10['Purchase_Count'], color='skyblue')
        ax.set_title(f'Year {year}')
        ax.set_xlabel('Quarter')
        ax.set_ylabel('Purchase Count')

    plt.tight_layout()
    Viz10 = 'static/Purchase_Count_By_Quarter.png'
    plt.savefig(Viz10)
    plt.close()


    return render_template('index.html', Viz1='static/Purchases_Per_Year.png',
                           Viz2='static/Brand_Purchases.png',
                           Viz3='static/Purchases_Per_ItemID.png',
                           Viz4='static/Purchases_Per_Attributes.png',
                           Viz5='static/Product_Ratings.png',
                           Viz6='static/Products_Based_on_Model_Attribute.png',
                           Viz7='static/Monthly_Purchases_By_Year.png',
                           Viz8='static/AverageRatings_Based_On_Brand.png',
                           Viz9='static/Top_3_Brands_With_Highest_Avg_Rating.png',
                           Viz10='static/Purchase_Count_By_Quarter.png',
                           )

if __name__ == '__main__':
    app.run(debug=True)