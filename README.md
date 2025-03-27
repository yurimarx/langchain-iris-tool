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
<img width="884" alt="UI 1" src="https://github.com/yurimarx/langchain-iris-tool/blob/defa15664fe741933f98e4bddb572549097d2793/images/ui-1.png">


you should see the output of fhir resources on this server

## Swagger UI

You can get the Swagger UI and work with it at:
http://localhost:32783/swagger-ui/index.html

To try it Open /Patient/{id} resource and call for the patient 3.
Here is what you should see:
<img width="1273" alt="Image" src="https://github.com/user-attachments/assets/8dc340cc-e5e4-4bf7-9e16-8169f76e27b6" />

## Testing Postman calls
Get fhir resources metadata
GET call for http://localhost:32783/fhir/r4/metadata
<img width="881" alt="Screenshot 2020-08-07 at 17 42 04" src="https://user-images.githubusercontent.com/2781759/89657453-c7cdac00-d8d5-11ea-8fed-71fa8447cc45.png">


Open Postman and make a GET call for the preloaded Patient:
http://localhost:32783/fhir/r4/Patient/1
<img width="884" alt="Screenshot 2020-08-07 at 17 42 26" src="https://user-images.githubusercontent.com/2781759/89657252-71606d80-d8d5-11ea-957f-041dbceffdc8.png">


## Testing FHIR API calls in simple frontend APP

the very basic frontend app with search and get calls to Patient and Observation FHIR resources could be found here:
http://localhost:32783/fhirUI/FHIRAppDemo.html
or from VSCode ObjectScript menu:
<img width="616" alt="Screenshot 2020-08-07 at 17 34 49" src="https://user-images.githubusercontent.com/2781759/89657546-ea5fc500-d8d5-11ea-97ed-6fbbf84da655.png">

While open the page you will see search result for female anemic patients and graphs a selected patient's hemoglobin values:
<img width="484" alt="Screenshot 2020-08-06 at 18 51 22" src="https://user-images.githubusercontent.com/2781759/89657718-2b57d980-d8d6-11ea-800f-d09dfb48f8bc.png">


## More sophisticated UI

The example of a richer UI around the FHIR data can be observed at:
http://localhost:32783/fhir/portal/patientlist.html

Here is an example screenshot of it:
<img width="1381" alt="Image" src="https://github.com/user-attachments/assets/0aa18442-90ed-495a-9fb0-7ced2f121527" />


## Development Resources
[InterSystems IRIS FHIR Documentation](https://docs.intersystems.com/irisforhealth20203/csp/docbook/Doc.View.cls?KEY=HXFHIR)
[FHIR API](http://hl7.org/fhir/resourcelist.html)
[Developer Community FHIR section](https://community.intersystems.com/tags/fhir)

## What's inside the repository

### Dockerfile

The simplest dockerfile which starts IRIS and imports Installer.cls and then runs the Installer.setup method, which creates IRISAPP Namespace and imports ObjectScript code from /src folder into it.
Use the related docker-compose.yml to easily setup additional parametes like port number and where you map keys and host folders.
Use .env/ file to adjust the dockerfile being used in docker-compose.


### .vscode/settings.json

Settings file to let you immedietly code in VSCode with [VSCode ObjectScript plugin](https://marketplace.visualstudio.com/items?itemName=daimor.vscode-objectscript))

### .vscode/launch.json
Config file if you want to debug with VSCode ObjectScript


## Troubleshooting
**ERROR #5001: Error -28 Creating Directory /usr/irissys/mgr/FHIRSERVER/**
If you see this error it probably means that you ran out of space in docker.
you can clean up it with the following command:
```
docker system prune -f
```
And then start rebuilding image without using cache:
```
docker-compose build --no-cache
```
and start the container with:
```
docker-compose up -d
```

This and other helpful commands you can find in [dev.md](https://github.com/intersystems-community/iris-fhir-template/blob/cd7e0111ff94dcac82377a2aa7df0ce5e0571b5a/dev.md)