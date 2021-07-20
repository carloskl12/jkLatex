from jkPyLaTeX import litBasico
from jkPyLaTeX import LineTikz,  RectangleTikz 
from jkPyLaTeX import NodeDrawTikz, TikzPicture

from jkpyUtils.math import Vector


class BoxFlowChart(object):
    '''
    Clase utilizada para crear diagramas de flujo utilizando 
    cajas cuadradas
    '''
    # Modos para trazar las lineas , el primer parámetro indica si
    # se traza o no 
    # (trazo, line_pattern, marker)
    modo = {'MOVE': (False, '',''),    # Sin trazar nada
            'LINK': (True, '', ''),    # Enlace simple
            'ARROW': (True, '', '>'),   # Enlace con flecha al final
            'ARROWI': (True, '', '<'),   # Enlace con flecha al inicio
            'ARROW_D': (True, '', '<>'), # Enlace con flecha a los dos extremos
            # Versiones dashed
            'LINK_DASH':(True, 'dashed', ''),
            'ARROW_DASH':(True, 'dashed', '>'),
            'ARROWI_DASH':(True, 'dashed', '<'),
            'ARROW_D_DASH':(True, 'dashed', '<>'),
             }
    def __init__(self, fname ):
        self.fname = fname
        self.fig = litBasico(fname)
        # Define la dimensión de la unidad con fines de ajustarse 
        # al tamaño de texto por defecto
        self.unidad = 0.45
        self.dicBoxStyle = {}
        self.dicBoxTypes = {}
        self.dicBox ={}
        self.ltBox =[]
        self.ltLines=[] #Lista de lineas a trazar
        
        self.tikzpicture = TikzPicture(options=">=stealth")
        self.ndTxt = NodeDrawTikz(env=self.tikzpicture)
        self.line_width = 1
        self.bgColour = "white" #Color de fondo del gráfico
        
        #Indicadores de lo que ya se ha dibujado
        self._drawBoxes = False
        self._preamble = False
        self._drawLines = False
        self._boxOptions = False
        self._flowChart = False
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def AddBoxType(self, name, width, height):
        '''
        Agrega un tipo de caja que se identificará por su tamaño y nombre
        '''
        if name not in self.dicBoxTypes:
            self.dicBoxTypes[name]= (width*self.unidad,height*self.unidad)
        else:
            raise Exception(f"El tipo de caja '{name}' ya existe")
    
    def AddBoxTypes(self, ltBoxes):
        for args in ltBoxes:
            self.AddBoxType(*args)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def AddBoxStyle(self,name,fgColour, bgColour):
        '''
        Agrega un estilo de color en formato html, dando su versión para foreground, es decir 
        el relleno de una caja, y background para el color de linea.
        
        name: indicará el sufijo que se dará a los colores, y la forma como 
        se identifica el estilo. 
        
        fgColour: color para Light<name> en formato html con el prefijo #.
        
        bgColour: color para Dark<name> en formato html con el prefijo #.
        '''
        if name not in self.dicBoxStyle:
            if fgColour[0]!='#' or bgColour[0] != '#':
                raise Exception('El formato de color debe tener prefijo #')
            self.dicBoxStyle[name]= (fgColour, bgColour)
        else:
            raise Exception(f"El tipo de caja '{name}' ya existe")

    def AddStyles(self, ltStyles):
        '''
        Agrega los estilos de colores en bloque como una lista de tuplas
        '''
        for args in ltStyles:
            self.AddBoxStyle(*args)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def AddBox(self,idName,content,tpBox,tpStyle,pos, draw = True):
        '''
        Agrega una caja o bloque 
        
        idName : string que identifica la caja
        content : contenido de texto 
        tpBox : tipo de caja (asociado al tamaño)
        tpStyle : tipo de estilo utilizado (colores)
        pos : posición, puede ser una tupla con dos números
            que especifican la coordenada absoluta, o 
            puede ser una tupla con el formato adecuado 
            para dar una coordenada relativa acorde 
            a otras cajas (ver ParsePos)
        draw : indica si se debe dibujar o no, puesto que solo se puede 
            utilizar como un nodo de referencia
        '''
        if idName in self.dicBox:
            raise Exception(f"El idName '{idName}' ya existe")
        if isinstance(pos[0], str):
            pos , lastDir = self.ParsePos(pos)
            wb, hb = self.dicBoxTypes[ tpBox ]
            delta = { 'L':Vector(-wb/2, 0), 'R':Vector(wb/2, 0), 
                  'U':Vector(0, hb/2),  'D':Vector(0, -hb/2)}
            pos = pos + delta[lastDir]
        if tpBox not in self.dicBoxTypes:
            raise Exception(f'El tipo de caja "{tpBox}" no existe')
        if tpStyle not in self.dicBoxStyle:
            raise Exception(f'El estilo de caja "{tpStyle}" no existe')
        self.dicBox[idName] = (content,tpBox,tpStyle,pos, draw)
        self.ltBox.append(idName)
        
    def AddBoxes(self, ltBoxes):
        for args in ltBoxes:
            self.AddBox(*args)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def ParsePos(self, pos):
        '''
        Interpreta la secuecia de desplazamientos relativos para 
        hallar la coordenada de la caja, se asume que se llega
        de forma perpendicular a algún lado de la caja 
        
        pos: una tupla de dos strings, el primero indica el id de la 
        caja desde donde se parte para llegar a la posisión requerida.
        '''
        idBoxName = pos[0]
        if idBoxName not in self.dicBox:
            raise Exception(f'La caja {idBoxName} no existe')
        content, tpBox, tpStyle, pos0, draw = self.dicBox[idBoxName]
        # Obtiene las posiciones LRUD de la caja
        
        LRUD = self.GetLRUD_Box(idBoxName)
        # cadena de comandos separados por espacio
        cmd = pos[1].strip().split(' ')
        
        # pasa a mayúsculas todos los comandos
        cmd = [ s.upper() for s in cmd]
        # Identifica si se requiere trazar una linea o no
        
        if cmd[0] not in self.modo:
            raise Exception(f"El comando '{cmd[0]}' no es válido ")
        # Lista que almacena los movimientos, al inicio obtiene la coordenada
        # según la caja de referencia
        pos0 =  LRUD[ cmd[1][0] ]
        pos0 = Vector(pos0[0], pos0[1])
        ltMov=[ pos0 ]
        # Cada comando empieza por una letra L,R,U,D y pegado un 
        # número positivo que indica el desplazamiento en unidades internas
        base = { 'L':Vector(-1, 0), 'R':Vector(1, 0), 
                  'U':Vector(0, 1),  'D':Vector(0, -1)}
        lastDir = ''
        for i, c in enumerate( cmd[1:] ):
            delta = 0
            if '.' in c:
                delta = float(c[1:])
            else:
                delta = int(c[1:])
            lastDir = c[0]
            #Calcula el vector de variación
            delta *=self.unidad
            deltaV = base[ lastDir ]*delta
            # Nueva posicion
            newPos = deltaV + ltMov[i]
            ltMov.append(newPos)
            
        # Verifica si se debe trazar una linea o no 
        if self.modo[ cmd[0] ][0]:
            self.ltLines.append( (cmd[0], tpStyle, ltMov ) )
        return ltMov[-1], lastDir

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def GetLRUD_Box(self, idBoxName):
        '''
        Calcula las 4 coordenadas de una caja correspondientes al 
        centro de cada uno de sus cuatro lados Left, Right, Up, Down
        '''
        if idBoxName not in self.dicBox:
            raise Exception(f'La caja {idBoxName} no existe')
        content, tpBox, tpStyle, pos0, draw = self.dicBox[idBoxName]
        # Obtiene las dimensiones de la caja, pues la posición
        # indica el centro de la caja
        wb, hb = self.dicBoxTypes[ tpBox ]
        x,y=pos0
        LRUD = {}
        LRUD['L'] = (x-wb/2,y)
        LRUD['R'] = (x+wb/2,y)
        LRUD['U'] = (x, y+hb/2)
        LRUD['D'] = (x, y-hb/2)
        return LRUD

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def GenPreamble(self):
        '''
        Acorde a las definiciones de colores en los diferentes estilos
        se crean los colores en el preámbulo
        '''
        #defineColor=self.fig.useCmd('definecolor')
        s='\\usetikzlibrary{arrows}'
        for style , value in self.dicBoxStyle.items():
            fgColour, bgColour = value
            s+="\n\\definecolor{Light%s}{HTML}{%s}"%(style, fgColour[1:])
            s+="\n\\definecolor{Dark%s}{HTML}{%s}"%(style, bgColour[1:])
        self.fig.appendPreamble(s)
        self._preamble = True

    def GenBoxOptions(self):
        '''
        Genera las opciones utilizadas en los diferentes tipos de cajas
        definidos segun los estilos
        '''
        self.boxOptions = {}
        self.lines = {}
        for box , value in self.dicBox.items():
            content, tpBox, tpStyle, pos0, draw = value
            # el id de las opciones se genera con el estilo que
            # se sugiere sea una referencia al color 
            # y el tipo de caja una referencia a su tamaño o finalidad
            optionId = f'{tpStyle} {tpBox}'
            if optionId not in self.boxOptions:
                wbox, hbox = self.dicBoxTypes[tpBox]
                fgColour, bgColour = self.dicBoxStyle[tpStyle]
                
                opt = 'fill=Light%s, rectangle,'%tpStyle
                opt += ' minimum width=%fcm, align=center,'% wbox
                opt += 'draw=Dark%s, minimum height=%fcm'%( tpStyle, hbox)
                opt += ', text width=%fcm'%(wbox-0.3)
                self.boxOptions[optionId] = opt
                
        self._boxOptions = True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def DrawBoxes(self):
        '''
        Dibuja las cajas en el orden en que se agregaron
        '''
        
        for box in self.ltBox:
            content,tpBox,tpStyle,pos, draw = self.dicBox[box]
            optionId = f'{tpStyle} {tpBox}'
            if draw:
                self.ndTxt(pos, content, self.boxOptions[optionId])
        self._drawBoxes = True

    def DrawLines(self):
        '''
        Dibuja las lineas
        '''
        for cmd, tpStyle, ltMov in self.ltLines:
            draw , pattern, marker = self.modo[cmd]
            start_marker = ''
            end_marker = ''
            if marker == '>':
                end_marker = marker
            elif marker == '<':
                start_marker = marker
            elif marker == '<>':
                start_marker = '<'
                end_marker = '>'
            
            line = LineTikz(env = self.tikzpicture,
                line_pattern = pattern,
                line_width = self.line_width,
                draw_color = 'Dark'+tpStyle,
                start_marker = start_marker,
                end_marker = end_marker
                )
            line(ltMov)
        self._drawLines = True
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def GetMinRectBox(self):
        '''
        Obtiene el rectángulo mínimo para dibujar todas las cajas
        '''
        minX = None
        maxX = None
        minY = None
        maxY = None
        for box , value in self.dicBox.items():
            content,tpBox,tpStyle,pos, draw = value
            LRUD = self.GetLRUD_Box(box)
            if minX == None :
                minX = LRUD['L'][0]
            elif minX > LRUD['L'][0]:
                minX = LRUD['L'][0]
            
            if maxX == None :
                maxX = LRUD['R'][0]
            elif maxX < LRUD['R'][0]:
                maxX = LRUD['R'][0]
                
            if minY == None :
                minY = LRUD['D'][1]
            elif minY > LRUD['D'][1]:
                minY = LRUD['D'][1]
            
            if maxY == None :
                maxY = LRUD['U'][1]
            elif maxY < LRUD['U'][1]:
                maxY = LRUD['U'][1]
        return ( minX,minY, maxX,maxY)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def AddPadding(self, padding=None, left = 0, right=0, up = 0, down = 0):
        '''
        Agrega un espacio
        '''
        l = r= u = d = 0
        if padding !=None:
            l = r = u = d = padding
        if left > 0:  l = left
        if right > 0: r = right 
        if up > 0:    u = up 
        if down > 0:   d = down
        
        marco = RectangleTikz(env= self.tikzpicture,line_width=1, draw_color=self.bgColour)
        minX,minY, maxX, maxY = self.GetMinRectBox()
        
        minX -= l*self.unidad
        minY -= d*self.unidad
        maxX += r*self.unidad
        maxY += u*self.unidad
        marco( (minX,minY), (maxX,maxY) )

    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def GenFlowChart(self):
        '''
        Genera el gráfico
        '''
        if not self._preamble:
            self.GenPreamble()
        if not self._boxOptions:
            self.GenBoxOptions()
        if not self._drawBoxes:
            self.DrawBoxes()
        if not self._drawLines:
            self.DrawLines()
        
        if not self._flowChart:
            self.fig( self.tikzpicture())
        self._flowChart = True


