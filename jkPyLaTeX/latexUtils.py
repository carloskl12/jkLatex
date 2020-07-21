'''
Funcionalidades para el manejo de documentos en LaTex


'''


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LatexCommand(object):
  '''
  Clase utilizada para definir un comando latex
  
  Los comandos se deben utilizar dentro de un entorno para que 
  se escriba el resultado de forma automática
  '''
  def __init__(self, name, body,numargs=0,package='default',info=''):
    self._name=name
    self._numargs=numargs
    self._body=body
    self._package=package
    self._info=info
    
  def __str__(self):
    return 'command {}'.format(self._name)
  
  @property
  def name(self):
    return self._name
  
  @property
  def numargs(self):
    return self._numargs
  
  @property
  def body(self):
    return self._body

  @property
  def package(self):
    return self._package

  @property
  def info(self):
    return self._info
 
  def declara(self):
    '''
    Retorna el modo de la declaración del comando
    '''
    s='\\newcommand{\\%s}'%self._name
    if self._numargs >0:
      s+='[%i]'%self._numargs
    s+="{%s}"%self._body
    return s
    
  def __call__(self,*args):
    '''
    Retorna el string con el uso del comando dados los parámetros 
    del comando
    '''
    s='\\%s'%self._name
    if len(args)==2:
      # Se verifica si está en modo opciones que consiste en
      # pasar como argumentos dos tuplas, la primera con las opciones
      # y la segunda con los argumentos
      if isinstance(args[0],tuple) :
        s+='['
        for i, opt in enumerate(args[0]):
          if i>0:
            s+=','
          s+=str(opt)
        s+=']'
        if isinstance(args[1],tuple):
          args=args[1]
        else:
          args=(args[1],)
    if self._numargs >0:
      if self._numargs == len(args):
        for i,arg in enumerate(args):
          s+="{%s}"%str(arg)
      else:
        raise Exception('El número de argumentos no es correcto')
    return s
    
  def __add__(self,other):
    '''
    Sobreescrible el comportamiento con el símbolo +
    
    revisar: https://www.programiz.com/python-programming/operator-overloading
    '''
    if self._numargs == 0:
      if isinstance(other, LatexCommand):
        if other.numargs == 0:
          return (self()+other())
        else:
          raise Exception('El comando "%s" requiere argumentos'%other.name)
      elif isinstance(other, str):
        return (self()+other)
      else:
        raise Exception('Imposible concatenarse con un objeto de tipo %s '%str(type(other)))
    else:
      raise Exception('El comando "%s" requiere argumentos para utilizarse '%self.name)
      
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LatexEnvironment(LatexCommand):
  '''
  Declaracion de un ambiente o entorno
  '''
  def __call__(self, content,*args,**kwargs):
    s="\n\\begin{%s}"%self._name
    if 'options' in kwargs:
      if isinstance( kwargs['options'], (str,int)):
        s+='[%s]'%str(kwargs['options'])
      elif isinstance(kwargs['options'],(list,tuple)):
        s+='['
        for i, v in enumerate(kwargs['options']):
          if i>0:
            s+=','
          s+=str(v)
        s+=']'
    if len(args)>0:
      for i,arg in enumerate(args):
        s+="{%s}"%str(arg)
    
    s+='\n%s'%content
    s+='\n\\end{%s}\n'%self._name
    return s

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LatexPackage(object):
  '''
  clase que encapsula un paquete de latex, sirve para almacenar los comandos
  y detalles de los casos en que se usa un paquete particular, el cual 
  debe heredar de esta clase
  
  orderLeft: una lista con los nombres de los paquetes que deben ir primero
  orderRight: una lista con los nombres de los paquetes que deben ir luego
  '''
  def __init__(self, name,comment="",orderLeft=[],orderRight=[]):
    self._name = name
    self._commands={}
    self._comment=""
    self._orderLeft=orderLeft
    self._orderRight=orderRight
    self._options=None

  @property
  def name(self):
    return self._name
  
  @property
  def comment(self):
    return self._comment
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def add(self, *args):
    '''
    Agrega un comando al paquete
    '''
    command=args[0]
    if len(args)> 1:
      for cmd in args:
        self.add(cmd)
    else:
      if not isinstance(command,LatexCommand):
        if isinstance(command,str):
          #Crea un commando básico con solo el nombre
          command=LatexCommand(command,'',package=self._name)
        elif isinstance(command,tuple):
          #Name, numargs, info
          command=LatexCommand(command[0],'',numargs=command[1],
            package=self._name,info=command[2])
        else:
          raise Exception('Solo se pueden agregar comandos latex al paquete')
      self._commands[command.name]=command
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def addEnv(self,*args):
    '''
    Agrega uno o más entornor al paquete
    '''
    command=args[0]
    if len(args)> 1:
      for cmd in args:
        self.add(cmd)
    else:
      if not isinstance(command,LatexEnvironment):
        if isinstance(command,str):
          #Crea un commando básico con solo el nombre
          command=LatexEnvironment(command,'')
        else:
          raise Exception('Solo se pueden agregar entornos latex')
      self._commands[command.name]=command
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __getitem__(self, key):
    return self._commands[key]

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __contains__(self,command):
    if isinstance(command, LatexCommand):
      command=command.name
    return command in self._commands
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def setOptions(self,options):
    '''
    Define las opciones,
    esto es con el fin de definir 
    las opciones a usar al llamar un paquete 
    luego de declararse
    '''
    if isinstance(options,list):
      self._options=options
    else:
      self._options=[str(options)]

  def addOption(self,option):
    '''
    Agrega una opcion más
    '''
    if self._options == None:
      self._options=[]
    self._options.append(str(option))

  
  def __call__(self, *args):
    '''
    Llamar al paquete genera el modo como se declara 
    en el preambulo
    '''
    s='\\usepackage'
    if len(args) == 0 and isinstance(self._options,list):
      args=self._options
    if len(args)>0:
      s+='['
      for i, arg in enumerate(args):
        if i>0:
          s+=','
        s+=str(arg)
      s+=']'
    s+='{%s}\n'%self._name
    return s

  def __lt__(self,other):
    '''
    self <  other
    '''
    if other in self._orderRight:
      return True
    else:
      return False

  def __gt__(self,other):
    '''
    self > other
    '''
    if other in self._orderLeft:
      return True
    else:
      return False

  def __eq__(self,other):
    '''
    self == other
    '''
    return not ( self < other or self > other)

