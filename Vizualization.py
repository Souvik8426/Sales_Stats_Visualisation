import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
    cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Database=SM;Trusted_Connection=yes;')
    cursor = cnxn.cursor()

#############  QUERY-1 ###############
    ##### Visualize the distribution of gender among respondents using a pie chart. ###
    query1 = "SELECT GENDER, COUNT(*) AS gender_count FROM DETAILS GROUP BY GENDER"
    df1 = pd.read_sql_query(query1, cnxn)

    plt.figure(figsize=(8, 8))
    plt.pie(df1['gender_count'], labels=df1['GENDER'], autopct='%1.1f%%', startangle=140)
    plt.title('Gender Distribution')
    plt.tight_layout()
    Viz1 = 'static/Gender_Distribution.png'
    plt.savefig(Viz1)
    plt.close()

#############  QUERY-2 ###############
    ### Explore the distribution of ages among respondents using a violin plot. ###
    query2 = "SELECT AGE FROM DETAILS"
    df2 = pd.read_sql_query(query2, cnxn)

    plt.figure(figsize=(10, 6))
    sns.violinplot(data=df2, x='AGE')
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.tight_layout()
    Viz2 = 'static/Age_Distribution.png'
    plt.savefig(Viz2)
    plt.close()

#############  QUERY-3 ###############
    ### Plot the most used social media platforms using a horizontal bar plot for a different perspective. ###
    query3 = """SELECT MOST_USED, COUNT(*) AS platform_count
    FROM SOCIAL_MEDIA GROUP BY MOST_USED
    """
    df3 = pd.read_sql_query(query3, cnxn)

    plt.figure(figsize=(10, 6))
    plt.barh(df3['MOST_USED'], df3['platform_count'])
    plt.title('Most Used Social Media Platforms')
    plt.xlabel('Number of Respondents')
    plt.ylabel('Social Media Platform')
    plt.tight_layout()
    Viz3 = 'static/Most_Used_SMP.png'
    plt.savefig(Viz3)
    plt.close()



#############  QUERY-4 ###############
    ### Create a stacked bar plot to show the 
    ### distribution of time of day usage across different social media platforms.
    query4 = """
                SELECT MOST_USED, 
                    SUM(CASE WHEN TIME_OF_DAY = 'Morning (6:00 AM - 12:00 PM)' THEN 1 ELSE 0 END) AS Morning,
                    SUM(CASE WHEN TIME_OF_DAY = 'Afternoon (12:00 PM - 6:00 PM)' THEN 1 ELSE 0 END) AS Afternoon,
                    SUM(CASE WHEN TIME_OF_DAY = 'Evening (6:00 PM - 12:00 AM)' THEN 1 ELSE 0 END) AS Evening,
                    SUM(CASE WHEN TIME_OF_DAY = 'Late Night (12:00 AM - 6:00 AM)' THEN 1 ELSE 0 END) AS LateNight
                FROM SOCIAL_MEDIA
                GROUP BY MOST_USED
                """
    df4 = pd.read_sql_query(query4, cnxn)

    plt.figure(figsize=(10, 6))
    plt.bar(df4['MOST_USED'], df4['Morning'], label='Morning')
    plt.bar(df4['MOST_USED'], df4['Afternoon'], bottom=df4['Morning'], label='Afternoon')
    plt.bar(df4['MOST_USED'], df4['Evening'], bottom=df4['Morning'] + df4['Afternoon'], label='Evening')
    plt.bar(df4['MOST_USED'], df4['LateNight'], bottom=df4['Morning'] + df4['Afternoon'] + df4['Evening'], label='LateNight')
    plt.title('Time of Day Usage Across Social Media Platforms')
    plt.xlabel('Social Media Platform')
    plt.ylabel('Number of Respondents')
    plt.legend()
    plt.tight_layout()
    Viz4 = 'static/SM_TimeSpent.png'
    plt.savefig(Viz4)
    plt.close()

#############  QUERY-5 ###############
    ### Explore the frequency distribution of social media usage per day using a histogram. ###
    query5 = "SELECT FREQUENCY FROM SOCIAL_MEDIA"
    df5 = pd.read_sql_query(query5, cnxn)

    plt.figure(figsize=(10, 6))
    plt.hist(df5['FREQUENCY'], bins=10, edgecolor='black')
    plt.title('Frequency of Social Media Usage per Day')
    plt.xlabel('Frequency')
    plt.ylabel('Number of Respondents')
    plt.tight_layout()
    Viz5 = 'static/Frequency.png'
    plt.savefig(Viz5)
    plt.close()

