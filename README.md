 [![Gitter](https://img.shields.io/badge/Available%20on-Intersystems%20Open%20Exchange-00b2a9.svg)](https://openexchange.intersystems.com/package/langchain-iris-tool)
 
# langchain-iris-tool
Contains an implementation of a Langchain Tool (BaseTool) to do RAG operations on Intersystems IRIS Server. 
It is a Chat Agent tool also. It is possible ask questions like:

1. Return intersystems iris server information
2. Save the global value Hello to the global name Greetings
3. Get the global value Greetings
4. Kill the global Greetings
5. List the classes on IRIS Server
6. Where is intersystems iris installed?
7. Return namespace information from the USER
8. List the CSP Applications
9. List the server files on namespace USER
10. List the jobs on namespace %SYS

## Prerequisites
Make sure you have [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and [Docker desktop](https://www.docker.com/products/docker-desktop) installed.

## Installation

### Docker (e.g. for dev purposes)

Clone/git pull the repo into any local directory

```
$ git clone https://github.com/yurimarx/langchain-iris-tool.git
```

Open the terminal in this directory and run:

```
$ docker-compose build
$ docker-compose up -d
```

## Solutions used

1. Ollama - private LLM and NLP Chat tool
2. Lanchain - plataform to build AI agents
3. Streamlit - Frontend framework
4. InterSystems IRIS as a server to answer the questions about it

## Testing

1. Open the URL http://localhost:8501
<img width="600" alt="UI 1" src="https://github.com/yurimarx/langchain-iris-tool/blob/defa15664fe741933f98e4bddb572549097d2793/images/ui-1.png">

2. Check out the Settings button used to the Agent connect the InterSystems IRIS
<img width="600" alt="UI 1" src="https://github.com/yurimarx/langchain-iris-tool/blob/defa15664fe741933f98e4bddb572549097d2793/images/ui-1.png">

3. Ask one of the following questions and wait some seconds to see the results:

3.1. Return intersystems iris server information
3.2. Save the global value Hello to the global name Greetings
3.3. Get the global value Greetings
3.4. Kill the global Greetings
3.5. List the classes on IRIS Server
3.6. Where is intersystems iris installed?
3.7. Return namespace information from the USER
3.8. List the CSP Applications
3.9. List the server files on namespace USER
3.10. List the jobs on namespace %SYS

<img width="600" alt="UI 1" src="https://github.com/yurimarx/langchain-iris-tool/blob/defa15664fe741933f98e4bddb572549097d2793/images/ui-1.png">



