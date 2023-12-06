# Generated from c://Users//miap7//Desktop//Certamen//vecindad.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .vecindadParser import vecindadParser
else:
    from vecindadParser import vecindadParser

# This class defines a complete listener for a parse tree produced by vecindadParser.
class vecindadListener(ParseTreeListener):

    # Enter a parse tree produced by vecindadParser#prog.
    def enterProg(self, ctx:vecindadParser.ProgContext):
        pass

    # Exit a parse tree produced by vecindadParser#prog.
    def exitProg(self, ctx:vecindadParser.ProgContext):
        pass


    # Enter a parse tree produced by vecindadParser#instruccion.
    def enterInstruccion(self, ctx:vecindadParser.InstruccionContext):
        pass

    # Exit a parse tree produced by vecindadParser#instruccion.
    def exitInstruccion(self, ctx:vecindadParser.InstruccionContext):
        pass


    # Enter a parse tree produced by vecindadParser#configuration.
    def enterConfiguration(self, ctx:vecindadParser.ConfigurationContext):
        pass

    # Exit a parse tree produced by vecindadParser#configuration.
    def exitConfiguration(self, ctx:vecindadParser.ConfigurationContext):
        pass


    # Enter a parse tree produced by vecindadParser#infectados.
    def enterInfectados(self, ctx:vecindadParser.InfectadosContext):
        pass

    # Exit a parse tree produced by vecindadParser#infectados.
    def exitInfectados(self, ctx:vecindadParser.InfectadosContext):
        pass


    # Enter a parse tree produced by vecindadParser#capas.
    def enterCapas(self, ctx:vecindadParser.CapasContext):
        pass

    # Exit a parse tree produced by vecindadParser#capas.
    def exitCapas(self, ctx:vecindadParser.CapasContext):
        pass


    # Enter a parse tree produced by vecindadParser#tamano.
    def enterTamano(self, ctx:vecindadParser.TamanoContext):
        pass

    # Exit a parse tree produced by vecindadParser#tamano.
    def exitTamano(self, ctx:vecindadParser.TamanoContext):
        pass


    # Enter a parse tree produced by vecindadParser#propagacion.
    def enterPropagacion(self, ctx:vecindadParser.PropagacionContext):
        pass

    # Exit a parse tree produced by vecindadParser#propagacion.
    def exitPropagacion(self, ctx:vecindadParser.PropagacionContext):
        pass



del vecindadParser