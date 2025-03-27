from langchain_iris_tool.tools import InterSystemsIRISTool
from langchain_ollama import ChatOllama

tool = InterSystemsIRISTool(
    username="_SYSTEM", password="SYS", hostname="localhost", port=56117, namespace="USER"
)

llm = ChatOllama(
    model="mistral",
    temperature=0,
).bind_tools([tool])

result = llm.invoke(
    "Save the value Ragdoll to the global animal"
)

print(tool.invoke(result.tool_calls[0]["args"]))
