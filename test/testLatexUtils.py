import math
import sys,time
import unittest

import random


from jkPyLaTeX import LatexCommand, LatexPackage, LatexEnvironment, LatexDoc
from test import setupLogger
logger =setupLogger(__name__)

class TestLatexUtils(unittest.TestCase):
  def test_LatexCommand(self):
    '''
    Testeando el uso de comandos latex
    '''
    logger.info('%%% LatexUtils: Prueba  de uso de comandos latex.')
    cl_abs=LatexCommand('abs','\\left\\vert#1\\right\\vert',1)
    logger.info(cl_abs.declara())
    logger.info(cl_abs('3x+1'))
    with self.assertRaises(Exception):
      cl_abs()
    #comando sin argumentos
    vui =LatexCommand( 'vui', '\hat{\imath}')
    logger.info(cl_abs('3x+1')+vui())
    logger.info(cl_abs(('option1','option2'), ('-1',) ))
    #Prueba del epaquetamiento de comandos
    pack=LatexPackage('miPaquete')
    pack.add(cl_abs,vui)
    logger.info('vui in pack: '+str(vui in pack))
    logger.info('"vui" in pack: '+str("vui" in pack))
    logger.info('Declara paquete: '+pack())
    

