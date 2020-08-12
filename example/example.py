#!/usr/bin/python
# script python 3
'''
Este script está hecho para ejecutarse desde el exterior de esta carpeta

>> python example/example.py

En este script se refleja una forma de flujo de trabajo con jkPyLaTeX,
en el cual se tiene un archivo externo con una estructura de documento
que por lo general no suele variar, pero si se requiere cambiar o 
actualizar otra parte.

En este script se muestra como generar un documento utilizado para 
presentar ejercicios de manera muy simplificada.

El logo puede cambiarse por el que se ubique afuera de esta carpeta en formato
pdf con el nombre "logo.pdf"

En este ejemplo se muestra el potencial uso de la librería sympy para 
trabajar con ejercicios de matemáticas.
'''
import sys, os

try:
  from jkPyLaTeX import LatexDoc, ldtTaller
except:
  #Configura para que el paquete jkPyLaTeX sea visible
  #Obtiene directorio relativo donde esta el archivo
  quitar=__file__.replace('/'+__file__.split('/')[-1],'')
  #Obtiene el directorio absoluto
  dir_path = os.path.dirname(os.path.realpath(__file__))
  #Elimina el subdirectorio
  dir_path=dir_path.replace(quitar,'')
  # Agrega el directorio desde donde se invoca el script para tener 
  # acceso a los módulos disponibles en el mismo
  sys.path.insert(0,dir_path)
  from jkPyLaTeX import LatexDoc, ldtTaller


from random import shuffle


from  sympy import symbols, latex, sin ,cos , tan, diff

x= symbols('x')

exercises=''
answers=''
excN=list(range(2,10))
shuffle(excN)
for c in excN:
  eji=  c*x**2+x*cos(c*x)/x
  exercises+='  \\item $%s$'%latex(eji)
  answers+='  \\item $%s$'%latex(diff(eji))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Create the document
doc=ldtTaller('doc','Derivative','Calculus','')
# Add content
doc.addSlice('exercises',exercises)
doc.addSlice('answers',answers)

#template or content
fnameMainSlice='./example/example.tex'
doc.setMainSlice(fnameMainSlice)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#Save the files necessary to compile in ./texOut
doc.save('./texExample/')
#compile with pdflatex
doc.genDoc()












