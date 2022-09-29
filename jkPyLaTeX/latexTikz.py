'''
Clases relacionadas con la generación de gráficos utilizando tikz y 
LatexImg
'''
#from jkPyLaTeX import LatexImg, newDocCfg

import math

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class  ShapeTikz(object):
  '''
    Clase que permiten dibujar en el 
    ambiente tikzpicture utilizando draw
  '''
    #patrones de linea válidos
  _line_pattern=('solid','dashed', 'dotted', "dashdotted", 
  "densely dotted", "loosely dotted", "double" )
  def __init__(self,**kwargs):
    self._cmd='draw'
    if 'cmd' in kwargs:
      self._cmd=kwargs['cmd']
      del kwargs['cmd']
    
    self._env=None
    if 'env' in kwargs:
      if isinstance(kwargs['env'], TikzPicture):
        self._env=kwargs['env']
        del kwargs['env']
      else:
        raise Exception('env debe ser TikzPicture')
    self._first_call=True #Utilizado en scope
    self._opt_line_width='' #0.5pt
    self._opt_line_cap=''
    self._opt_line_join=''
    self._opt_draw_color=''
    self._opt_fill_color=''
    self._opt_color=''
    self._opt_top_color=''
    self._opt_bottom_color=''
    self._opt_left_color=''
    self._opt_right_color=''
    self._opt_shading_angle=''
    self._opt_opacity=''
    
    #patrones de linea
    self._opt_line_pattern=''
    self._opt_dash_pattern=''
    #El inicio puede ser <
    self._opt_start_marker=''
    self._opt_end_marker=''
    self._opt_mid_marker=''#Raya
    
    
    self._opt_fill_rule=''
    self._opt_pattern='' #podría requerir el uso del paquete de patrones
    self._opt_pattern_color=''
    
    self._opt_yshift=''
    self._opt_xshift=''
    self._opt_rotate=''
    
    self._opt_scale=''
    self._opt_clip=''
    
    self._opt_options="" #especial que se agrega al final
    self.SetOptions(**kwargs)

  def SetOptions(self,**kwargs):
    for k, v in kwargs.items():
      nameParam='_opt_'+k
      if hasattr(self,nameParam):
        setattr(self,nameParam,v)
      else:
        raise Exception("Error: %s don't have the param '%s'."%(type(self).__name__,k) )
    self.GenOptions()

  def GenOptions(self):
    '''
    Genera las opciones cada que se requiera
    '''
    s='\\%s'%self._cmd
    so=''
    if self._opt_start_marker!='' or self._opt_end_marker!='':
      self._opt_mid_marker='-'
    so=self._opt_start_marker+self._opt_mid_marker+self._opt_end_marker
    #Opciones básicas de asignar valor
    for opt in ('line width', 'opacity', 'dash pattern',
      'pattern', 'pattern color','top color', 'left color',
      'right color', 'bottom color', 'shading angle',
       'rotate', 'yshift','xshift',
      'line cap','line join', 'scale'):
      optName= '_opt_'+opt.replace(' ','_')
      value= getattr(self, optName)
      if value!= '':
        so+=', %s= %s'%( opt, str(value))
    #Se modificaron para dar mas claridad al nombre del parámtero
    for opt in ('draw','fill'):
      optName= '_opt_'+opt.replace(' ','_')+'_color'
      value= getattr(self, optName)
      if value!= '':
        so+=', %s= %s'%( opt, str(value))

    
    if self._opt_color != '':
      so+=', '+self._opt_color
    if self._opt_fill_rule != '':
      if self._opt_fill_rule =='even odd rule':
        so+=', even odd rule';
      else:
        raise Exception( 'fill_rule: solo puede ser "even odd rule"')
    if self._opt_line_pattern !='':
      if self._opt_line_pattern in self._line_pattern:
        so+=', dashed'
      else:
        raise Exception('Error: line pattern "%s" invalid'%self._opt_line_pattern)
    if self._opt_clip !='':
      if so !='':
        raise Exception('clip debe ser un parámetro único')
      so+=', clip'
    
    if self._opt_options != "":
      so+=","+self._opt_options
    if so != '':
      if so[0]==',':
        so=so[1:]#Elimina si hay una coma extra
      s+='[%s]'%so
    s+=' '
    self._options=s
    
  def __call__(self,*args,**kwargs):