#############  QUERY-6 ###############
    ### Create a clustered bar plot to compare the primary use of social media by gender. ###
    query6 = """
                SELECT Gender, 
        SUM(CASE WHEN [PRIMARY_USE] = 'Staying connected with friends and family' THEN 1 ELSE 0 END) AS Staying_connected,
        SUM(CASE WHEN [PRIMARY_USE] = 'Sharing photos or videos' THEN 1 ELSE 0 END) AS Sharing_photos_videos,
        SUM(CASE WHEN [PRIMARY_USE] = 'Keeping up with news and current events' THEN 1 ELSE 0 END) AS Keeping_up_with_news,
        SUM(CASE WHEN [PRIMARY_USE] = 'Networking with professionals or colleagues' THEN 1 ELSE 0 END) AS Networking_with_professionals,
        SUM(CASE WHEN [PRIMARY_USE] = 'Messaging or chatting with others' THEN 1 ELSE 0 END) AS Messaging_chatting,
        SUM(CASE WHEN [PRIMARY_USE] = 'Discovering new content or entertainment' THEN 1 ELSE 0 END) AS Discovering_new_content
    FROM SOCIAL_MEDIA
    INNER JOIN STATS ON LTRIM(RTRIM(SOCIAL_MEDIA.SM_ID)) = LTRIM(RTRIM(STATS.SM_ID))
    INNER JOIN DETAILS ON LTRIM(RTRIM(SOCIAL_MEDIA.ID)) = LTRIM(RTRIM(DETAILS.ID))
    GROUP BY Gender
                """
    df6 = pd.read_sql_query(query6, cnxn)

    plt.figure(figsize=(12, 8))
    sns.barplot(data=df6, x='Gender', y='Staying_connected', color='skyblue', label='Staying connected')
    sns.barplot(data=df6, x='Gender', y='Sharing_photos_videos', color='orange', label='Sharing photos/videos', bottom=df6['Staying_connected'])
    sns.barplot(data=df6, x='Gender', y='Keeping_up_with_news', color='green', label='Keeping up with news', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'])
    sns.barplot(data=df6, x='Gender', y='Networking_with_professionals', color='red', label='Networking', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'])
    sns.barplot(data=df6, x='Gender', y='Messaging_chatting', color='purple', label='Messaging/chatting', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'] + df6['Networking_with_professionals'])
    sns.barplot(data=df6, x='Gender', y='Discovering_new_content', color='yellow', label='Discovering content', bottom=df6['Staying_connected'] + df6['Sharing_photos_videos'] + df6['Keeping_up_with_news'] + df6['Networking_with_professionals'] + df6['Messaging_chatting'])
    plt.title('Primary Use of Social Media by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Number of Respondents')
    plt.legend()
    plt.tight_layout()
    Viz6 = 'static/Primary_Use_Gender.png'
    plt.savefig(Viz6)
    plt.close()


#############  QUERY-7 ###############
    ### Visualize the distribution of responses regarding the importance of social media 
    ### in daily life using a line plot. ###
    query7 = "SELECT IMPORTANCE FROM STATS"
    df7 = pd.read_sql_query(query7, cnxn)

    plt.figure(figsize=(10, 6))
    df7['IMPORTANCE'].value_counts().sort_index().plot(marker='o')
    plt.title('Distribution of Importance of Social Media in Daily Life')
    plt.xlabel('Importance Level')
    plt.ylabel('Number of Respondents')
    plt.grid(True)
    plt.tight_layout()
    Viz7 = 'static/Importance.png'
    plt.savefig(Viz7)
    plt.close()

    #############  QUERY-8 ###############
        ### Explore the relationship between age and confidence in 
        ### controlling social media usage using a scatter plot.
    query8 = """
                SELECT AGE, CONTROLLING_ABILITY
                FROM DETAILS
                INNER JOIN STATS ON DETAILS.E_ID = STATS.E_ID
                """
    df8 = pd.read_sql_query(query8, cnxn)

    plt.figure(figsize=(10, 6))
    plt.scatter(df8['AGE'], df8['CONTROLLING_ABILITY'], alpha=0.5)
    plt.title('Relationship between Age and Confidence in Controlling Social Media Usage')
    plt.xlabel('Age')
    plt.ylabel('Confidence in Controlling Usage')
    plt.grid(True)
    plt.tight_layout()
    Viz8 = 'static/Age_Confidence.png'
    plt.savefig(Viz8)
    plt.close()

#############  QUERY-9 ###############
    ### Create a grouped box plot to compare the sleep impact 
    ### due to social media between different genders.
    query9 = """
                SELECT GENDER, SLEEP_AFFECT
                FROM DETAILS
                INNER JOIN STATS ON DETAILS.E_ID = STATS.E_ID
                """
    df9 = pd.read_sql_query(query9, cnxn)

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='GENDER', y='SLEEP_AFFECT', data=df9)
    plt.title('Sleep Impact Due to Social Media by Gender')
    plt.xlabel('Gender')
    plt.ylabel('Sleep Impact')
    plt.grid(True)
    plt.tight_layout()
    Viz9 = 'static/Sleep_Gender.png'
    plt.savefig(Viz9)
    plt.close()



#############  QUERY-10 ###############
    ### Use a pair plot to visualize pairwise relationships between 
    ### different variables, such as age, time spent on social media, and sleep impact.
    query10 = """
                SELECT Age, Avg_time_spent, Sleep_Affect
                FROM SOCIAL_MEDIA
                INNER JOIN STATS ON SOCIAL_MEDIA.SM_ID = STATS.SM_ID
                INNER JOIN DETAILS ON DETAILS.ID = SOCIAL_MEDIA.ID
                INNER JOIN EMOTIONS ON SOCIAL_MEDIA.SM_ID = EMOTIONS.SM_ID
                """
    df10 = pd.read_sql_query(query10, cnxn)

    sns.set_theme(style="ticks")
    sns.pairplot(df10)
    plt.title('Pairwise Relationships')
    plt.tight_layout()
    Viz10 = 'static/Age_Time_Sleep.png'
    plt.savefig(Viz10)
    plt.close()

#############  QUERY-11 ###############
    ### Compare the frequency of content posting 
    ### across different social media platforms using a clustered bar plot.
    query11 = """
                SELECT SM.MOST_USED, SM.POSTING_FREQUENCY
                FROM SOCIAL_MEDIA SM ORDER BY ID
                """
    df11 = pd.read_sql_query(query11, cnxn)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='MOST_USED', y='POSTING_FREQUENCY', data=df11, errorbar=None)
    plt.title('Frequency of Content Posting by Most Used Platform')
    plt.xlabel('Social Media Platform')
    plt.ylabel('Frequency of Content Posting')
    plt.tight_layout()
    Viz11 = 'static/Post_Frequency.png'
    plt.savefig(Viz11)
    plt.close()

#############  QUERY-12 ###############
    ### Create a grouped bar plot to compare the pressure to present 
    ### a certain image on social media between different age groups.
    query12 = """
                SELECT AGE, PRESSURE_TO_PRESENT
                FROM DETAILS
                INNER JOIN EMOTIONS ON DETAILS.E_ID = EMOTIONS.E_ID ORDER BY ID
                """
    df12 = pd.read_sql_query(query12, cnxn)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='AGE', y='PRESSURE_TO_PRESENT', data=df12, errorbar=None)
    plt.title('Pressure to Present a Certain Image on Social Media by Age')
    plt.xlabel('Age Group')
    plt.ylabel('Pressure to Present Image (Scale)')
    plt.tight_layout()
    Viz12 = 'static/pressure_present.png'
    plt.savefig(Viz12)
    plt.close()

