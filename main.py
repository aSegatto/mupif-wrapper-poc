import ast
import logging
import os

from flask import Flask, Response, request
from flask_restful import Resource, Api

from execution_service import ExecutionService


class DinamicallyImportedScriptExecution(Resource):
    default_working_dir = os.getcwd()

    def get(self, script_name):
        inputs = request.args.get("inputs")
        inputs_dict = ast.literal_eval(inputs)
        logger.info("Inputs: %s" % inputs_dict)
        execution_id = executionService.create_new_execution(script_name, inputs_dict)
        response_message = '<body><p>Execution id = ' + execution_id + '</p><a href="http://127.0.0.1:5000/info/' + execution_id + '">view result</a></body>'
        return Response(response=response_message, status=200, mimetype="text/html")

    def post(self, script_name):
        inputs = request.data
        inputs_dict = ast.literal_eval(inputs.decode())
        logger.info("Inputs: %s" % inputs_dict)
        execution_id = executionService.create_new_execution(script_name, inputs_dict)
        response_message = 'Execution id = %s\n' % execution_id
        return Response(response=response_message, status=200, mimetype="text/html")


class InfoOnScriptExecution(Resource):
    def get(self, execution_id):
        return executionService.get_execution_state(execution_id)


app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

api = Api(app)
api.add_resource(DinamicallyImportedScriptExecution, '/run/<string:script_name>')
api.add_resource(InfoOnScriptExecution, '/info/<string:execution_id>')
executionService = ExecutionService(3)

if __name__ == '__main__':
    app.run(threaded=True)
