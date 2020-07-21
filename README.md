# jkPyLaTeX
Generación de documentos en python

### Contenido
**[Requisitos](#requisitos)**<br>
**[Objetivo de su desarrollo](#objetivo-de-su-desarrollo)**<br>
**[Modo de uso](#modo-de-uso)**<br>
**[Licencia](#licencia)**<br>
**[Trabajos Futuros](#trabajos-futuros)**<br>

## Requisitos
El paquete es desarrollado en python 3 sobre Linux, y requiere:
* pdflaTeX
* sympy (para ejecutar el [ejemplo](example/example.py))

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

## Licencia
[GNU GENERAL PUBLIC LICENSE](LICENCE)

## Trabajos futuros
Agregar una plantilla para generar gráficas de funciones con facilidad.


