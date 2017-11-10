import logging
import os
from importlib import import_module
from time import sleep

EXAMPLES_DIR = "examples"


def worker(script_name, inputs, exec_id):
    logger = logging.getLogger(__name__)
    logger.info("Worker working on %s ID: %s" % (script_name, exec_id))
    try:
        logger.info("Worker started work on %s ID: %s" % (script_name, exec_id))
        sleep(10)
        outputs = import_and_run_script(inputs, script_name)

        logger.info("Worker completed work on %s ID: %s" % (script_name, exec_id))
        return outputs
    except FileNotFoundError as err:
        logger.error("Worker completed work on %s ID: %s with error: %s" % (script_name, exec_id, err))
        return {}
    except AttributeError as err:
        logger.error("Worker completed work on %s ID: %s with error: %s" % (script_name, exec_id, err))
        return {}


def import_and_run_script(inputs, script_name):
    os.chdir(os.path.join(EXAMPLES_DIR, script_name))
    script = import_module(EXAMPLES_DIR + "." + script_name + "." + script_name, __name__)
    outputs = script.main(inputs)
    return outputs
