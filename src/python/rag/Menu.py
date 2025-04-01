import streamlit as st

st.set_page_config(
    page_title="InterSystems IRIS Langchain Demos",
    page_icon="👋",
)

st.write("# Welcome to Langchain IRIS Tool! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Langchain IRIS Tool is an open-source app for interact with InterSystems IRIS using
    langchain framework.
    **👈 Select a demo from the sidebar** to see some examples
    of what Langchain IRIS Tool can do!
    ### Want to learn more?
    - Check out [Langchain IRIS Tool](https://openexchange.intersystems.com/package/langchain-iris-tool)
"""
)
