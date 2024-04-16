from flask import Flask, render_template
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)



# Establish a connection to the database
cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=ELECTRONICS;Trusted_Connection=yes;')

@app.route('/')
def index():
    # Query to fetch data for visualization
    query1 = '''
        SELECT gender, COUNT(*) as count
        FROM user_table
        GROUP BY gender
    '''
    df1 = pd.read_sql_query(query1, cnxn)

    # Query to fetch data for visualization
    query2 = '''
        SELECT age_group, COUNT(*) as count
        FROM user_table
        GROUP BY age_group
    '''
    df2 = pd.read_sql_query(query2, cnxn)

    # Query to fetch data for visualization
    query3 = '''
        SELECT social_media_platform, COUNT(*) as count
        FROM user_social_media
        GROUP BY social_media_platform
    '''
    df3 = pd.read_sql_query(query3, cnxn)

    # Query to fetch data for visualization
    query4 = '''
        SELECT time_of_day, COUNT(*) as count
        FROM user_activity
        GROUP BY time_of_day
    '''
    df4 = pd.read_sql_query(query4, cnxn)

    # Query to fetch data for visualization
    query5 = '''
        SELECT u.USER_ATTR, COUNT(*) as user_count
        FROM user_table u
        JOIN connection_table c ON u.USER_ID = c.USER_ID
        GROUP BY u.USER_ATTR
    '''
    df5 = pd.read_sql_query(query5, cnxn)

    # Drop unnecessary columns after the join
    # df5.drop(columns=['column_to_drop_from_joined_table'], inplace=True)  # Replace 'column_to_drop_from_joined_table' with the actual column name

    # Plotting
    plt.figure(figsize=(8, 5))
    plt.bar(df5['USER_ATTR'], df5['user_count'])
    plt.xlabel('User Attribute')
    plt.ylabel('User Count')
    plt.title('User Attribute Distribution')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Convert plot to PNG image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # Pass the plot URL to the HTML template
    return render_template('index.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
