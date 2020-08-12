import math
class Vector(object):
  '''
  Clase para encapsular un vector y trabajar
  con los operadores básicos
  
  '''
  
  def __init__(self,*args):
    self._v=tuple(args)
    self._coordinates='cartesian'
  
  @property
  def coordinates(self):
    return self._coordinates

  def __add__(self, other):
    other=self._verify(other)
    r=[ a+b for a,b in zip(other,self._v)]
    r=Vector(*r)
    return r
  
  def __sub__(self, other):
    other=self._verify(other)
    r=[ a-b for a,b in zip(other,self._v)]
    r=Vector(*r)
    return r
  
  def __mul__(self, other):
    #Producto punto
    other=self._verify(other)
    r=[ a*b for a,b in zip(other,self._v)]
    r=sum(r)
    return r
  
  def __mod__(self,other):
    #Producto escalar
    r= [ v*other for v in self._v]
    return Vector(*r)

  def __getitem__(self,index):
    return self._v[index]

  def __len__(self):
    return len(self._v)
  
  def __abs__(self):
    return math.sqrt(self*self)
    
  def __str__(self):
    return str(self._v)
  def _verify(self,other):
    '''
    Verifica si es posible operar con el vector
    '''
    if isinstance(other,Vector):
      if other.coordinates == self.coordinates:
        if len(other) != len(self):
          raise Exception('  Error: no coincide el espacio de los vectores a operar')
      else:
        # los vectores no coinciden en el tipo de coordendas
        other= other.ConvertTo(self.coordinates)
    else:
      raise Exception('  Error: la operación es válida solo entre vectores')
    return other

  def ConvertTo(self, coordinates):
    result=None
    if coordinates=='polar':
      if len(self)==2:
        r= math.sqrt(self*self)
        #atan2(y,x)
        a=math.atan2(self[1],self[0])
        a*=180/math.pi
        result=(r,a)
      else:
        raise Exception('  conversión no válida')
    else:
      raise Exception('  conversión no existente')
    if result == None:
      raise Exception('  Error del programador')
    return result

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def GetVectorFromPolar( radio, angulo):
  '''
  Retorna el vector correspondiente
  
  radio: radio
  angulo: ángulo en grados sexagesimales
  '''
  angulo= math.pi*angulo/180
  x=radio*math.cos(angulo)
  y=radio*math.sin(angulo)
  return Vector(x,y)
# Por implementar
#class PolarVector(object):
#  '''
#  Vector Constru
#  '''
#  def __init__(self,*args):
#    self._v=tuple(args)
#    self._coordinates='polar'
#    
#  def __add__(self,other):
#    if other.coordinates=='polar':
#      other=other.ConvertTo('cartesian')
#    elif other.coordinates!='cartesian':
#      raise Exception('  Error: imposible sumar con un vector en coordenadas "%s"'%other.coordinates)
#    v=self.ConvertTo('cartesian')
#    r=[ a-b for a,b in zip(other,self._v)]
#    r=Vector(*r)
#    return r
    
  
