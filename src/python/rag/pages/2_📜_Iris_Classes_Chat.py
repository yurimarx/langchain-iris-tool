import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import langchain_helper as lch

username = "_system"
password = "SYS"
hostname = "iris"
port = 51972
webport = 52773
namespace = "USER"

st.set_page_config(page_title="InterSystems IRIS Classes Demo", page_icon="📜")

st.title("Langchain IRIS Classes Chat")

with st.popover("Settings"):
    with st.spinner(text="Connecting to the IRIS classes"):
        engine = create_engine("iris://" + username + ":" + password + "@" + hostname + ":" + str(port) + "/" + namespace)
        connection  = engine.connect()
        query = 'select * from %Dictionary.ClassDefinition where substring(ID,1,1) <> \'%\' and  Copyright is null'
        df = pd.read_sql(query, con=connection)
        df.to_csv("classes.csv")
    
    username = st.text_input("Username:", username)
    password = st.text_input("Password:", password)
    hostname = st.text_input("Hostname:", hostname)
    port = int(st.text_input("Port:", port))
    webport = int(st.text_input("Web port:", webport))
    namespace = st.text_input("Namespace:", namespace)

            

# User query input
query = st.text_input(label="Enter your query")

# Submit button
if st.button(label="Ask IRIS Classes", type="primary"):
    
    with st.spinner(text="Generating response"):
        iris_conn_str = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"
        response = lch.get_insights(query, "classes.csv", iris_conn=iris_conn_str, collection_name="classes")
        st.write(response['result'])
