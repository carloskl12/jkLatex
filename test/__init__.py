'''
modulo de test

Para correr el paquete de test completo
>>> python -m unittest test
Para mostrar la lista de métodos de clase que se ejecutan en los test
>>> python -m unittest -v test

Para correr una clase particular
>>> python -m unittest test.TestClass 

Para ejecutar un método de clase particular
>>> python -m unittest module.Class.test_method
'''
import sys, os,time
import logging
import  subprocess

def setupEnvironment():
  '''
  Instala el entorno de trabajo para probar
  '''
  #Obtiene directorio relativo donde esta el archivo
  quitar=__file__.replace('/'+__file__.split('/')[-1],'')
  #Obtiene el directorio absoluto
  dir_path = os.path.dirname(os.path.realpath(__file__))
  #Elimina el subdirectorio
  dir_path=dir_path.replace(quitar,'')
  # Agrega el directorio desde donde se invoca el script para tener 
  # acceso a los módulos disponibles en el mismo
  sys.path.insert(0,dir_path)

setupEnvironment()
from jkPyLaTeX import JKPYLATEX_VERSION

def setupLogger(name):
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)
  if not len(logger.handlers):
    '''
    En este caso se verifica si ya tiene manejadores activos,
    de no existir, implica que es por primera vez que se configura
    por lo tanto se deben agregar
    '''
    # Imprime la información en terminal
    ch = logging.StreamHandler()
    # Manejador para archivo
    fileHandler = logging.FileHandler('jkPyLaTeX.log')
    # crea un formato
    formatter = logging.Formatter("%(message)s")#Formato sencillo
    # agrega el formato
    ch.setFormatter(formatter)
    fileHandler.setFormatter(formatter)
    
    logger.addHandler(ch)
    logger.addHandler(fileHandler)
    stime= time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    logger.info('*'*35)
    logger.info('**      %s     **'%stime)
    logger.info('**  Pruebas unitarias iniciadas  **')
    logger.info('logger level: DEBUG')
    logger.info('iniciado en : '+name)
    pyversion="%i.%i.%i "%(sys.version_info[0],sys.version_info[1],sys.version_info[2])
    logger.info('python : '+pyversion)
    logger.info('jkPyLaTeX: '+JKPYLATEX_VERSION)
    
    try:
      #Ejecuta make sobre el directorio especificado
      s=subprocess.check_output("pdflatex -version",shell=True,stderr=subprocess.STDOUT)
      s=s.decode('utf8')
      lines=s.split('\n')
      version=lines[0].split(' ')[1:]
      version=' '.join(version)
      logger.info('pdfTeX : '+version)
    except subprocess.CalledProcessError as e:
      #Si se genera un error se imprime la información
      raise RuntimeError(
        "command '{}' return with error (code {}): {}".format(
          e.cmd, e.returncode, e.output.decode('utf8')
        )
      )
    logger.info('')
  return logger

from test.testLatexUtils import TestLatexUtils
from test.testLatexDoc import TestLatexDoc
