import sys, os, math

try:
  from jkPyLaTeX import TikzPicture, litBasico
  from jkPyLaTeX import CircleTikz
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
  
  from jkPyLaTeX import TikzPicture, litBasico
  from jkPyLaTeX import CircleTikz


#Crea el documento
fig=litBasico('nombreFigura')

#Obtiene una instancia para manejar el entorno de tikzpicture
tikzpicture=TikzPicture()
#Crea una instancia para dibujar un círculo con parámetros por defecto
circle=CircleTikz(env=tikzpicture)
#Crea una instancia para dibujar rellenando la figura con color azul
circle2=CircleTikz(env=tikzpicture,fill_color='blue')
#dibuja un círuclo con centro en (1,1) cuyo radio es 1
circle((1,1),1)
#Segúndo círculo que se rellena con color azul
circle2((2,1),1)

#Genera el codigo del gráfico y se guarda en el documento
fig(tikzpicture())

#Guarda el documento latex
fig.save('./')
#Compila el código
fig.genDoc(target=True)
