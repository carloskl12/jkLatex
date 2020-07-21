#Macros de make para crear un archivo pdf a partir de archivos latex


ARCHIVOS_TEX:= $(wildcard *.tex)

#----------------antepone comando de compilación
COMPILA:= $(patsubst %.tex, pdflatex -halt-on-error %.tex; ,$(ARCHIVOS_TEX))

COMPILA_S:= $(patsubst %.tex, pdflatex -no-shell-escape -halt-on-error %.tex; ,$(ARCHIVOS_TEX))

compilatodo: $(ARCHIVOS_TEX)
	$(COMPILA)
	$(COMPILA)
	@make clean
	@echo "\n Compilados:\n" $(ARCHIVOS_TEX) "\n"

compilaSimple: $(ARCHIVOS_TEX)
	$(COMPILA_S)
	$(COMPILA_S)
	@make clean
	@echo "\n Compilados:\n" $(ARCHIVOS_TEX) "\n"
.PHONY: clean cleanAll	#Ficheros ficticios
#Siempre que se tenga como dependencia se ejecuta, o se llama con make clean
clean :
	bash latexClean.sh
#cleanAll: clean 	#Ejecuta clean, borra el ejecutable, se llama como make cleanAll

