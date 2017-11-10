from __future__ import print_function
from builtins import str
import sys

# sys.path.append('../../..')
from mupif import *
import os
import logging

log = logging.getLogger()
for handler in log.handlers:
    if type(handler) == logging.StreamHandler:
        log.removeHandler(handler)

DEFAULT_INPUTS = {'app3.in': 'app3.in',
                  'application3': './application3'}


def main(inputs=DEFAULT_INPUTS):
    outputs = {"log": "mupif.log"}

    class application1(Application.Application):
        """
        Simple application that generates a property with a value equal to actual time
        """

        def __init__(self, file):
            super(application1, self).__init__(file)
            return

        def getProperty(self, propID, time, objectID=0):
            if (propID == PropertyID.PID_Concentration):
                return Property.Property(self.value, PropertyID.PID_Concentration, ValueType.Scalar, time, propID, 0)
            else:
                raise APIError.APIError('Unknown property ID')

        def solveStep(self, tstep, stageID=0, runInBackground=False):
            time = tstep.getTime()
            self.value = 1.0 * time

        def getCriticalTimeStep(self):
            return 0.1

    class application3(Application.Application):
        """
        Simple application that computes an arithmetical average of mapped property using an external code
        """

        def __init__(self, file):
            # list storing all mapped values from the beginning
            super(application3, self).__init__(file)
            self.values = []

        def getProperty(self, propID, time, objectID=0):
            if (propID == PropertyID.PID_CumulativeConcentration):
                log.debug("Getting property name: %s with ID  %d" % (PropertyID.PID_CumulativeConcentration.name, PropertyID.PID_CumulativeConcentration.value))
                # parse output of application3
                f = open('app3.out', 'r')
                outputs["app3.out"] = "app3.out"
                answer = float(f.readline())
                f.close()
                return Property.Property(answer, PropertyID.PID_CumulativeConcentration, ValueType.Scalar, time, propID, 0)
            else:
                raise APIError.APIError('Unknown property ID')

        def setProperty(self, property, objectID=0):
            if (property.getPropertyID() == PropertyID.PID_Concentration):
                # remember the mapped value
                self.values.append(property.getValue())
            else:
                raise APIError.APIError('Unknown property ID')

        def solveStep(self, tstep, stageID=0, runInBackground=False):
            f = open(inputs['app3.in'], 'w')
            # process list of mapped values and store them into an external file
            for val in self.values:
                f.write(str(val) + '\n')
            f.close()
            # execute external application to compute the average
            os.system(inputs['application3'])

        def getCriticalTimeStep(self):
            return 1.0

    time = 0
    timestepnumber = 0
    targetTime = 10.0

    app1 = application1(None)
    app3 = application3(None)

    while (abs(time - targetTime) > 1.e-6):

        # determine critical time step
        dt = min(app1.getCriticalTimeStep(), app3.getCriticalTimeStep())
        # update time
        time = time + dt
        if (time > targetTime):
            # make sure we reach targetTime at the end
            time = targetTime
        timestepnumber = timestepnumber + 1
        log.debug("Step: %g %g %g " % (timestepnumber, time, dt))
        # create a time step
        istep = TimeStep.TimeStep(time, dt, timestepnumber)

        try:
            # solve problem 1
            app1.solveStep(istep)
            # request Concentration property from app1
            c = app1.getProperty(PropertyID.PID_Concentration, istep)
            # register Concentration property in app3
            app3.setProperty(c)
            # solve second sub-problem
            app3.solveStep(istep)


        except APIError.APIError as e:
            log.error("Following API error occurred:", e)
            break

    prop = app3.getProperty(PropertyID.PID_CumulativeConcentration, istep)
    log.debug("Result: " + str(prop.getValue()))

    if (abs(prop.getValue() - 5.05) <= 1.e-4):
        log.info("Test OK")
    else:
        log.error("Test FAILED")
        sys.exit(1)

    # terminate
    app1.terminate()
    app3.terminate()

    return outputs


if __name__ == '__main__':
    main()
