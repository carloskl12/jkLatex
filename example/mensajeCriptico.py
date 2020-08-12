'''
En este ejemplo  se muestra como se pueden facilitar ciertas tareas de 
dibujo utilizando python para coordinar el gráfico de un mensaje 
cifrado que utiliza un conjunto de carácteres particulares, lo que 
se busca con el script es generar de manera rápida visualizaciones de 
posibles reemplazos de letras para los diferentes carácteres.

El mensaje realmente es desconocido, y contiene un mensaje que siempre
he querido averiguar, pero a día de hoy aún sigo sin lograrlo, y según 
mi poco entendimiento hay muy poca información para poder descifrar el 
mensaje, aunque el problema si es útil para mostrar el potencial para 
integrar la generación de gráficos a python utilizando la librería 
tikz de latex
'''
import sys, os

try:
  from jkPyLaTeX import LineTikz, NodeDrawTikz, RectangleTikz
  from jkPyLaTeX import TikzPicture, litBasico

  from jkMath import MathSet, Vector
  from jkMath import GetVectorFromPolar as polar
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
  
  from jkPyLaTeX import LineTikz, NodeDrawTikz, RectangleTikz
  from jkPyLaTeX import TikzPicture, litBasico

  from jkMath import MathSet, Vector
  from jkMath import GetVectorFromPolar as polar
  

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Realiza el dibujo
fig=litBasico('mensajeCriptico')

#Obtiene una instancia para manejar el entorno de tikzpicture
tikzpicture=TikzPicture('scale=1')

rectangle=RectangleTikz(env=tikzpicture)
node=NodeDrawTikz(env=tikzpicture)
line=LineTikz(env=tikzpicture,line_width=1)

#Lineas de los carácteres
keys={}
keys[1]=[(0,0.5),(0,0),(1,0),(1,0.5)]
keys[2]=[(0.2,0),(0.2,0.5),(0,0.5),(1,0.5),(None,None),(0.8,1),(0.8,0)]
keys[3]=[(0.8,0),(0.8,0.5),(0.2,0.7),(0.8,1),(0.8,0.7)]
keys[4]=[(0.8,0),(0.2,0.3),(0.8,0.5),(0.8,1)]
keys[5]=[(0,0.3),(0,-0.1),(None,None),(0,0),(1,0),(1,0.5)]#parece la 1
keys[6]=[(0.2,0.3),(0.8,0.3)]
keys[7]=[(0,0),(0.6,0),(0.6,0.5),(1,0.5)]
keys[8]=[(0,0),(1,0),(None,None),(0.2,0.5),(0.5,0.5),(0.5,0)]
keys[9]=[(0.25,1),(0.25,0.5),(0.75,0.5),(0.75,0)]
keys[10]=[(0,0),(0,0.5),(0.5,0.5),(0.5,0),(1,0),(1,0.5)]
keys[11]=[(0.25,0.8),(0,0.4),(0.35,0),(0.65,0),(1,0.4),(0.75,0.8),(None,None),(0.5,0.2),(0.5,0)]
keys[12]=[(0,0.5),(1,0.5),(None,None),(0.5,0.5),(0.5,0),(0.8,0)]
keys[13]=[(0,0.6),(0,0),(0.5,0),(0.5,0.5),(1,0.5)]
keys[14]=[(0,0.5),(1,0.5),(1,0),(0.4,0),(0.4,0.5)]
keys[15]=[(0.1,0),(0.9,0),(0.9,0.5),(0.1,0.5),(0.1,0)]
keys[16]=[(0.6,0),(0.6,1),(None,None),(0.35,0.5),(0.6,0.5)]
keys[17]=[(0.1,0),(0.9,0),(0.9,0.5),(0.1,0.5),(0.1,0),(0.35,0),(0.35,0.5),(0.65,0.5),(0.65,0)]
keys[18]=[(0.2,0.9),(0.2,0.5),(0.8,0.2),(0.8,0),(0.8,0.8)]
keys[19]=[(0,0.5),(0.5,0),(0.5,0.5),(0.5,0),(1,0.5),(1,0.8)]
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Equivalencias
# en el papel fuente
equiv={}
equiv[2]='e'
#equiv[15]='r'
equiv[4]='d'
equiv[0]=' '
# Equivalencias de carácteres que se quieran probar
equiv[2]='a'
equiv[4]='d'
equiv[11]='a'

equiv[4]='l'
equiv[11]='s'
equiv[5]='u'

#equiv[8]='r'
#equiv[3]='t'
#equiv[12]='u' #altamente probable
#equiv[18]='t'
#equiv[16]='p'
#equiv[3]='y'
#equiv[8]='n'
#equiv[19]='a'
#equiv[11]='a'
#equiv[13]='i'
#equiv[5]='o'
#equiv[6]='f'
#equiv[14]='v'


def transf( points, xoff,yoff , scale=0.5):
  '''
  Escala y traslada un carácter dado por sus 
  puntos en points a una coordenad xoff,yoff.
  
  En points si hay puntos (None,None) no se 
  dibuja el trazo  y se continua con un nuevo 
  trazo. En tikz corresponde a no unir los 
  puntos con --.
  '''
  p=[]
  for x,y in points:
    if x ==None:
      p.append((x,y))
    else:
      p.append( (x*scale+xoff,y*scale+yoff) )
  return p

i=0
for k, key in keys.items():
  key=transf(key,i+0.25,4.3)
  line(key)
  value=k
  if k in equiv:
    value='%i=%s'%(k,equiv[k])
  node((k-0.5,3.9),value, options='scale=0.9,red')
  i+=1

#0 indica espacio
texto=[[1,0,2,3,4,0,5,2,0,6,4,0,7,4,8,9],
[0,0,0,10,11,2,3,12,8,11,4],
[4,13,11,0,6,5,2,0,14,11,8,5,0,18,19,15,4,2],
[16,12,2,4,2,0,17]
]

repeticiones={}
for k in keys:
  repeticiones[k]=0


#%%%%%%%%%%%%%%%%%%%%%%
descifrado=[]
for il, fila in enumerate(texto):
  row=[]
  for ic, code in enumerate(fila):
    if code>0:
      repeticiones[code]+=1
      key=transf(keys[code],ic+0.25,2.5-il)
      line(key)
    value=code
    if code in equiv:
      value=equiv[code]
      row.append(value)
    else:
      row.append('\\_')
    node((ic+0.5,2.15-il),value,options='scale=0.8,blue')
    
  descifrado.append(row)

descifrado=[''.join(r) for r in descifrado]
for il, r in enumerate(descifrado):
  node((10,-1.4-il),r,options='scale=2.5,green!80!black')

# Ordena las repeticiones para
repeticiones=[(k,v) for k,v in repeticiones.items()]
repeticiones.sort(key=lambda arg:-arg[1])

# Mostrará los carácteres por orden de importancia
for ik, rp in enumerate(repeticiones):
  code,count=rp
  key=keys[code]
  key=transf(key,ik+0.25,-6.7)
  line(key)
  value=count
  if code in equiv:
    value='%i(%s)'%(count,equiv[code])
  node((ik+0.5,-7.3),value, options='scale=1,black')

#print(repeticiones)
ancho=19
alto=5
O=Vector(0,-8)
R=Vector(ancho,alto)

rectangle(O,R)
#print( key)


fig(tikzpicture())
fig.save('./')
fig.genDoc(target=True)


