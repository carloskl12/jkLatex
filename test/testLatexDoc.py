import math
import sys, time
import unittest
import random

from jkPyLaTeX import LatexDoc, LatexEnvironment, LatexPackage
from jkPyLaTeX import  ldtTaller, ldtParcial, newDocCfg

from test import setupLogger
logger =setupLogger(__name__)

class TestLatexDoc(unittest.TestCase):
  def test_BasicUse(self):
    '''
    Testeando el uso de comandos latex
    '''
    logger.info('\n%%% TestLatexDoc: Prueba  de uso de LatexDoc.')
    # Carga una configuracion y la ajusta
    config= newDocCfg('BASE')
    config['language']='spanish'
    config['lhead']='Encabezado izquierdo'
    config['lfoot']='Pie de página izquierdo'
    doc=LatexDoc('test',**config)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Declara el uso de un comando para actualizar
    # la lista de paquetes requeridos en el preámbulo
    section=doc.useCmd('section')
    equation=doc.useCmd('equation')
    mangle=doc.useCmd('measuredangle')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cAbs=doc.newcommand('abs','\\ensuremath{\\left|#1\\right|}',1)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Escribe en el cuerpo del documento
    doc(section('Sección inicial'))
    doc('\nTexto dentro del documento, a continuación una ecuación:')
    doc( equation('x^2+3x=10'))
    doc(
    'Ahora se presenta un ángulo $'+
    mangle()+' a=30$, el uso de valor absoluto\n'+
    cAbs('x^3-2')
    )
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Guarda el documento
    doc.save('./texOut/')
    # Genera el documento pdf
    doc.genDoc('./texOut/')
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

  def test_taller(self):
    logger.info('\n%%% TestLatexDoc: Prueba  de uso del formato taller.')
    # Carga una configuracion y la ajusta
    doc=ldtTaller('test','Teoría básica de conjuntos','Fundamentos de Matemáticas','')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Declara el uso de un comando para actualizar
    # la lista de paquetes requeridos en el preámbulo
    section=doc.useCmd('section')
    equation=doc.useCmd('equation')
    mangle=doc.useCmd('measuredangle')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    cAbs=doc.newcommand('abs','\\ensuremath{\\left|#1\\right|}',1)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Escribe en el cuerpo del documento
    doc(section('Sección inicial'))
    doc('\nTexto dentro del documento, a continuación una ecuación:')
    doc( equation('x^2+3x=10'))
    doc(
    'Ahora se presenta un ángulo $'+
    mangle()+' a=30$, el uso de valor absoluto\n'+
     '\\abs{ x^3-2}'
    )
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Guarda el documento
    doc.save('./texOut/')
    # Genera el documento pdf
    doc.genDoc('./texOut/')
    
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def test_parcial(self):
    logger.info('\n%%% TestLatexDoc: Prueba  de uso del formato parcial.')
    # Carga una configuracion y la ajusta
    doc=ldtParcial('test')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Declara el uso de un comando para actualizar
    # la lista de paquetes requeridos en el preámbulo
    enum=doc.useCmd('enumerate')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Escribe en el cuerpo del documento
    s=''
    for i in range(20):
      s+='\\item Ejercicio %i\n'%i
    doc(enum( s ))
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Guarda el documento
    doc.save('./texOut/')
    # Genera el documento pdf
    doc.genDoc('./texOut/')
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def test_parser(self):
    logger.info('\n%%% TestLatexDoc: Prueba  de uso del parser de comandos.')
    doc=ldtTaller('test','Teoría básica de conjuntos','Fundamentos de Matemáticas','')
    sentencia="\\vecijk{2}{+3}{-5}"
    doc.cmdParser(sentencia)
    doc('Se escribe un ejemplo de vectores $'+sentencia+'$')
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Guarda el documento
    doc.save('./texOut/')
    # Genera el documento pdf
    doc.genDoc('./texOut/')
  
  def test_slice(self):
    logger.info('\n%%% TestLatexDoc: Prueba  de uso de slices.')
    doc=ldtTaller('test','Teoría básica de conjuntos','Fundamentos de Matemáticas','')
    pytex="""
    Documento principal de pytex desde donde se llamarán
    slices o fragmentos de codigo latex \\usepytex{primerCodigo}
    y ahora llamaré la ecuación \\usepytex{equation}, y puedo 
    llamar nuevamente algo que ya use antes \\usepytex{primerCodigo}
    """
    primerCodigo="$3^2=%i$"%(3**2)
    equation="$3x+5x=%ix$"%(3+5)
    doc.addSlice('primerCodigo',primerCodigo)
    doc.addSlice('equation', equation)
    
    #Dado que el mainSlice debe ser un documento externo
    #Se guardará el documento
    fnameMainSlice='./mainPyTeX.tex'
    with open(fnameMainSlice,'w') as f:
      f.write(pytex)
    doc.setMainSlice(fnameMainSlice)
    doc.save('./texOut/')
    doc.genDoc('./texOut/')
    
