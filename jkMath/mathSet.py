class MathSet (object):
  '''
  Clase para trabajar con operaciones en conjuntos de forma 
  sencilla
  
  A+B : A unión B
  A*B : A intersección B
  A-B : A diferencia de B
  A%B : A diferencia simétrica de B
  A < B: A subconjunto de B
  A > B: A superconjunto de B
  
  '''
  def __init__(self, *args):
    self._set= set(args)
    #print('  content=',self._set)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __add__(self, other):
    return self.operation('union',other)
  
  def __sub__(self,other):
    return self.operation('difference',other)
  
  def __mod__(self,other):#diferencia simétrica
    return self.operation('sym_difference',other)

  def __mul__(self,other):
    return self.operation('intersection',other)
  
  def __lt__(self,other):
    return self.comparation('issubset',other)
  
  def __gt__(self,other):
    return self.comparation('issuperset',other)

  def __contains__(self,item):
    return item in self._set
  def __len__(self):
    return len(self._set)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __call__(self, theSet):
    '''
    Utilizado para asignar un nuevo conjunto
    '''
    if isinstance(theSet, set):
      self._set=theSet
    else:
      raise Exception('  Solo se admiten conjuntos para generar el MathSet')

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def operation(self, operation, mathset):
    newSet=self._set.copy()
    dicOp={'union':newSet.union, 'intersection':newSet.intersection,
    'difference':newSet.difference, 
    'sym_difference':newSet.symmetric_difference}
    if isinstance(mathset,MathSet):
        newSet=dicOp[operation](mathset._set)
    else:
      raise Exception(' No se puede operar con un objeto tipo "%s"'%type(other).__name__)
    newMathSet=MathSet()
    newMathSet(newSet)
    return newMathSet

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def comparation(self,comp, theSet):
    newSet=self._set.copy()
    dicOp={'issubset':newSet.issubset, 'issuperset':newSet.issuperset}
    value=False
    if isinstance(theSet,MathSet):
      value=dicOp[comp](theSet._set)
    else:
      raise Exception(' No se puede comparar con un objeto tipo "%s"'%type(other).__name__)
    return value

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __str__(self):
    if len(self._set)>0:
      return str(self._set)
    return '{}'

def test():
  A=MathSet(1,2,3,4)
  B=MathSet(3,2,4)
  print('  A:',A, '  B:',B)
  print('  A u B:',A+B)
  print('  A n B:',A*B)
  print('  A - B:', A-B , '  B - A:',B-A)
  print('  A Δ B:', A%B , '  B Δ A:',B%A)
  print('  B is subset A:', B<A, '  A is superset B', A> B)

if __name__ == '__main__':
  test()
