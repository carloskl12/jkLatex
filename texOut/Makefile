# makefile creado por jkPyLaTeX
ARCHIVOS_TEX:= $(wildcard *.tex)

COMPILA:= $(patsubst %.tex, pdflatex -shell-escape -interaction=nonstopmode -halt-on-error %.tex; ,$(ARCHIVOS_TEX))

compilayborra: $(ARCHIVOS_TEX)
	$(COMPILA)
	@make clean

compila: $(ARCHIVOS_TEX)
	$(COMPILA)
.PHONY: clean

clean:
	rm *.aux || true
	rm *.log || true
	rm *.out || true
