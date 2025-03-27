"""InterSystems IRIS tools for interacting with InterSystems IRIS."""

from typing import Any, Dict, List, Optional, Type, Union, cast

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langchain_core.tools.base import ToolCall
from pydantic import BaseModel, Field, PrivateAttr
import requests
import yaml
import iris
import urllib.parse


class InterSystemsIRISInput(BaseModel):
    """Input schema for InterSystems IRIS operations."""

    operation: str = Field(
        ...,
        description=(
            "The operation to perform: 'set_global' (Set Global value), 'get_global' "
            "(get global value), 'kill_global (delete global)', 'list_objects' (get available objects), 'describe' "
            "(get object documentation), 'query' (sql query), install_path (get Intersystems IRIS installation path), "
            "class_list (get Intersystems IRIS class list), server_info (get InterSystems IRIS server information), "
            "list_csp (list web/csp applications), list_files (list server/intersystems iris files), "
            "get_namespace (get information about a namespace), list_jobs (list the jobs on server/intersystems iris namespace)"
            "'create', 'update', or 'delete'"
        ),
    )
    global_name: Optional[str] = Field(
        None,
        description="The InterSystems IRIS global name for the operations get_global and set_global (e.g., 'Contact', 'Account', 'Lead')",
    ),
    global_value: Optional[str] = Field(
        None, description="InterSystems IRIS global value for set_global operation"
    ),
    query: Optional[str] = Field(
        None, description="The SQL query string for 'query' operation"
    ),
    filename: Optional[str] = Field(
        None,
        description="The InterSystems IRIS file name (e.g., 'Contact', 'Account', 'Lead')",
    ),
    class_name: Optional[str] = Field(
        None,
        description="The InterSystems IRIS class name (e.g., 'Contact', 'Account', 'Lead')",
    ),
    record_data: Optional[Dict[str, Any]] = Field(
        None, description="Data for create/update operations as key-value pairs"
    )
    record_id: Optional[str] = Field(
        None, description="InterSystems IRIS record ID for update/delete operations"
    )


