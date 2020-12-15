# jkPyLaTeX
Generación de documentos en python

### Contenido
**[Requisitos](#requisitos)**<br>
**[Objetivo de su desarrollo](#objetivo-de-su-desarrollo)**<br>
**[Modo de uso](#modo-de-uso)**<br>
**[Generación de gráficos](#generación-de-gráficos)**<br>
**[Licencia](#licencia)**<br>
**[Trabajos Futuros](#trabajos-futuros)**<br>

## Requisitos
El paquete es desarrollado en python 3 sobre Linux, y requiere:
* pdflaTeX
* sympy (para ejecutar el [ejemplo](example/example.py))
* unittest (para ejecutar los tests)

## Objetivo de su desarrollo
Este paquete fué desarrollado con el fin de generar documentos latex
de ejercicios de matemáticas. La idea principal es que para generar
documentos se guarde la información realmente importante, y que 
a partir de la misma se pueda generar el documento de manera sencilla,

El paquete está hecho para generar documentos latex a la medida,
sin carga de paquetes innecesarios, haciendo que su compilación
final sea ligera. Además la estructura de los archivos de salida
busca ser ordenada y limpia, organizando en carpetas diferente las 
figuras, el código latex del preámbulo, y el código del contenido.

## Modo de uso
Para utilizarlo se puede trabajar dentro del
directorio. Por ejemplo, al ejecutar:

			$ python example/example.py

se genera el [ejemplo](example/example.py) creando los resultados en la carpeta
[texExample](texExample/). Desde otros directorios se puede trabajar de una 
manera simple, si previo al llamado del paquete se utiliza:
    
      sys.path.insert(0,<directorio donde se halla el paquete=.../jkPyLatex>)

para cambiar el logo por defecto, se puede ubicar un nuevo logo en la misma carpeta
en que está está este archivo, debe tener el nombre logo.pdf (formato pdf).

Para revisar más formas de uso se puede revisar en test el archivo  [testLatexDoc.py](test/testLatexDoc.py)

Si se requiere ejecutar la unidad de test:

	$ python -m unittest test


### trabajo como paquete
Para utilizar el paquete se puede utilizar en modo desarrollo o instalarlo
directamente como un paquete. El modo desarrollo es útil si se quieren hacer 
algunos ajustes particulares en el paquete, en dicho caso hay que descargar 
y descomprimir el paquete en el directorio que se quiera trabajar y ejecutar
este modo de instalación mediante el script setup.py:

			$ python setup.py develop

Para desinstalarlo:

			$ python setup.py develop --uninstall

Finalmente si se quiere instalarlo como una librería que no se quiere modificar

			$ python setup.py install

## Generación de gráficos
La generación de gráficos tiene un interesante potencial al integrarse con 
python, se tienen disponibles diferentes clases que generan una capa de 
abstracción con la librería Tikz para generar gráficos con mayor libertad
utilizando el lenguaje Python.

El flujo de trabajo para la creación de gráficos consiste en crear un documento 
utilizando la plantilla **litBasico**. Luego se crea una instancia de 
TikzPicture que abstrae el ambiente tikzpicture, haciendo las veces de 
canvaz de dibujo, y este ambiente será utilizado para crear instancias 
de las clases que abstraen el gráfico de diferentes figuras geométricas.
Una vez se ha terminado el gráfico, con una llamada de la instancia de 
TikzPicture se genera el código que irá en el documento latex para 
generar el dibujo.

```python
from jkPyLaTeX import TikzPicture, litBasico
from jkPyLaTeX import CircleTikz

#Crea el documento
fig=litBasico('nombreFigura')

#Obtiene una instancia para manejar el entorno de tikzpicture
tikzpicture=TikzPicture()
#Crea una instancia para dibujar un círculo con parámetros por defecto
circle=CircleTikz(env=tikzpicture)
#Crea una instancia para dibujar rellenando la figura con color azul
circle2=CircleTikz(env=tikzpicture,fill_color='blue')
#dibuja un círuclo con centro en (1,1) cuyo radio es 1
circle((1,1),1)
#Segúndo círculo que se rellena con color azul
circle2((2,1),1)

#Genera el codigo del gráfico y se guarda en el documento
fig(tikzpicture())

#Guarda el documento latex
fig.save('./')
#Compila el código
fig.genDoc(target=True)
```

Las diferentes figuras geométricas para graficar corresponden 
a clases con sufijo Tikz: 
  * CircleTikz: círculos
  * RectangleTikz: rectángulo
  * ArcTikz: arco
  * LineTikz: secuencia de puntos unidos por una linea
  * EllipseTikz: elipse
  * ScopeTikz: permite utilizar en entorno scope
  * NodeDrawTikz: abstrae el nodo de tikz, comúnmente utilizado para posicionar
    texto.
  * DrawTikz: abstrae el comando draw que permite hacer diferentes figuras 
    bajo un mismo estilo.

Las anteriores clases, permiten dibujar automáticamente sobre tikzpicture si 
las instancias creadas partieron indicando el entorno tikzpicture:

```python

circle=CircleTikz(env=tikzpicture)
circle((1,1),1)
```

Si no se indica el entorno tikzpicture, las instancias se pueden utilizar 
para generar codigo latex y concatenarlo manualmente para crear el documento 
tex que se ha de compilar luego. Para mas detalles se pueden revisar los 
ejemplos de: figBasica.py, conjuntos.py, mensajeCriptico.py.

## Licencia
[GNU GENERAL PUBLIC LICENSE](LICENSE)



## Trabajos futuros
Agregar una plantilla para generar gráficas de funciones con facilidad.


