# Generated from c://Users//miap7//Desktop//Certamen//vecindad.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vecindadParser import vecindadParser
else:
    from vecindadParser import vecindadParser

# This class defines a complete generic visitor for a parse tree produced by vecindadParser.

class vecindadVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by vecindadParser#prog.
    def visitProg(self, ctx:vecindadParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#instruccion.
    def visitInstruccion(self, ctx:vecindadParser.InstruccionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#configuration.
    def visitConfiguration(self, ctx:vecindadParser.ConfigurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#infectados.
    def visitInfectados(self, ctx:vecindadParser.InfectadosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#capas.
    def visitCapas(self, ctx:vecindadParser.CapasContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#tamano.
    def visitTamano(self, ctx:vecindadParser.TamanoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by vecindadParser#propagacion.
    def visitPropagacion(self, ctx:vecindadParser.PropagacionContext):
        return self.visitChildren(ctx)



del vecindadParser