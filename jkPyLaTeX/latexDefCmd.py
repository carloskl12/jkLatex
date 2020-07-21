'''
Definiciones de comandos nuevos
'''
from jkPyLaTeX import LatexCommand

CMD_LATEX={}
def defCmd(cmdName, body,numargs, packs,info=''):
  CMD_LATEX[cmdName]=LatexCommand(cmdName,body,numargs,packs,info)

defCmd('abs','\\ensuremath{\\left|#1\\right|}',1,'amsmath')
defCmd('parentesis','\\left(#1\\right)',1,'amsmath')# Hacer el parentesis
defCmd('limite','\\lim_{ #1 \\to #2} #3 ',3,'amsmath')
defCmd('llaves','\\{ #1 \\}',1,'amsmath')
defCmd('fracds','\\displaystyle\\frac{#1}{#2}',2,'amsmath')# Fracción con displaystyle
#%%%%%%%%%%% Geometría %%%%%%%%%%%%%%%%%
defCmd('segmento','\\stackrel{\\hrulefill}{#1}',1,'amsmath')# Segmento de recta
defCmd('tarc','\\mbox{\\large$\\frown$}',0,'amsmath')
defCmd('arc','\\stackrel{\\tarc}{#1}',1,'amsmath')
#%%%%%%%%%%% vectores %%%%%%%%%%%%%%%%%%
defCmd('vui','\\hat{\\imath}',0,'amsmath') # Vector Unitario I 
defCmd('vuj','\\hat{\\jmath}',0,'amsmath') # Vector Unitario J
defCmd('vuk','\\hat{k}',0,'amsmath') # Vector Unitario k
defCmd('vecijk','#1 \\vui #2 \\vuj #3 \\vuk',3,'amsmath') 
# Para escribir un vector con sus unitarios i j k, se debe incluir el signo a cada numero
defCmd('normaVec','\\left\\lVert #1 \\right\\rVert}',1,'amsmath')
#%%%%%%%%%%% Unidades %%%%%%%%%%%%%%%%%%
defCmd('angstrom','\\text{\\normalfont\\AA}',0,'amsmath')
defCmd('grados','^\\circ',0,'amsmath') # Grados en ángulos, debe estar en modo matemático
# \newcommand\tablename{Tabla}



