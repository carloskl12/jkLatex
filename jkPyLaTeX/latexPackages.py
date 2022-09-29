'''
Paquetes de latex
'''
from jkPyLaTeX import LatexPackage, LatexCommand, LatexEnvironment

PACKAGES={'global':{}}
lpack=[]
lpackNames=[]
def addOrder(name,comment):
  '''
  Agrega los paquetes en el order adecuado
  para que se preserve cuando se llaman los paquetes respectivos
  '''
  if name in lpackNames:
    raise Exception('The package "%s" already exists in lpack.'%name)
  lpackNames.append(name)
  lpack.append((name,comment))

def addPacks():
  '''
  Agrega los paquetes al diccionario de paquetes utilizando el 
  orden según la lista lpack
  '''
  for i, args in enumerate(lpack):
    ordLeft=lpackNames[:i]
    ordRight=lpackNames[i+1:]
    PACKAGES[args[0]]=LatexPackage(args[0],args[1], orderLeft=ordLeft,orderRight=ordRight)
  print('** Hay %i paquetes disponibles en jkPyLaTeX'%len(PACKAGES))

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Se agregan en el orden adecuado
addOrder('babel', 'Manejo de idiomas diferentes al inglés'   )
addOrder('inputenc', 'Permite usar las tildes y la ñ de forma normal' )
addOrder('tikz','Permite hacer gráficos')
addOrder('amsmath', '')
addOrder('amsfonts','')
addOrder('amssymb', 'Simbolos matemáticos')
addOrder('mathtools','Mejora amsmath')
addOrder("xparse","Para utilizar NewDocumentCommand")
addOrder('verbatim',   'Para agregar código de programas'  )
addOrder('layout', 'Se usa para ver la configuracion de pagina .' )
addOrder('multicol',    'varias columnas'  )
addOrder('fancyhdr', 'Encabezados, pie de páginas y notas marginales' )
addOrder('rawfonts',   ''  )
addOrder('graphicx','Solo si se compila con pdflatex' )
addOrder('hyperref', 'Para utilizar vínculos')
addOrder('array','Mejora tabular y array')
addOrder('booktabs','Ayuda a crear lineas mejor personalizadas')
addOrder('longtable',   'Tablas largas'  )
addOrder('colortab','')
addOrder('colortbl','')

addOrder('tabularx',   'Tablas '  )
addOrder('tabularray',   'Tablas con centrado vertical, colores '  )

addOrder('multirow',  '' )
addOrder('esvect', 'Para vectores con vv{vector}'  )
addOrder('geometry', comment='Define las margenes del documento' )
addOrder('xcolor','Definición de colores')
addOrder('arydshln','Denotar submatrices')
addOrder('enumitem','aumenta las opciones para enumerate e itemize')
addPacks()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PACKAGES['inputenc'].addOption('utf8')
PACKAGES['graphicx'].addOption('pdftex')


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%% Agrega comandos globales
def addGlobalCmd(name,numargs=0,info=''):
  PACKAGES['global'][name]=LatexCommand(name,'',numargs,'global',info)
def addGlobalEnv(name,numargs=0,info=''):
  PACKAGES['global'][name]=LatexEnvironment(name,'',numargs,'global',info)

addGlobalCmd('frac',2)
addGlobalCmd('label',1)
addGlobalCmd('section',1)
addGlobalCmd('section*',1)
addGlobalCmd('subsection',1)
addGlobalCmd('subsection*',1)
addGlobalCmd('subsubsection',1)
addGlobalCmd('subsubsection*',1)

addGlobalCmd('ensuremath',1)

addGlobalCmd('em')
addGlobalCmd('bf')
addGlobalCmd('small')

addGlobalEnv('hspace')
addGlobalCmd('vspace')
addGlobalCmd('thepage')
addGlobalCmd('newpage')
addGlobalCmd('today')


addGlobalCmd('left')
addGlobalCmd('right')

addGlobalCmd('hat')
addGlobalCmd('circ')

addGlobalCmd('rightarrow')

addGlobalEnv('equation')
addGlobalEnv('center')
addGlobalEnv('enumerate')




#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%% Agrega comandos a paquetes, cada parámetro se puede interpretar
# como un simple comando sin argumentos si es un string
# si es una lista, debe tener 3 elementos,
# (<nombrecmd>, <numero de argumentos>,<información>)
# Hay comandos con opciones, para ellos no hay necesidad de indicar
# nada adicional, pueden ser comandos sin argumentos
PACKAGES['tikz'].add(
  'draw', 'fill', 'usetikzlibrary'
)
PACKAGES['tikz'].addEnv(
  'tikzpicture', 'scope'
)

