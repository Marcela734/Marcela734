import pygame
import random
import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from antlr4.CommonTokenStream import CommonTokenStream
from vecindadLexer import vecindadLexer
from vecindadParser import vecindadParser
from visitor import visitor

if __name__ == '__main__':
    while True:
        print("Ingrese los valores: ")

        input_stream = InputStream(sys.stdin.readline())

        try:
            lexer = vecindadLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = vecindadParser(token_stream)
            tree = parser.prog()
            visitor = visitor()
            result = visitor.visit(tree)
            break
        except:
            print("No se reconoce la instrucción")

    infeccion_adyacente_activada = result[3]

    ANCHO, ALTO = result[2], result[2]
    TAMANO_CELDA = 10
    ANCHO_CAPA = ANCHO // TAMANO_CELDA
    ALTO_CAPA = ALTO // TAMANO_CELDA
    NUM_CAPAS = result[1]

    # Agregar separación entre capas
    SEPARACION_CAPAS = 10

    SUSCEPTIBLE = "S"
    EXPUESTO = "E"
    INFECTADO = "I"
    RECUPERADO = "R"

    capas = []
    tiempos_expuestos = []

    for _ in range(NUM_CAPAS):
        capa = [[SUSCEPTIBLE for _ in range(ANCHO_CAPA)] for _ in range(ALTO_CAPA)]
        tiempo_expuesto = [[0 for _ in range(ANCHO_CAPA)] for _ in range(ALTO_CAPA)]

        infectados_agregados = 0
        while infectados_agregados < result[0]:
            x, y = random.randint(0, ANCHO_CAPA - 1), random.randint(0, ALTO_CAPA - 1)
            if capa[y][x] == SUSCEPTIBLE:
                capa[y][x] = INFECTADO
                infectados_agregados += 1
        capas.append(capa)
        tiempos_expuestos.append(tiempo_expuesto)

    pygame.init()

    pantalla = pygame.display.set_mode((ANCHO * NUM_CAPAS + (NUM_CAPAS - 1) * SEPARACION_CAPAS, ALTO))
    pygame.display.set_caption("Autómata Celular SEIR de Capas Múltiples")

    clock = pygame.time.Clock()

    def dibujar_capas():
    # Establecer un color de fondo para el lienzo
        pantalla.fill(pygame.Color("white"))

        for i, capa in enumerate(capas):
            for y in range(ALTO_CAPA):
                for x in range(ANCHO_CAPA):
                    valor_celda = capa[y][x]
                    color = "gray" if valor_celda == SUSCEPTIBLE else "yellow" if valor_celda == EXPUESTO else "red" if valor_celda == INFECTADO else "purple" if valor_celda == RECUPERADO else "blue"
                    
                    # Dibujar cada célula con el color correspondiente
                    pygame.draw.rect(pantalla, pygame.Color(color), (i * (ANCHO_CAPA * TAMANO_CELDA + SEPARACION_CAPAS) + x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA))


    def actualizar_capas():
        nuevas_capas = []
        nuevos_tiempos_expuestos = []
        for i in range(NUM_CAPAS):
            nueva_capa = [[celda for celda in fila] for fila in capas[i]]
            tiempo_expuesto = [[tiempo for tiempo in fila] for fila in tiempos_expuestos[i]]
            for y in range(ALTO_CAPA):
                for x in range(ANCHO_CAPA):
                    if capas[i][y][x] == SUSCEPTIBLE:
                        vecinos_i_misma_capa = sum(1 for j in [-1, 0, 1] for k in [-1, 0, 1]
                                                    if (j == 0 or k == 0)
                                                    and 0 <= x + j < ANCHO_CAPA and 0 <= y + k < ALTO_CAPA
                                                    and capas[i][y + k][x + j] == INFECTADO)
                        vecinos_i_capas_adyacentes = 0
                        if infeccion_adyacente_activada:
                            if i > 0 and 0 <= y - 1 < ALTO_CAPA:
                                vecinos_i_capas_adyacentes += 1 if capas[i - 1][y][x] == INFECTADO else 0
                            if 0 <= y + 1 < ALTO_CAPA and i < NUM_CAPAS - 1:
                                vecinos_i_capas_adyacentes += 1 if capas[i + 1][y][x] == INFECTADO else 0
                        if vecinos_i_misma_capa >= 1 or vecinos_i_capas_adyacentes >= 1:
                            nueva_capa[y][x] = EXPUESTO
                            tiempo_expuesto[y][x] = 0
                    elif capas[i][y][x] == EXPUESTO:
                        tiempo_expuesto[y][x] += 1
                        if tiempo_expuesto[y][x] >= 3:
                            nueva_capa[y][x] = INFECTADO
                    elif capas[i][y][x] == INFECTADO:
                        tiempo_expuesto[y][x] += 1
                        if tiempo_expuesto[y][x] >= 5:
                            nueva_capa[y][x] = RECUPERADO
                    elif capas[i][y][x] == RECUPERADO:
                        tiempo_expuesto[y][x] += 1
                        if tiempo_expuesto[y][x] >= 10:
                            nueva_capa[y][x] = SUSCEPTIBLE
            nuevas_capas.append(nueva_capa)
            nuevos_tiempos_expuestos.append(tiempo_expuesto)
        return nuevas_capas, nuevos_tiempos_expuestos

    def actualizar_y_redibujar():
        global capas, tiempos_expuestos
        capas, tiempos_expuestos = actualizar_capas()
        pantalla.fill((0, 0, 0))  # Limpia la pantalla antes de redibujar
        dibujar_capas()

        # Imprime la cantidad de cada estado en cada capa
        for i, capa in enumerate(capas):
            estado_counts = {"S": 0, "E": 0, "I": 0, "R": 0}
            for fila in capa:
                for estado_celda in fila:
                    estado_counts[estado_celda] += 1
            print(f"Capa {i + 1}: {estado_counts}")

        pygame.display.flip()
        clock.tick(1)
        pygame.time.delay(1000)
        pygame.event.get()


    dibujar_capas()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        actualizar_y_redibujar()