import os
import subprocess
import re
from shutil import copyfile,copy

# recursos propios
from jkPyLaTeX import LatexCommand , LatexPackage , PACKAGES
from jkPyLaTeX import CMD_LATEX, LatexDoc
'''
El modo de uso consiste en declarar los comandos a usar y la 
clase se encargaría de administrar los paquetes
'''

class LatexImg(LatexDoc):
  '''
  Encapsula un fichero latex
  '''
  __version='0.1'
  def __init__(self,name,**kwargs):
    super(LatexImg,self).__init__(name,**kwargs)
    #Se debe agregar porque está oculta para una clase que hereda
    self.__docIni=None 


  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def save(self,fnameDir='./'):
    '''
    Guarda el documento en la carpeta especificada
    el documento es único
    '''
    #tree ya no utiliza getTree
    fname=os.path.join(fnameDir,self._name)
    if not ( fname.split(".")[-1]=='tex'):
      fname+=".tex"
    if not os.path.isdir(fnameDir):
      '''
      Si no existe el directorio lo crea
      '''
      os.makedirs(fnameDir)
    self._dirOut=fnameDir
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    #Genera el contenido del archivo
    #Genera el preámbulo
    sP=self.preamble()
    s='%%%%%%%%%%%%%%%%%%%%%\n'
    s+='%%%% LatexImg v'+self.__version
    s+='\n'+sP#agrega el preámbulo
    s+='\n\\begin{document}\n'
    if self._cfg_language != 'english':
      s+='\\selectlanguage{%s}\n'%self._cfg_language
    if self.__docIni != None:
      s+=self.__docIni
    
    if self._mainSlice !=None:
      s+=self.jointSlice()
    s+=self._s+'\n'
    s+='\\end{document}\n'
    with open(fname,'w') as f:
      f.write(s)