#\definecolor{name}{model}{color-spec} \definecolor{micolor}{HTML}{FF3344}
PACKAGES['xcolor'].add( ('definecolor', 3,'define un color nuevo'))

PACKAGES['amsmath'].add(
  'sum',
  'notag','dotsc','dotsb',
  'dotsm','dotsi','dotso',
  'bigl','bigr','Bigl','Bigr',
  'biggl','biggr', 'Biggl','Biggr',
  'lvert','rvert', 'lVert', 'rVert',
  ('leftroot',1,'Mueve el índice de la raíz a la izquierda'),
  ('uproot',1,'Mueve el índice de lar ráiz a la derecha'),
  ('overleftarrow',1,''),
  ('overrightarrow',1,''),
  ('overleftrightarrow',1,''),
  ('underleftarrow',1,''),
  ('underrightarrow',1,''),
  ('underleftrightarrow',1,''),
  ('xleftarrow',1,''),
  ('xrightarrow',1,''),
  ('overset',2,''),
  ('underset',2,''),
  ('genfrac',6,''),
  ('smash',1,'alinear sobre el renglón'),
  ('dfrac',2,'fracción en modo dysplaymath'),
  ('tfrac',2,'fracción en modo texto'),
  ('binom',2,''),
  ('dbinom',2,'binom en modo dysplaymath'),
  ('tbinom',2,'binom en modo texto'),
  ('DeclareMathOperator',2,''),
  ('DeclareMathOperator*',2,'Operador con subscript como Limite'),
  ('text',1,''),
  ('eqref',1,''),
  ('intertext',1,''),
  ('sideset',2,'Ubica símbolos a diferentes lados de otro')
)
PACKAGES['amsmath'].addEnv(
  'align','align*', 
  'gather','gather*',
  'alignat','alignat*',
  'flalign','flalign*',
  'multiline','multiline*',
  'split','cases',
  'pmatrix','bmatrix', 'Bmatrix', #(x) [x] {x}
  'vmatrix','Vmatrix' #|x|  ||x||
)
PACKAGES['colortab'].add(
    'coloralign',
    'CC', #Color cells pra cajas
    'ECC', # End color cells para cajas
    'LCC', #para entornos como tabular se cambia el CC
    'LC', # Para longtable, en cambio de LCC
     'LCi', 'LCii', 'LCiii', 'LCz','LColors', 
)

PACKAGES['colortbl'].add(
    'rowcolor', 'columncolor', 'cellcolor', 'arrayrulecolor', 
    'doublerulesepcolor', 
)

PACKAGES['xcolor'].add(
    'textcolor'
)

PACKAGES['arydshln'].add(
    'hdashline',
    'cdashline',
    'firsthdashline',
    'lasthdashline',
)
PACKAGES['mathtools'].add(
    'SwapAboveDisplaySkip', #Evita dar un espacio adicional al pasar a display 
    ('mathllap',1,''),
    ('mathrlap',1,''),
    ('mathmbox',1,''),
    ('mathclap',1,''),
    ('mathmakebox',1,''),
    ('cramped',1,'ajusta superíndices y subíndices de manera más compacta'),
    ('crampedllap',1,''),
    ('crampedrlap',1,''),
    ('crampedclap',1,''),
    ('smashoperator',1,''),
    ('adjustlimits',1,''),
    
)
PACKAGES['amsfonts'].add(('mathbb',1,''), ('mathbf',1,''))
PACKAGES['amssymb'].add(
    'measuredangle','imath','jmath','subset', 'subseteq',
    'varnothing',
)
PACKAGES['multirow'].add(('multirow',3,''))
PACKAGES['esvect'].add(('vv',1,''))
PACKAGES['graphicx'].add(('includegraphics',1,''))

PACKAGES['hyperref'].add(('url',1,''))

PACKAGES['array'].add(
    'extrarowheight', 'newcolumntype', 'showcols',
    'firsthline', 'lasthline', 'extratabsurround',
    'arraybackslash', 'extrarowheight', 'multicolumn',
)
PACKAGES['booktabs'].add( 
    'toprule', 'midrule', 'bottomrule', 'cmidrule'
)
PACKAGES['multicol'].addEnv('multicols')
PACKAGES['fancyhdr'].add(
  ('pagestyle',1,''),
  ('lhead',1,''),
  ('chead',1,''),
  ('rhead',1,''),
  ('lfoot',1,''),
  ('cfoot',1,''),
  ('rfoot',1,''),
  ('fancyhead',1,''),
  'headrulewidth',
  'footrulewidth'
)

PACKAGES['longtable'].add('longtable')
PACKAGES['tabularx'].add('tabularx')
PACKAGES['tabularray'].add('tblr')

PACKAGES['enumitem'].add('setlist')
PACKAGES['xparse'].add('NewDocumentCommand')

