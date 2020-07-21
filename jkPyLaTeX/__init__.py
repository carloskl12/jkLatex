#!/usr/bin/python
# -*- coding: utf-8 -*-
JKPYLATEX_VERSION='1.0'
from .latexConfigs import newDocCfg
from .latexUtils import LatexCommand, LatexEnvironment, LatexPackage
from .latexDefCmd import CMD_LATEX
from .latexPackages import PACKAGES
from .latexDoc import LatexDoc
from .latexDocTemplate import ldtTaller, ldtParcial, ldtBasicoLogo
#__all__ = lista de modulos a cargar con import *
