import mysql.connector
from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
## Configure Genai Key  
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    ## Function To Load Google Gemini Model and provide queries as response

    def get_gemini_response(question,prompt):
        model=genai.GenerativeModel('gemini-pro')
        response=model.generate_content([prompt[0],question])
        return response.text
    def get_gemini_content(prompt):
        model=genai.GenerativeModel('gemini-pro')
        response=model.generate_content(prompt)
        return response.text

    ## Fucntion To retrieve query from the database

    def read_sql_query(sql):
        # conn=sqlite3.connect(db)
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="DATABASE"
        )
        cur=conn.cursor()
        cur.execute(sql)
        print(cur.rowcount)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        for row in rows:
            print(row)
        return rows

    ## Define Your Prompt
    prompt=[
        """
        You are an expert in converting English questions to SQL query!
        The SQL database has the name USERS and has the following columns -SNO, NAME, EMAIL, 
        PASSWORD, DATE, SOCIAL_MEDIA \n\nFor example,\nExample 1 - How many entries of records are present?, 
        the SQL command will be something like this SELECT COUNT(*) FROM USERS ;
        \nExample 2 - Show me all the users., the SQL command will be something like this SELECT * FROM USERS
        \nExample 3 - Tell me all the users who use facebook social media?, 
        the SQL command will be something like this SELECT * FROM USERS WHERE SOCIAL_MEDIA="Facebook" 
        also the sql code should not have ``` in beginning or end and sql word in output

        """


    ]
    

    ## Streamlit App

    # st.set_page_config(page_title="")
    st.header("Talk to MySQL Database")

    question=st.text_input("Input: ",key="input")

    submit=st.button("Ask the question")

    # if submit is clicked
    if submit:
        response=get_gemini_response(question,prompt)
        print(response)
        response1=read_sql_query(response)
        print("response1 is ", response1)
        st.subheader("The Response is") 
        # for row in response1:
        #     print(row)
            # st.write(row)
        if len(response1) == 0:
            explanation_request= f"Show simple shoter acknowledgment according to {question} in one line and do not add extra text according to your knowledge do not show this kind of line Sure, here's a simple shorter acknowledgment according to the change of Karishma's name to Suhana in one line:"
        else:
            explanation_request = f"convert this object data {response1} in a user friendly language and write it little shorter according to {question}. do not add extra such as shorter answer and such things?"
        response2=get_gemini_content(explanation_request)
        print("response2 is ", response2)
        st.write(response2)
except Exception as e:
    print(f"An error occurred: {e}")
