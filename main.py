from langchain_iris_tool.tools import InterSystemsIRISTool
from langchain_ollama import ChatOllama
from langchain_ollama.llms import OllamaLLM
import streamlit as st

#
#   LANGCHAIN OLLAMA WRAPPER
#

tool = InterSystemsIRISTool(
    username="_SYSTEM", password="SYS", hostname="localhost", port=55797, namespace="USER"
)

llm = ChatOllama(
    model="mistral",
    temperature=0,
).bind_tools([tool])

#
#   STREAMLIT APP
#

st.title("LLM App")

# User query input
query = st.text_input(label="Enter your query")

# Submit button
if st.button(label="Ask LLM", type="primary"):

    with st.container(border=True):
        with st.spinner(text="Generating response"):
            # Get response from llm
            response = llm.invoke(query)

        # Display it
        st.code(tool.invoke(response.tool_calls[0]["args"]), language="yaml")