#############  QUERY-13 ###############
    ### Visualize the frequency of interacting with new people 
    ### on social media by platform using a stacked bar plot.
    query13 = """
                SELECT SM.MOST_USED, E.NEW_INTERACTIONS
                FROM SOCIAL_MEDIA SM
                INNER JOIN STATS S ON SM.SM_ID = S.SM_ID
                INNER JOIN EMOTIONS E ON S.E_ID = E.E_ID ORDER BY ID
                """
    df13 = pd.read_sql_query(query13, cnxn)
    cnxn.close()
    df_pivot = df13.pivot_table(index='MOST_USED', columns='NEW_INTERACTIONS', aggfunc='size', fill_value=0)
    plt.figure(figsize=(10, 6))
    df_pivot.plot(kind='bar', stacked=True)
    plt.title('Frequency of Interacting with New People by Platform')
    plt.xlabel('Social Media Platform')
    plt.ylabel('Frequency of Interaction')
    plt.tight_layout()
    Viz13 = 'static/New_Interactions.png'
    plt.savefig(Viz13)
    plt.close()
    return render_template('index.html', Viz1 = 'static/Gender_Distribution.png', 
                           Viz2 = 'static/Age_Distribution.png',
                           Viz3 = 'static/Most_Used_SMP.png',
                           Viz4 = 'static/SM_TimeSpent.png',
                           Viz5 = 'static/Frequency.png',
                           Viz6 = 'static/Primary_Use_Gender.png',
                           Viz7 = 'static/Importance.png',
                           Viz8 = 'static/Age_Confidence.png',
                           Viz9 = 'static/Sleep_Gender.png',
                           Viz10 = 'static/Age_Time_Sleep.png',
                           Viz11 = 'static/Post_Frequency.png',
                           Viz12 = 'static/pressure_present.png',
                           Viz13 = 'static/New_Interactions.png',
                           Viz14 = 'static/pressure_present.png',
                           Viz15 = 'static/New_Interactions.png'
                           )

if __name__ == '__main__':
    app.run(debug=True)
