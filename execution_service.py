import logging
import multiprocessing
import uuid

from mupif_worker import worker

result_dictionary = {}


class ExecutionService:
    def __init__(self, pool_size=3):
        self.logger = logging.getLogger(__name__)
        self._poolSize = pool_size
        self._resultDictionary = {}
        self._pool = multiprocessing.Pool(processes=pool_size, maxtasksperchild=1)

    def create_new_execution(self, script_name, inputs):
        random_id = uuid.uuid4().hex
        result = self._pool.apply_async(worker, (script_name, inputs, random_id), callback=self.log_job_completed)
        result_dictionary[random_id] = result
        return random_id

    def log_job_completed(self, result):
        self.logger.info("Outputs:" + str(result))
        # print("Outputs:", result)

    def get_execution_state(self, execution_id):
        if result_dictionary[execution_id].ready():
            return result_dictionary[execution_id].get()
        else:
            return 'RUNNING'
