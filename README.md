# mupif-wrapper-poc
Proof of concept with the aim to expose mupif functionalities as a rest service. 

## How to launch
- clone / download the project from github
- install / check pipenv (developed with version 8.2.7) 
- create a virtualenv associated to the project and install all the required dependencies, using pipenv, running `pipenv install` from inside the project folder
- enter pipenv with command `pipenv shell`
- inside the activated shell environment run `python main.py`

## Quick example using Chrome web browser
- open your browser at `http://127.0.0.1:5000/run/Example03?inputs={'app3.in': 'app3.in', 'application3': './application3'}` , an execution will be triggered
- click on the `view result` link
- `RUNNING` message will be displayed
- wait 10 seconds, then refresh the page 
- output file names will be displayed: `{"app3.out": "app3.out", "log": "mupif.log"}` 

## Example using CURL to simulate beepmn client requesting an execution
- install / check  curl 
- run `curl -X POST -H "Content-Type: application/json" -d "{'app3.in': 'app3.in', 'application3': './application3'}" http://127.0.0.1:5000/run/Example03`
- run `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/info/INSERT_RETRIEVED_EXECUTION_ID_HERE`
- `RUNNING` message will be displayed
- wait 10 seconds, the execute the second curl command again 
- output file names should be displayed: `{"app3.out": "app3.out", "log": "mupif.log"}` 

## Notes
The main idea behind this proof of concept is to create a service (an always running process) that exposes some functionalities:
- ask for a MuPIF workflow execution 
- ask for MuPIF workflow execution status / output 

The code is divided into 3 modules:
- **rest interface** (main.py)
- **execution service**: responsible to launch the executions in a process pool and to hold the status / results of a started execution 
- **mupif worker**: code that runs inside the pool processes and loads MuPIF workflows

The ouput of a correctly completed execution is an object containing the produced files names. We intend this names as a pointer to the outputs produced by the execution, so they could also be an id pointing to a record set on a database.
