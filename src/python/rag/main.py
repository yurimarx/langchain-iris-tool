from langchain_iris_tool.tools import InterSystemsIRISTool
from langchain_ollama import ChatOllama
import streamlit as st

#
#   LANGCHAIN OLLAMA WRAPPER
#

username = "_system"
password = "SYS"
hostname = "iris"
port = 1972
webport = 52773
namespace = "USER"


#
#   STREAMLIT APP
#

st.title("Langchain IRIS Tool Agent")

with st.popover("Settings"):
    username = st.text_input("Username:", username)
    password = st.text_input("Password:", password)
    hostname = st.text_input("Hostname:", hostname)
    port = int(st.text_input("Port:", port))
    webport = int(st.text_input("Web port:", webport))
    namespace = st.text_input("Namespace:", namespace)
    

# User query input
query = st.text_input(label="Enter your query")

# Submit button
if st.button(label="Ask IRIS", type="primary"):
    
    tool = InterSystemsIRISTool(
            username=username, password=password, hostname=hostname, 
            port=port, webport=webport, namespace=namespace)

    llm = ChatOllama(
        base_url="http://ollama:11434", 
        model="mistral", 
        temperature=0,
    ).bind_tools([tool])

    with st.container(border=True):
        with st.spinner(text="Generating response"):
            # Get response from llm
            response = llm.invoke(query)
            st.code(tool.invoke(response.tool_calls[0]["args"]), language="yaml")