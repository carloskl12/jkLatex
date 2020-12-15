#!/usr/bin/python
# -*- coding: utf-8 -*-
__version__='2.0.0'
JKPYLATEX_VERSION=__version__
from .latexConfigs import newDocCfg
from .latexUtils import LatexCommand, LatexEnvironment, LatexPackage
from .latexDefCmd import CMD_LATEX
from .latexPackages import PACKAGES
from .latexDoc import LatexDoc
from .latexImg import LatexImg
from .latexDocTemplate import ldtTaller, ldtParcial, ldtBasicoLogo, litBasico
from .latexTikz import ShapeTikz, LineTikz, CircleTikz, EllipseTikz, ArcTikz
from .latexTikz import NodeDrawTikz, RectangleTikz, ScopeTikz, TikzPicture
from .latexTikz import DrawTikz
#__all__ = lista de modulos a cargar con import *
