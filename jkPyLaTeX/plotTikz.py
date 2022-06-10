
from jkPyLaTeX import LineTikz, CircleTikz, EllipseTikz, RectangleTikz, ArcTikz
from jkPyLaTeX import NodeDrawTikz, ScopeTikz, TikzPicture
from jkPyLaTeX import DrawTikz
from jkpyUtils.math import  Vector


import math
from decimal import Decimal


class PlotTikz(object):
    '''
    La metodología de uso es que existen parámetros que se habilitan o deshabilitan
    cuando se pasan argumentos a la función Plot, si se requiere mayor 
    presición de algunos estilos se deben deshabilitar y luego utilizar las 
    funciones específicas para personalizar el estilo con mayor versatilidad.
    
    Los estilos de trazos se pueden reajustar reasignando la instacia de dibujo
    a la respectiva variable tool_<...>.
    
    '''
    COLORS=('black', 'blue', 'red', 'green', 'cyan', 'magenta', 'yellow',
            'brown',  'gray', 'lime','orange',  'pink',  'olive',
            'lightgray', 'purple', 'teal', 'violet','darkgray')
    def __init__(self,env, xmin=-1,xmax=1,ymin=-1,ymax=1, size = (4,3) , corner_axis = True  ):
        '''
        env: entorno donde se dibujará
        xmin, xmax: valor mínimo y máximo en x a graficar
        ymin, ymax: valor minimo y máximo en y a graficar
        size: indica el tamaño que ocupará la región del plano (ancho, alto) . 
            No incluye los labels y títulos que se adicionen
        '''
        self.env = env
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.corner_axis = corner_axis
        self.xgrid_width = 1 #espaciado en la grilla en x
        self.ygrid_width = 1 #espaciado de la grilla en y
        
        self.width, self.height = size
        #print('  width:',self.width, '  height:',self.height)
        self._plots=[]#Lista de plots
        self.GenSyles()
        
    
    def GetColor(self,i):
        '''
        Retorna el nombre de un color para cambiar los valores de forma automática
        cuando no se da un color específico para las curvas
        '''
        return self.COLORS[i%len(self.COLORS)]
    def GenSyles(self):
        '''
        Genera los estilos y las herramientas de dibujo
        '''
        self.xgrid_width = 1 #espaciado en la grilla en x
        self.ygrid_width = 1 #espaciado de la grilla en y
        
        # ancho del texto de las leyendas
        self.legends_text_width = 0.6
        # escala del texto (mas pequeño del normal)
        self.legends_text_scale = 0.7 
        # longitud de la linea de muestra 
        self.legends_line_length = 0.6
        # margen 
        self.legends_margin = 0.1
        
        # Herramientas
        self.tool_node = NodeDrawTikz(env=self.env)
        self.tool_line = LineTikz(env=self.env, line_width=0.5, color = 'black!100')
        self.tool_rect_bounds = RectangleTikz(env=self.env, line_width = 0.5, color='black!100')
        self.tool_line_minor_grid = LineTikz(env=self.env, line_width=0.5, 
            dash_pattern = 'on 1pt off 1pt',color='black!30')
        self.tool_line_major_grid = LineTikz(env=self.env, line_width=0.5, 
            dash_pattern = 'on 2pt off 3pt', color='black!50')
        
        self.tool_rect_legends = RectangleTikz(env = self.env, line_width = 0.5,
            fill_color='white', draw_color='black')
        # _line_pattern=('solid','dashed', 'dotted', "dashdotted", 
        # "densely dotted", "loosely dotted", "double" )
        # Dash patern: on 20pt off 10pt

    def AddPlot(self,x,y,label='',**kwargs):
        '''
        x,y : datos para x,y a graficar
        label: nombre de la curva
        kwargs: las opciones para el trazo
        '''
        dicPlot={'x':x, 'y':y, 'label':label,'line_width':1}
        for k, v in kwargs.items():
            dicPlot[k]=v
        self._plots.append(dicPlot)
        
    def AdjustSize(self,x,y):
        '''
        Ajusta el rango de la gráfica dados los datos a graficar
        '''
        self.xmin = min(x)
        self.xmax = max(x)
        self.ymin = min(y)
        self.ymax = max(y)
        
        
    def FunAdjX(self):
        '''
        Calcula la función para ajustar las coordenadas en x
        '''
        m = self.width/(self.xmax-self.xmin)
        b = -m*self.xmin
        f = lambda x: m*x+b
        fi = lambda x: (x-b)/m
        return (f,fi)

    def FunAdjY(self):
        '''
        Calcula la función para ajustar las coordenadas en y
        '''
        m = self.height/(self.ymax-self.ymin)
        b = -m*self.ymin
        f = lambda y: m*y+b
        fi = lambda y: (y-b)/m
        return (f,fi)

    def Plot(self,**kwargs):
        '''
        Genera el gráfico
        xlabel, ylabel : nombres de los ejes
        title: titulo
        legends: indica si se muestran etiquetas de las curvas graficadas
        axis: indica si se grafican los ejes con sus labels, grilla, etc.
        minor_grid: indica si grafica la grilla menor
        major_grid: indica si se grafica la grilla mayor
        minor_x_thick, major_x_thick ... : indica el espaciado de la 
            grilla, mayor o menor, y como se indican las unidades en los ejes
        xticklabel,yticklabel: si se muestra o no las unidades de los ejes
        '''
        dicArgs={'legends':True, 'axis':True,
        'xticklabel':True, 'yticklabel':True}
        for k,v in kwargs.items():
            dicArgs[k]=v
        
        if dicArgs['axis']:
            self.PlotAxis(**dicArgs)
        
        for i, dicPlot in enumerate( self._plots):
            opt = dicPlot.copy()
            del opt['x']
            del opt['y']
            del opt['label']
            if 'color' not in opt:
                opt['color'] = self.GetColor(i)
            line = LineTikz(env=self.env, **opt)
            line(self.AdjustPoints( dicPlot['x'],dicPlot['y'])  )
        
        if dicArgs['legends']:
            self.Draw_legends()
        
    def IsVisiblePoint(self,x,y):
        return ( self.xmin <= x <= self.xmax) and  (self.ymin <= y <=self.ymax )

    def AdjustPoints(self, x,y):
        '''
        Ajusta los puntos para que se pueda graficar
        '''
        ftx , ftxi = self.FunAdjX()
        fty , ftyi = self.FunAdjY()
        x2 = [ftx(xi) for xi in x]
        y2 = [fty(yi) for yi in y]
        points=[]
        last = True
        for i in range( len(x2)):
            if self.IsVisiblePoint( x[i], y[i]):
                points.append( ( x2[i], y2[i]) )
                last =True
            else :
                if last :
                    points.append( (None, None) )
                    last = False
        if not last:
            points.pop()
        return points


    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def PlotAxis(self, **kwargs ):
        # Ajuste de las unidades x,y
        ftx , ftxi = self.FunAdjX()
        fty , ftyi = self.FunAdjY()
        
        minor_grid = kwargs.get('minor_grid', False)
        major_grid = kwargs.get('major_grid', False)
        major_x_thick = kwargs.get('major_x_thick',self.major_x_thick)
        major_y_thick = kwargs.get('major_y_thick', self.major_y_thick)
        minor_x_thick = major_x_thick/10
        minor_y_thick = major_y_thick/10
        
        xticklabel = kwargs.get('xticklabel', True)
        yticklabel = kwargs.get('yticklabel', True)
        xlabel = kwargs.get('xlabel','')
        ylabel = kwargs.get('ylabel','')
        title = kwargs.get('title', '')
        
        
        
        # Obtiene el valor mínimo a colocar
        xmintk = self.DigRound(abs(self.xmin),True)
        if self.xmin < 0:
            xmintk *= -1
        while(xmintk  < self.xmin):
            xmintk += major_x_thick
        xmintk2 = xmintk # para minor_x_thick
        while(xmintk2 > self.xmin):
            xmintk2 -= minor_x_thick
        xmintk2 += minor_x_thick
        
        # ajusta y
        ymintk = self.DigRound(abs(self.ymin),True)
        if self.ymin < 0:
            ymintk *= -1
        while(ymintk < self.ymin ):
            ymintk += major_y_thick
        ymintk2= ymintk
        while (ymintk2 > self.ymin):
            ymintk2 -= minor_y_thick
        ymintk2 += minor_y_thick
        
        # Dibuja eje horizontal
        line = self.tool_line
        node = self.tool_node
        l1 = 0.1 #Longitud de la raya
        l2 = 0.2
        while(xmintk2 < self.xmax):
            x = ftx( float(xmintk2) )
            if minor_grid: self.tool_line_minor_grid([(x,0),(x,self.height)])
            line([(x,0), (x,l1), (None,None), (x,self.height), (x,self.height-l1)])
            xmintk2 += minor_x_thick
        
        while(xmintk < self.xmax):
            x = ftx( float( xmintk) )
            if major_grid : self.tool_line_major_grid([(x,0),(x,self.height)])
            line([(x,0), (x,l2), (None,None), (x,self.height), (x,self.height-l2)])
            if xticklabel : node((x,-.3), str(xmintk))
            xmintk += major_x_thick
        # Dibuja eje vertical
        while(ymintk2 < self.ymax):
            y = fty(float(ymintk2))
            if minor_grid: self.tool_line_minor_grid([(0,y),(self.width, y)])
            line( [(0,y),(l1,y), (None,None), (self.width,y), (self.width-l1,y)])
            ymintk2 += minor_y_thick
        while ( ymintk < self.ymax ) :
            y = fty( float( ymintk ) )
            if major_grid : self.tool_line_major_grid([(0,y),(self.width, y)])
            line( [(0,y),(l2,y), (None,None), (self.width,y), (self.width-l2,y)])
            if yticklabel : node((-0.5,y), str(ymintk) )
            ymintk += major_y_thick
        
        self.tool_rect_bounds( (0,0), (self.width,self.height) )
        # Traza las etiquetas para los ejes
        if xlabel != '':
            self.Draw_xlabel(xlabel)
        if ylabel != '':
            self.Draw_ylabel(ylabel)
        if title != '':
            self.Draw_title(title)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Draw_xlabel(self, label, options = '', xoff = 0, yoff = 0, pos = None):
        '''
        Dibuja la etiqueta del eje x
        '''
        if pos == None:
            pos = Vector( self.width/2, -0.8)
        else:
            pos = Vector(pos[0],pos[1])
        
        pos = pos + Vector(xoff, yoff)
        self.tool_node( pos, label, options= options)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Draw_ylabel(self, label, options = '', xoff = 0, yoff = 0,
         pos = None, rotate = True):
        '''
        rotate indica si se rota el label
        '''
        if pos == None:
            pos = Vector(-1.2, self.height/2)
        else:
            pos = Vector(pos[0],pos[1])
        if rotate:
            if options != '' : options=', '+options
            options='rotate = 90 '+options
        pos = pos + Vector(xoff, yoff)
        self.tool_node( pos, label, options= options)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Draw_title(self, title, options = '', xoff = 0, yoff = 0, pos = None):
        if pos == None:
            pos = Vector( self.width/2, self.height+0.6)
        else:
            pos = Vector(pos[0],pos[1])
        
        pos = pos + Vector(xoff, yoff)
        self.tool_node( pos, title, options= options )
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def Draw_legends(self, xoff=0, yoff=0, pos = None):
        '''
        Dibuja las etiquetas de las curvas graficas
        
        pos: esquina superior izquierda de la caja de las etiquetas
        '''
        w,h= self.size_box_legends
        if pos == None:
            pos = Vector( self.width-w, self.height)
        else:
            pos = Vector(pos[0],pos[1])
        pos += Vector(xoff, yoff)
        
        self.tool_rect_legends( pos, pos+Vector(w,-h))
        
        wtxt = self.legends_text_width
        hrow = self.row_height_legends
        lline = self.legends_line_length #Longitud de la linea
        posLine = pos-Vector(0,self.legends_margin+hrow/2)
        
        optNode = 'scale = %f'%self.legends_text_scale
        for i, dicPlot in enumerate(self._plots):
            lbl = dicPlot['label']
            if lbl == '':
                lbl = '$f_{%i}$'%(i+1)
            
            opt = dicPlot.copy()
            del opt['x']
            del opt['y']
            del opt['label']
            if 'color' not in opt:
                opt['color'] = self.GetColor(i)
            line = LineTikz(env=self.env, **opt)
            self.tool_node( posLine+Vector(wtxt/2,0), lbl, options= optNode)
            line( [posLine+Vector( wtxt,0) , posLine+Vector(wtxt+lline,0)])
            
            posLine-=Vector(0,hrow)
    @property
    def row_height_legends(self):
        '''
        Altura de una linea
        '''
        return 0.55*self.legends_text_scale
    @property
    def size_box_legends(self):
        '''
        Calcula las dimenciones de la caja de las leyendas
        '''
        width = self.legends_text_width + self.legends_line_length +2*self.legends_margin
        height = len(self._plots)*self.row_height_legends+ 2*self.legends_margin
        return (width,height)
    
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    @property
    def major_x_thick(self):
        '''
        Calcula el espaciado más apropiado de de la grilla mayor horizontal
        '''
        rango = self.xmax-self.xmin
        ftx , ftxi = self.FunAdjX()
        nSegmentos = self.width/self.xgrid_width #Sobre el ancho de segmento
        return self.DigRound( rango/nSegmentos , True)
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    @property
    def major_y_thick(self):
        '''
        Calcula el espaciado más apropiado de de la grilla mayor horizontal
        '''
        rango = self.ymax-self.ymin
        fty , ftyi = self.FunAdjY()
        nSegmentos = self.height / self.ygrid_width #Sobre el ancho de segmento
        return self.DigRound( rango/nSegmentos , True)
        
    #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def DigRound(self, v, to_decimal = False):
        '''
        Redondea a un solo dígito el valor v, el cual 
        siempre debe ser positivo
        
        Pasa el número al factor de notación científica con un 
        dígito entero, el cual se redondea hacia el entero próximo mayor,
        y se vuelve a escalar a los órdenes de magnitud originales
        
        to_decimal indica si se genera el número como un valor decimal
        '''
        if v == 0:
            return 0
        dig = math.log(v,10)
        diga = math.ceil( abs(dig))
        if dig < 0:
            dig = -diga
        else:
            dig = diga-1
        coef = v/10**dig # Primer factor de notación científica
        q = math.ceil(coef)
        if to_decimal:
            return Decimal(q)*Decimal(10)**dig
            
        return q*10**dig
