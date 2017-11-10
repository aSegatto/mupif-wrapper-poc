# mupif-wrapper-poc
Proof of concept with the aim to expose mupif functionalities as a rest service. 

## How to Lauch
- clone / download the project form github
- install / check pipenv (developed with version 8.2.7) 
- create a pipenv associated to the project running `pipenv install` from inside the project folder
- enter pipenv with command `pipenv shell`
- inside the activated shell environment run `python main.py`

## Quick Example using Chrome web browser
- open your browser at `http://127.0.0.1:5000/run/Example03?inputs={'app3.in': 'app3.in', 'application3': './application3'}` , an execution will be triggered
- click on the view result link
- `RUNNING` message will be displayed
- Wait 10 seconds, then refresh the page 
- Output file names will be displayed 

## Example using CURL to simulate beepmn client requesting an execution
- install / check  curl 
- run `curl -X POST -H "Content-Type: application/json" -d "{'app3.in': 'app3.in', 'application3': './application3'}" http://127.0.0.1:5000/run/Example03`
- run `curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://127.0.0.1:5000/info/INSERT_RETRIEVED_EXECUTION_ID_HERE`
- `RUNNING` message will be displayed
- Wait 10 seconds, the execute the curl command again 
- Output file names should be displayed (`{"app3.out": "app3.out", "log": "mupif.log"}`)

## Architectural notes
The main idea behind this poc is to create a service (a process always running) that exposes some functionalities
- Ask for a MuPIF WF execution 
- Ask for MuPIF WF execution status / output 
The code is divided into 3 modules
- rest interface (main.py)
- execution service:  which is responsible to launch the executions in a process pool and to hold the status / results of a started execution 
- mupif_worker: which is the code that gets run inside the pool processes and loads MuPIF workflows