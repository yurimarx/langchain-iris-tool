from langchain_ollama.llms import OllamaLLM
from langchain.prompts.prompt import PromptTemplate
from langchain_iris_tool.tools import InterSystemsIRISTool
from langchain_ollama import ChatOllama

tool = InterSystemsIRISTool(
    username="_SYSTEM", password="SYS", hostname="localhost", port=55551, namespace="USER"
)

llm = ChatOllama(
    model="mistral",
    temperature=0,
).bind_tools([tool])

result = llm.invoke(
    "List the jobs on namespace %SYS"
)

print(tool.invoke(result.tool_calls[0]["args"]))
