'''
Funciones que generan los templates de documentos
'''

from jkPyLaTeX import LatexDoc, PACKAGES, CMD_LATEX, newDocCfg, LatexImg


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def litBasico(filename):
  '''
  lit - LatexImg Template 
  '''
  config= newDocCfg('IMG_BASE')
  doc=LatexImg(filename,**config)
  doc.appendPreamble('\\usepackage[utf8]{inputenc}')
  doc.useCmd('draw') #Para invocar tikz
  return doc

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def ldtBasicoLogo(filename,titulo=''):
  config= newDocCfg('TALLER')
  config['lfoot']=''
  doc=LatexDoc(filename,**config)
  doc.useCmd('includegraphics')
  if titulo != '':
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Genera el encabezado
    sIni='\\begin{centering}\n'
    sIni+='\\bf{ \\Large  %s'%titulo
    sIni+='}\\\\\\vspace{3mm}\n\\end{centering}\n'
    doc.setDocIni(
     sIni
    )
    
  
  return doc

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def ldtTaller(filename,titulo, asignatura='',fecha='today'):
  config= newDocCfg('TALLER')
  if fecha != 'today':
    config['lfoot']=fecha
  doc=LatexDoc(filename,**config)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Genera el encabezado
  doc.useCmd('includegraphics')
  sIni='\\begin{centering}\n'
  sIni+='\\bf{ \\Large  %s \\\\\n'%asignatura
  sIni+='%s \\\\\n'%titulo
  sIni+='}\n\\end{centering}\n\\ \n'
  doc.setDocIni(
   sIni
  )
  return doc

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def ldtParcial(filename, codigoAsig='41A10',
  numGrupo=1, refParcial=1, fecha='Marzo 10 de 2020', 
  selMultiple=True, usarCalculadora=False,
   bonoTiempo=False, tiempoParcial=60):
  config= newDocCfg('TALLER')
  config['cfoot']=fecha
  config['lfoot']='%s-G%i: Parcial %i'%(codigoAsig,numGrupo,refParcial)
  doc=LatexDoc(filename,**config)
  doc.useCmd('includegraphics')
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Reglas e instrucciones
  instruccionesA='''
  {\\bf Responda las preguntas marcando la opción adecuada con tinta }. El
  parcial se califica sobre 100 puntos. Cada pregunta tiene asignada igual
  cantidad de puntos. Al finalizar la actividad debe entregar el cuestionario
  con las respuestas y todo el material que las sustente, en caso de que una
  respuesta no esté justificada no se tendrá en cuenta.
  '''
  instruccionesB='''
  {\\bf Responda las preguntas justificando cada respuesta }. El parcial se
  califica sobre 100 puntos. Cada pregunta tiene asignado sus puntos
  respectivos. Al finalizar la actividad debe entregar el cuestionario con las
  respuestas y todo el material que las sustente, en caso de que una respuesta
  no esté justificada no se tendrá en cuenta.
  '''
  reglasA='''
  Está prohibido el uso de cualquier ayuda externa, calculadora, celular,
  computador, o cualquier dispositivo diferente a un lápiz, esfero y borrador.
  Los estudiantes que presentan el exámen a lápiz no podrán presentar reclamos a
  la calificación.
  '''
  reglasB='''
  Está prohibido el uso de cualquier ayuda externa, celular, computador, o
  cualquier dispositivo diferente a un lápiz, esfero, borrador, y su calculadora
  personal. Los estudiantes que presentan el exámen a lápiz no podrán presentar
  reclamos a la calificación.
  '''
  instrucciones=instruccionesA
  reglas=reglasA
  if not selMultiple:
    instrucciones=instruccionesB
  if usarCalculadora:
    reglas=reglasB
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Genera el encabezado
  encabezado='\\parbox[c]{ 0.92\\textwidth}\n'
  encabezado+='{\\centering %s\\\\'%instrucciones
  encabezado+='{\\bf Reglas: %s\n}}'%reglas
  sIni='\\fbox{\\fbox{%s}}\n'%encabezado
  sIni+='\\vspace{0.7cm}\\\\\n'
  sIni+='Nombre:\\rule{0.52\\textwidth}{0.1mm}\\hspace{5mm}'
  sIni+='Código: \\rule{0.30\\textwidth}{0.1mm}\n\\\\ '
  doc.setDocIni(
   sIni
  )
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  # Bonificación de tiempo
  if bonoTiempo:
    s='{\\em Este cuestionario está hecho para resolverse en un '
    s+='tiempo máximo de '+str(tiempoParcial)+ ' minutos},'
    s+='''
    si se entrega antes del tiempo estipulado se
    asignará una bonificación del 24\\% sobre los puntos obtenidos luego de
    15 minutos iniciado el exámen, y descenderá linealmente hasta 0\\%
    acorde al tiempo utilizado. Si se superan los 100 puntos, estos no se
    tendrán en cuenta.'''
    doc.newcommand('bonificacionTiempo',s)
  return doc
