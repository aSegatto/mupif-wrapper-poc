#!/usr/bin/env python
from __future__ import print_function
from builtins import range
#
# This example requires pyvtk module, install it using
# pip install pyvtk
# Note: pyvtk is only available in Python 2.x (Sept, 2014)
#
import sys

sys.path.append('../../..')
from mupif import *
import logging

log = logging.getLogger()
for handler in log.handlers:
    if type(handler) == logging.StreamHandler:
        log.removeHandler(handler)

DEFAULT_INPUTS = {}


def main(inputs=DEFAULT_INPUTS):
    outputs = {'log': 'mupif.log'}

    # generate field and corresponding mesh
    mesh = Mesh.UnstructuredMesh()
    vertices = []
    values1 = []
    values2 = []
    num = 0
    for i in range(40):
        for j in range(15):
            vertices.append(Vertex.Vertex((i * 15) + j, (i * 15) + j + 1, (float(i), float(j), 0.0)))
            values1.append((num,))
            num += 0.5
    cells = []
    num = 0
    for i in range(39):
        for j in range(14):
            cells.append(Cell.Quad_2d_lin(mesh, num, num, ((i * 15) + j, (i + 1) * 15 + j, (i + 1) * 15 + j + 1, ((i * 15) + j + 1))))
            values2.append((num,))
            num += 1

    mesh.setup(vertices, cells)

    # Check saving a mesh
    mesh.dumpToLocalFile('mesh.dat')
    outputs['mesh'] = 'mesh.dat'
    Mesh.Mesh.loadFromLocalFile('mesh.dat')

    # field1 is vertex based, i.e., field values are provided at vertices
    field1 = Field.Field(mesh, FieldID.FID_Temperature, ValueType.Scalar, None, None, values1)
    # field1.field2Image2D(title='Field', barFormatNum='%.0f')
    # field2 is cell based, i.e., field values are provided for cells
    field2 = Field.Field(mesh, FieldID.FID_Temperature, ValueType.Scalar, None, None, values2, Field.FieldType.FT_cellBased)

    # evaluate field at given point
    position = (20.1, 7.5, 0.0)
    value1 = field1.evaluate(position)  # correct answer 154.5
    log.debug("Field1 value at position " + str(position) + " is " + str(value1))
    position = (20.1, 8.5, 0.0)
    value2 = field2.evaluate(position)  # correct answer 287.0
    log.debug("Field2 value at position " + str(position) + " is " + str(value2))

    field1.field2VTKData().tofile('example1')
    field2.field2VTKData().tofile('example2')
    outputs['example1'] = 'example1.vtk'
    outputs['example2'] = 'example2.vtk'

    # Test pickle module - serialization
    field1.dumpToLocalFile('field.dat')
    outputs['field'] = 'field.dat'
    field3 = Field.Field.loadFromLocalFile('field.dat')
    position = (20.1, 9.5, 0.0)
    value3 = field3.evaluate(position)  # correct answer 155.5

    if ((abs(value1[0] - 154.5) <= 1.e-4) and (abs(value2[0] - 288.0) <= 1.e-4) and (abs(value3[0] - 155.5) <= 1.e-4)):
        log.info("Test OK")
    else:
        log.error("Test FAILED")
        import sys
        sys.exit(1)

    return outputs


if __name__ == '__main__':
    main()
