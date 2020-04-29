#example of python connecting to MySQL server and databases
#
import mysql.connector
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import squarify
#
from mysql.connector import Error
#
def connecttomysql(db):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                             database = db,
                                             user='root',
                                             password='',
                                             auth_plugin = 'mysql_native_password')
        
        
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return e
        
        
def closeconnection(connection, cursor):
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

connection = connecttomysql('arms')
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("Your connected to database: ", record[0])
#
    sql_select_Query1 = '''SELECT location, YEAR(Date_time), count(*) AS NUM_OF_EVENTS 
                        FROM EVENT e group by location, YEAR(Date_time);'''
    cursor = connection.cursor()
    cursor.execute(sql_select_Query1)
    records = cursor.fetchall()
    print(":\n")
    event_info = pd.DataFrame(records, columns = ['Location', 'Year', 'Number_Of_Events'])
    
    print("Frequency of events that occured at each location over the years.")
    stack1 = np.add(event_info[event_info.Year == 2017].Number_Of_Events.values, 
                    event_info[event_info.Year == 2018].Number_Of_Events.values).tolist()
    stack2 = np.add(stack1, event_info[event_info.Year == 2019].Number_Of_Events.values)
    
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])    
    ax.bar(pd.unique(event_info.Location), event_info[event_info.Year == 2017].Number_Of_Events.values, color = 'r') 
    ax.bar(pd.unique(event_info.Location), event_info[event_info.Year == 2018].Number_Of_Events.values, 
           bottom = event_info[event_info.Year == 2017].Number_Of_Events.values, color='orange')
    ax.bar(pd.unique(event_info.Location), event_info[event_info.Year == 2019].Number_Of_Events.values, 
           bottom = stack1, color='b')
    ax.bar(pd.unique(event_info.Location), event_info[event_info.Year == 2020].Number_Of_Events.values,
           bottom = stack2, color='g')
    ax.set_yticks(np.arange(0, 11, 1))
    ax.set_ylabel('Number of Events')
    ax.set_xlabel('Locations')
    ax.set_title('Frequency of events that occured at each location over the years.')
    ax.legend(labels=pd.unique(event_info.Year))
    plt.show() 
    
    
    sql_select_Query2 = '''select C.Name, Count(*) AS Num_Of_Postings from job_posting JP, Company C
                        where JP.C_Tag_ID = C.C_Tag_ID
                        group by C.Name
                        order by 2 Desc;'''
    cursor = connection.cursor()
    cursor.execute(sql_select_Query2)
    records = cursor.fetchall()
    print("\n")
    print("Proportion of job postings of each company")
    company_postings = pd.DataFrame(records, columns = ['CompanyName', 'NoOfPostings'])
    squarify.plot(sizes=company_postings['NoOfPostings'], label=company_postings['CompanyName'], alpha=.8 )
    plt.axis('off')
    plt.title('Proportion of job postings of each company')
    plt.show()
    
    #View Created in Database has been Called here:
    sql_select_Query3 = "select * from top_career_events LIMIT 5;"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query3)
    records = cursor.fetchall()
    print("\n")
    top_career_event = pd.DataFrame(records, columns = ['Topic', 'NumOfStudentsAttended'])
    df = pd.DataFrame({'Students Attended': top_career_event.NumOfStudentsAttended.values}, index= top_career_event.Topic.values)
    
    print("Top 5 successful events based on student attendance")
    df.plot(kind='pie', subplots=True, figsize=(16,10))
    plt.show()
    
#Close the connection:    
closeconnection(connection,cursor)