from vecindadVisitor import vecindadVisitor # Permite visitar nodos específicos en un árbol de análisis sintáctico generado por ANTLR4 para el lenguaje definido en tu gramática 

class visitor(vecindadVisitor): # Hereda de la clase CellularAutomatonVisitor.
    def __init__(self): #Crear un diccionario vacío llamado memory que se utilizará para almacenar información durante el procesamiento del árbol sintáctico.
        self.memory = {}

    def visitConfiguration(self, ctx): #Se obtienen valores para infectados, capas, tamano, y propagacion.
        infectados = int(ctx.infectados().getText())
        capas = int(ctx.capas().getText())
        tamano = int(ctx.tamano().getText())
        propagacion = ctx.propagacion().getText()

        if(propagacion=='True'): # El valor es la cadena 'True', se asigna True; de lo contrario, se asigna False.
            propagacion=True
        else:
            propagacion=False

        return [infectados,capas,tamano,propagacion] #Retorna una lista que contiene los valores extraídos del contexto. Esta lista se utilizará más adelante en el código principal.
