'''
En este ejemplo se utilizan diferentes clases que permiten realizar 
gráficos utilizando diferentes herramientas de dibujo.

El problema que se soluciona corresponde a dibujar diagramas de Venn 
en problemas que involucran tres conjuntos, para ello se crea una 
función que permite realizar el diagrama de Venn sombreando las 
regiones correspondientes al conjunto resultante luego de aplicar 
cualquier operación con los tres conjuntos.

En este ejemplo es escencial el uso de la clase MathSet que define 
a los conjuntos y las diferentes operaciones sobre los mismos.
'''
import sys, os, math

try:
  from jkPyLaTeX import TikzPicture, litBasico
  from jkPyLaTeX import CircleTikz, NodeDrawTikz, RectangleTikz, DrawTikz
  from jkPyLaTeX import ArcTikz, LineTikz

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
  
  from jkPyLaTeX import TikzPicture, litBasico
  from jkPyLaTeX import CircleTikz, NodeDrawTikz, RectangleTikz, DrawTikz
  from jkPyLaTeX import ArcTikz, LineTikz
  

  from jkMath import MathSet, Vector
  from jkMath import GetVectorFromPolar as polar

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def drawSetABC(env, result,fill='blue!40', nombres=['A','B','C','U'],
  verNombres=False, verEjes=False,verRegiones=False):
  '''
  Dibuja las regiones que están en result en el entorno
   env que debe ser objeto de tipo  TikzPicture
  
  * env: entorno donde se dibuja 
  * result: el conjunto que contiene las regiones a dibujar, el diagrama
    consta de 8 regiones.
  * fill: color con el que se indica la región que se está representando
  * nombres: lista con los nombres para los 3 conjuntos
  * verEjes: habilita graficar los ejes de simetría del gráfico
  * verRegiones: habilita graficar el númmero de las diferentes regiones
  
  Para facilitar lo que se requiera graficar se puede utilizar los 
  conjuntos definidos por MathSet indicando las regiones de que 
  se componen:
  A=MathSet(1,4,7,5)
  B=MathSet(2,5,6,7)
  C=MathSet(3,4,6,7)
  U=MathSet(1,2,3,4,5,6,7,8)
  
  '''
  # Este diccionario se retorna con información para posibles
  # usos para adicionar información adicional a la gráfica
  valores={}
  # Dibujo de tres conjuntos donde sus centros forman 
  # un triángulo equilátero

  gab=0.1 #separación con la base del rectángulo
  if verNombres:
    gab=0.7
  ladoT=1.8 #Lado del triángulo equilátero que se forma al unir los centros
  radio=ladoT
  h=math.sqrt(ladoT**2 - (ladoT/2)**2)

  # Centros de los círculos
  x1=gab+radio
  y1=gab+radio+h

  c1=Vector(x1,y1)
  c2=Vector(x1+ladoT,y1)
  c3=Vector(x1+ladoT/2,gab+radio)
  
  # Ancho y alto del conjunto universal
  ancho, alto= 2*gab+2*radio+ladoT , 2*gab+2*radio+h
  if verNombres:
    alto-=gab/2
  O=(0,0)
  R=(ancho,alto)
  RT=R #Dimensiones del rectángulo de la imágen
  if verNombres:
    RT=(ancho,alto+0.5) 
  valores['c1']=c1
  valores['c2']=c2
  valores['c3']=c3
  valores['R']=R
  valores['RT']=RT
  valores['radio']=radio
  # Calcula posiciones para mostrar el número de 
  # cada región, empieza hallando el centro
  #  para la figura de tres círculos
  reg={}
  reg[7]=(c1+c2+c3)%(1/3)
  reg[1]=reg[7]+polar(radio*1.1,150)
  reg[2]=reg[7]+polar(radio*1.1,30)
  reg[3]=reg[7]+polar(radio*1.1,-90)
  reg[4]=reg[7]+polar(radio*0.8,210)
  reg[5]=reg[7]+polar(radio*.75,90)
  reg[6]=reg[7]+polar(radio*.75,-30)
  valores['regiones']=reg
  # crea las instancias para dibujar
  lw=1.
  circle= CircleTikz(env=tikzpicture,line_width=lw)
  rectangle= RectangleTikz(env=tikzpicture,line_width=lw)
  rectangleClip=RectangleTikz(env=tikzpicture,clip=True)
  node= NodeDrawTikz(env=tikzpicture)
  
  # Para utilizar draw se requieren objetos sin entorno
  draw= DrawTikz(env=tikzpicture, fill_color=fill, fill_rule='even odd rule')
  drectangle= RectangleTikz(cmd='')
  darc= ArcTikz(cmd='')
  
  # Recorta solo la región de interés
  #rectangleClip(O,RT)
  
  if 1 in result:
    draw( darc(c1,60,240,radio,True) 
      +darc(c3,180,120,radio,True)
      +darc(c2,180,120,radio,True)
    )
  if 2 in result:
    draw( darc(c2,-60,120,radio,True)+' -- '
    +darc(c1,60,0,radio,True)
    +darc(c3,0,60,radio,True)
      
    )
  if 3 in result:
    draw( darc(c1,240,300,radio,True) 
      +darc(c2,240,300,radio,True)
      +darc(c3,360,180,radio,True)
    )
  if 4 in result:
    draw( darc(c1,240,300,radio,True)+' -- '
    +darc(c2,240,180,radio,True)
    +darc(c3,120,180,radio,True)
      
    )
  if 5 in result:
    draw( darc(c1,0,60,radio,True)+' -- '
    +darc(c2,120,180,radio,True)
    +darc(c3,120,60,radio,True)
      
    )
  if 6 in result:
    draw( darc(c1,360,300,radio,True)+' -- '
    +darc(c2,240,300,radio,True)
    +darc(c3,0,60,radio,True)
    )
  if 7 in result:
    draw( darc(c1,360,300,radio,True)+' -- '
    +darc(c2,240,180,radio,True)
    +darc(c3,120,60,radio,True)
    )
  if 8 in result:
    draw(
    drectangle(O,R)
    +darc(c1,240,60,radio,True) + '--'
    +darc(c2,120,-60,radio,True)+' -- '
    +darc(c3,360,180,radio,True)
    )
  
  circle(c1,radio)
  circle(c2,radio)
  circle(c3,radio)
  rectangle(O,R)
  #Las guias de referencia en el proceso de construcción
  line= LineTikz(env=tikzpicture,line_patern='dashed',draw_color='red',opacity=0.5)
  
  vecUnitarios={}
  for k, v in reg.items():
    
    if v != reg[7]:
      #Vector de recorrido
      vr=reg[7]-v
      vru=vr%(1/abs(vr))
      vecUnitarios[k]=vru
      rv,av= vru.ConvertTo('polar')
      if av <0:
        av+=360
      #print( '  vru:', vru*vru)
      if verEjes:
        vr=vru%(radio*2)+reg[7]
        line( [reg[7], vr ] )
        vr=vru%(radio*2.3)+reg[7]
        node(vr,'%.0f'%av)
    if verRegiones:
      node(v,str(k) )
  if verNombres:
    node( (ancho/2,alto+0.3),nombres[3])
    node( (ancho/2,alto+0.3),nombres[3])
    vr=vecUnitarios[1]%(radio*1.75)+reg[7]
    node( vr, nombres[0])
    vr=vecUnitarios[2]%(radio*1.75)+reg[7]
    node( vr, nombres[1])
    vr=vecUnitarios[3]%(radio*1.75)+reg[7]
    node( vr, nombres[2])
  return valores
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Realiza el dibujo
fig=litBasico('conjuntos')

#Obtiene una instancia para manejar el entorno de tikzpicture
tikzpicture=TikzPicture('scale=1')


name='ejA'

A=MathSet(1,4,7,5)
B=MathSet(2,5,6,7)
C=MathSet(3,4,6,7)
U=MathSet(1,2,3,4,5,6,7,8)

valores=drawSetABC(tikzpicture,A+B-(U-C), verNombres=False, verRegiones=False, nombres=['E','L','B','U'])

node= NodeDrawTikz(env=tikzpicture)
nombres={1:7, 2: 11, 3:13, 4:5, 5: 6, 6:4, 7:2}
for r, pos in valores['regiones'].items():
  node(pos,str(nombres[r]) )

fig(tikzpicture())

fig._name=name
fig.save('./')
fig.genDoc(target=True)

