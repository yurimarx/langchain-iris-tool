from langchain.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OllamaEmbeddings
from langchain_iris import IRISVector

def get_insights(question, csv_file, iris_conn, collection_name):
    
    # Load and process the CSV data    
    loader = CSVLoader(csv_file)
    documents = loader.load()

    llm = Ollama(
        base_url="http://ollama:11434", 
        model="mistral", 
        temperature=0,
    )

    # Create embeddings
    embeddings = OllamaEmbeddings(model="mistral", base_url="http://ollama:11434", temperature=0)

    db = IRISVector.from_documents(
        embedding=embeddings, 
        documents=documents,
        connection_string=iris_conn,
        collection_name=collection_name,
        pre_delete_collection=True
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever())

    
    return qa({"query": question})
