'''
Configuraciones para documentos latex
'''

DOC_CFG_BASE={
  'tree':{'main':'_name','preamble':'./src/', 'figures':'./figs/'},
  'docclass':'article',
  'paper':'letter',
  'fontsize':'12',
  'language':'english',
  #Configuración de páginas
  #Las unidades pueden ser cm, in (pulgadas), pt (1cm = 28.5 pt)
  #Los valores tambien pueden ser negativos
  'parskip':"10pt", # espacio entre parrafos
  #Espacio para encuadernación que afecta la numeración impar si es de
  #impresion a doble cara, de lo contrario afecta a todas las páginas.
  'oddsidemargin':'-11mm',
  'headheight':'50pt', #Altura del encabezado
  'headsep':'12pt',#Espacio entre la base del encabezado y el tope del cuerpo del documento
  'marginparsep':'0pt', #Distancia que separa las notas marginales del texto principal
  'marginparwidth':'0pt',# Ancho de las notas marginales (A la derecha)
  'footskip':'20pt',# Distancia entre el texto y el pie de página.
  #Márgenes de pagina
  'top':'30mm',
  'bottom':'25mm',
  'left':'20mm',
  'right':'20mm',
}

DOC_CFG_TALLER=DOC_CFG_BASE.copy()
DOC_CFG_TALLER['language']='spanish'
DOC_CFG_TALLER['lhead']='\\small {--- Facultad de  Ciencias Naturales y  Matemáticas \\vspace{4pt}}'
DOC_CFG_TALLER['chead']=''
DOC_CFG_TALLER['rhead']='\\includegraphics[scale=0.65]{logo.pdf}'
DOC_CFG_TALLER['lfoot']='\\today'
DOC_CFG_TALLER['cfoot']='\\rightmark'
DOC_CFG_TALLER['rfoot']='\\thepage'
DOC_CFG_TALLER['headrulewidth']='0.4pt'
DOC_CFG_TALLER['footrulewidth']='0.4pt'

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuraciones para trabajar con imágenes
IMG_CFG_BASE={
  #'tree':N, No tiene arbol de archivos
  'docclass':'standalone',
  #'paper':'letter',  no hay especificación de papel
  'fontsize':'12',
  'language':'english',
  'paper':'tikz' #Hace que se genere una página por cada entorno tikz
}


def newDocCfg(cfgName):
  '''
  Función para obtener la configuración base
  con el fin de retornar una copia y no 
  alterar la base
  '''
  if cfgName=='BASE':
    return DOC_CFG_BASE.copy()
  elif cfgName=='TALLER':
    return DOC_CFG_TALLER.copy()
  elif cfgName=='IMG_BASE':
    return IMG_CFG_BASE.copy()
    