class InterSystemsIRISTool(BaseTool):
    """Tool for interacting with InterSystems IRIS using intersystems-irispython.

    Setup:
        Install required packages and set environment variables:

        .. code-block:: bash

            pip install intersystems-irispython
            export IRIS_USERNAME="your-username"
            export IRIS_PASSWORD="your-password"
            export IRIS_NAMESPACE="your-namespace"
            export IRIS_PORT="iris-port"
            export IRIS_WEBPORT="iris-webport"
            export IRIS_HOST="iris-host" 

    Examples:
        Set/Save the value Hello to the global/object greeting:
            {
                "operation": "set_global",
                "global_value": "Hello",
                "global_name": "greeting"
            }

        Get the global value greeting:
            {
                "operation": "get_global",
                "global_name": "greeting"
            }

        Kill/Delete the global greeting:
            {
                "operation": "kill_global",
                "global_name": "greeting"
            }
        
        Describe the class Account:
            {
                "operation": "describe",
                "class_name": "Account"
            }

        List server/intersystems iris files on namespace USER with file name Portal:
            {
                "operation": "list_files",
                "namespace": "USER",
                "filename": "Portal"
            }
        
        Where is intersystems iris installed?:
            {
                "operation": "install_path"
            }
        
        Return namespace information from the USER:
            {
                "operation": "get_namespace",
                "namespace": "USER"
            }
            
        Return information about intersystems iris server:
            {
                "operation": "server_info"
            }
        
        List the jobs on namespace USER:
            {
                "operation": "list_jobs"
                "query": "USER"
            }
        
            
        List the CSP/Web Applications on namespace USER:
            {
                "operation": "list_csp"
                "query": "USER"
            }
        
        Query contacts:
            {
                "operation": "query",
                "query": "SELECT TOP 5 Id, Name, Email FROM Contact"
            }

        Create new contact:
            {
                "operation": "create",
                "object_name": "Contact",
                "record_data": {"LastName": "Smith", "Email": "smith@example.com"}
            }
    """

    name: str = "intersystems_iris"
    description: str = (
        "Tool for interacting with InterSystems IRIS"
    )
    args_schema: Type[BaseModel] = InterSystemsIRISInput
    _iris: iris.IRIS = PrivateAttr()
    _conn: iris.IRISConnection = PrivateAttr()
    _username: str = PrivateAttr()
    _password: str = PrivateAttr()
    _namespace: str = PrivateAttr()
    _host: str = PrivateAttr()
    _port: int = PrivateAttr()
    _webport: int = PrivateAttr()

    def __init__(
        self,
        username: str,
        password: str,
        hostname: str,
        port: int,
        webport: int,
        namespace: str,
    ) -> None:
        """Initialize iris connection."""
        super().__init__()
        
        self._conn = iris.connect(hostname + ":" + str(port) + "/" + namespace, username=username, password=password, sharedmemory=False)
        self._iris = iris.createIRIS(self._conn)
        self._username = username 
        self._password = password
        self._namespace = namespace
        self._host = hostname
        self._port = port
        self._webport = webport
    
    def _run(
        self,
        operation: str,
        global_name: Optional[str] = None,
        global_value: Optional[Any] = None,
        query: Optional[str] = None,
        filename: Optional[str] = None,
        class_name: Optional[str] = None,
        namespace: Optional[str] = "%SYS",
        record_data: Optional[Dict[str, Any]] = None,
        record_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
        """Execute InterSystems IRIS operation."""
        try:
            
            baseurl = "http://" + self._host + ":" + str(self._webport)

            if operation == "get_global":
                if not global_name:
                    raise ValueError("Global name is required for 'get_global' operation")
                return self._iris.get(global_name) 

            elif operation == "set_global":
                if not global_name:
                    raise ValueError("Global name and global value are required for 'set_global' operation")
                return self._iris.set(global_value, global_name)

            elif operation == "kill_global":
                if not global_name:
                    raise ValueError("Global name is required for 'kill_global' operation")
                return self._iris.kill(global_name)

            elif operation == "query":
                if not query:
                    raise ValueError("Query string is required for 'query' operation")
                cursor = self._conn.cursor()
                cursor.execute(query)
                return cursor.fetchall()
            
            elif operation == "install_path":
                return self._iris.classMethodString('%SYSTEM.Util', 'InstallDirectory')
            
            elif operation == "get_namespace":
                if global_name:
                    namespace = global_name
                return self.getStudioApiResponse(baseurl, '/api/atelier/v1/' + urllib.parse.quote(namespace), self._username, self._password)

            elif operation == "list_jobs":
                return self.getStudioApiResponse(baseurl, '/api/atelier/v1/' + urllib.parse.quote(namespace) +'/jobs', self._username, self._password)

            elif operation == "list_files":
                if filename:
                    print("lista arquivos " + filename + " no namespace " + namespace)
                    return self.getStudioApiResponse(baseurl, '/api/atelier/v1/' + urllib.parse.quote(namespace) +'/docnames/CLS?filter=' + filename, self._username, self._password)
                else:
                    return self.getStudioApiResponse(baseurl, '/api/atelier/v1/' + urllib.parse.quote(namespace) +'/docnames/CLS', self._username, self._password)

            elif operation == "server_info":
                return self.getStudioApiResponse(baseurl, '/api/atelier/', self._username, self._password)

            elif operation == "list_csp":
                return self.getStudioApiResponse(baseurl, '/api/atelier/v1/' + urllib.parse.quote(namespace) +'/cspapps', self._username, self._password)
                
            elif operation == "describe":
                if not class_name:
                    raise ValueError("Class name is required for 'describe' operation")
                return self._iris.classMethodVoid(class_name, '%ClassName')

            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            return f"Error performing Intersystems IRIS operation: {str(e)}"

    async def _arun(
        self,
        operation: str,
        global_name: Optional[str] = None,
        global_value: Optional[str] = None,
        query: Optional[str] = None,
        filename: Optional[str] = None,
        class_name: Optional[str] = None,
        namespace: Optional[str] = "%SYS",
        record_data: Optional[Dict[str, Any]] = None,
        record_id: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[str, Dict[str, Any], List[Dict[str, Any]]]:
        """Async implementation of Intersystems IRIS operations."""
        # Intersystems IRIS doesn't have native async support,
        # so we just call the sync version
        return self._run(
            operation, global_name, global_value, query, filename, class_name, namespace, record_data, record_id, run_manager
        )

    def invoke(
        self,
        input: Union[str, Dict[str, Any], ToolCall],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Any:
        """Run the tool."""
        if input is None:
            raise ValueError("Unsupported input type: <class 'NoneType'>")

        if isinstance(input, str):
            raise ValueError("Input must be a dictionary")

        if hasattr(input, "args") and hasattr(input, "id") and hasattr(input, "name"):
            input_dict = cast(Dict[str, Any], input.args)
        else:
            input_dict = cast(Dict[str, Any], input)

        if not isinstance(input_dict, dict):
            raise ValueError(f"Unsupported input type: {type(input)}")

        if "operation" not in input_dict:
            raise ValueError("Input must be a dictionary with an 'operation' key")

        return self._run(**input_dict)

    async def ainvoke(
        self,
        input: Union[str, Dict[str, Any], ToolCall],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Any:
        """Run the tool asynchronously."""
        if input is None:
            raise ValueError("Unsupported input type: <class 'NoneType'>")

        if isinstance(input, str):
            raise ValueError("Input must be a dictionary")

        if hasattr(input, "args") and hasattr(input, "id") and hasattr(input, "name"):
            input_dict = cast(Dict[str, Any], input.args)
        else:
            input_dict = cast(Dict[str, Any], input)

        if not isinstance(input_dict, dict):
            raise ValueError(f"Unsupported input type: {type(input)}")

        if "operation" not in input_dict:
            raise ValueError("Input must be a dictionary with an 'operation' key")

        return await self._arun(**input_dict)
    
    @staticmethod
    def getStudioApiResponse(baseurl, path, username, password):
        credentials = (username, password)
        response = requests.get(baseurl + path, auth=credentials)
        status = response.status_code
        if status == 200:
            return yaml.dump(response.json()) 
        else:
            return None