#    scope=False
#    if 'scope' in kwargs:
#      kwargs['scope']
    s=self.call(*args,**kwargs)
    if isinstance(s,ShapeTikz):
      # Filtra scope que retornan a si misma
      # para configurar mejor el env donde se 
      # inicia dicho entorno
      return s
    if self._env !=None:
      if self._cmd !='':
        s=self._options+s+';\n'
      self._env.append(s)
    return s
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class TikzPicture(object):
  '''
  Esta clase se utiliza para evitar verbosidad al dibujar, funciona como un 
  canvaz, pero básicamente es un string sobre el que se van escribiendo
  los comandos cada vez que se los llama
  
  Se tiene la función SetOn, SetOff para habilitar y deshabilitar la 
  escritura en el entorno, esto es importante para evitar la 
  duplicación de información cuando se utiliza el entorno scope
  '''
  def __init__(self, options=''):
    self.__base='\\begin{tikzpicture}'
    if options !='':
      self.__base+='[%s]'%options
    self.__base+='\n'
    self.__on=True
    self.__s=self.__base

  def SetOn(self):
    self.__on=True
  def SetOff(self):
    self.__on=False
    
  def append(self, s):
    '''
    Agrega contenido al ambiente
    '''
    if self.__on:
      self.__s+=s
  
  def Clear(self):
    '''
    Borra todo el contenido
    excepto la configuración
    '''
    self.__s=self.__base
  def __call__(self):
    self.__s+='\n\\end{tikzpicture}\n'
    return self.__s
  
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LineTikz(ShapeTikz):
  '''
  Dibuja una linea a partir de una lista de puntos, una instancia
  se crea con el fin de definir un estilo de linea, pues 
  con su llamada mediante la lista de puntos, esta dibujará
  los puntos
  '''
  def call(self, points):
    '''
    Toma la lista o tupla de puntos para 
    '''
    if not isinstance(points,(tuple, list)):
      raise Exception('Error: se requiere una lista o tupla de los puntos a dibujar')
    s=''
    contiguos=True
    for x, y in points:
      # Filtra los puntos que no se pueden graficar haciendo x None
      # para normalizar la lógica que trabaja con la inserción de puntos
      # a plotear
      if y == None or isinstance(y,complex) or isinstance(x,complex):
        x = None

      if s!='':
        if x !=None and contiguos:
          # Para indicar que no está unida la linea
          s+=' -- '
        elif x == None and contiguos:
          contiguos= False
          
        elif x != None and not contiguos:
          contiguos = True
        

      if x == None:
        # Si hay un punto vacío lo salta
        continue
      if isinstance(x,int):
        s+='(%i,'%x
      elif isinstance(x,float):
        s+='(%.5f,'%x
      else:
        s+='(%s,'%str(x)
      if isinstance(y,int):
        s+='%i)'%y
      elif isinstance(y,float):
        s+='%.5f)'%y
      else:
        s+='%s)'%str(y)
    s+=' '
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CircleTikz(ShapeTikz):
  def call(self,center,radius):
    '''
    Crea un radio con el estilo que se defina
    '''
    #s=self._options
    #Centro
    xc,yc= center
    s='(%s,%s) circle '%(str(xc),str(yc))
    #radio
    s+='(%s) '%str(radius)
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class EllipseTikz(ShapeTikz):
  def call(self, center, axisA,axisB):
    #s=self._options
    #Centro
    xc,yc= center
    s='(%s,%s) ellipse '%(str(xc),str(yc))
    #radio
    s+='(%s and %s) '%(str(axisA), str(axisB) )
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class ArcTikz(ShapeTikz):
  def call(self, posInit, startAngle, endAngle,radius, initAsCenter=False):
    '''
    initAsCenter es un parámetro adicional para indicar que 
    el punto de inicio es conciderado como el centro del círculo
    del cual se diburá el arco
    '''
    #s=self._options
    #Centro
    xc,yc= posInit
    s = ""
    if initAsCenter:
      s = '(%s,%s) -- '%(str(xc),str(yc))
      radAngle=startAngle*math.pi/180
      xc+=math.cos(radAngle)*radius
      yc+=math.sin(radAngle)*radius
    s+='(%s,%s) arc '%(str(xc),str(yc))
    #radio
    s+='(%s:%s : %s) '%(str(startAngle), str(endAngle), str(radius) )
    if initAsCenter:
      s+= " cycle"
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class RectangleTikz(ShapeTikz):
  def call(self, cornerA, cornerB):
    '''
    se debe indicar las coordendas de las esquinas del rectángulo
    cornerA: esquina inferior izquierda
    cornerB: esquina superior derecha
    '''
    #s=self._options
    xc,yc=cornerA
    s='(%s,%s) rectangle '%(str(xc),str(yc))
    xc,yc=cornerB
    s+='(%s,%s) '%(str(xc),str(yc))
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class NodeDrawTikz(ShapeTikz):
  def call(self, pos, content,options=''):
    '''
    se debe indicar las coordendas de donde ubicar el nodo, y es opcional 
    dar opciones
    pos: posición del nodo
    content: contenido del nodo
    '''
    #s=self._options
    xc,yc=pos
    s='(%s,%s) node'%(str(xc),str(yc))
    if options !='':
      s+='[%s]'%options
    s+='{%s}'%content
    return s
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class DrawTikz(ShapeTikz):
  def call(self,content):
    '''
    Utilizado para utilizar las instancias que se utilizaron en su modalidad 
    cmd='', para así construir en un solo draw varios elementos compuestos
    '''
    #print( content)
    return content
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class ScopeTikz(ShapeTikz):
  def call(self, content=''):
    '''
    Para utilizar una instancia se debe llamar dos veces scope()(<argumentos>).
    
    En la primera llamada apaga el entorno TikzPicture para que 
    no se duplique el contenido, y en la segunda llamada ya 
    se prende el entorno, y se vuelve _first_call a True
    '''
    self._cmd=''
    if self._first_call:
      self._first_call=False
      if content != '':
        raise Exception('  Error: la primera llamada  de scope siempre debe ser vacía')
      self._env.SetOff()
      return self
    s=self._options.replace('\\draw','\\begin{scope}')
    s+='\n'+content
    s+='\n\\end{scope};\n'
    if self._env != None:
      self._env.SetOn()
    self._first_call=True #Para poder reutilizar el scope
    return s

