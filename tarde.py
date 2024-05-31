import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Configuración de pantalla completa
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
pygame.display.set_caption("Ordena tus Rutinas Diarias")

# Colores
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# Fuente para el texto
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)  # Fuente más grande para el título

# Cargar y redimensionar las imágenes de las rutinas
rutina_imagenes = {
    "1 T": pygame.transform.scale(pygame.image.load("imagenes/1 T.jpg").convert_alpha(), (150, 150)),
    "2 T": pygame.transform.scale(pygame.image.load("imagenes/2 T.jpg").convert_alpha(), (150, 150)),
    "5 T": pygame.transform.scale(pygame.image.load("imagenes/5 T.jpg").convert_alpha(), (150, 150)),
    "26 D": pygame.transform.scale(pygame.image.load("imagenes/26 D.jpg").convert_alpha(), (150, 150)),
    "4 T": pygame.transform.scale(pygame.image.load("imagenes/4 T.jpg").convert_alpha(), (150, 150)),
    "3 T": pygame.transform.scale(pygame.image.load("imagenes/3 T.jpg").convert_alpha(), (150, 150)),
   
}

# Función para calcular las posiciones de las imágenes en una cuadrícula
def calcular_posiciones_cuadricula(imagenes, num_columnas, separacion):
    posiciones = []
    num_imagenes = len(imagenes)
    espacio_horizontal = (screen_info.current_w - (num_columnas * imagenes[0].get_width() + (num_columnas - 1) * separacion)) // 2
    for i in range(num_imagenes):
        columna = i % num_columnas
        fila = i // num_columnas
        x = espacio_horizontal + columna * (imagenes[i].get_width() + separacion)
        y = 40 + fila * (imagenes[i].get_height() + separacion)
        posiciones.append((x, y))
    return posiciones

# Desordenar las rutinas
rutinas = list(rutina_imagenes.keys())
random.shuffle(rutinas)

# Posiciones actuales de las rutinas
posiciones_rutinas = calcular_posiciones_cuadricula([rutina_imagenes[r] for r in rutinas], 8, 20)

# Lista para rastrear las rutinas colocadas correctamente
rutinas_colocadas = []

# Lista que contiene el orden correcto de las rutinas
orden_correcto = ["1 T","26 D", "2 T", "3 T", "4 T", "5 T", ]

num_cuadrados_verdes = len(orden_correcto)

# Tamaño y posición de los cuadrados verdes
cuadrados_verdes_size = 150
num_columnas = 8  # Un cuadrado por rutina
num_filas = (num_cuadrados_verdes + num_columnas - 1) // num_columnas
espacio_entre_cuadrados_x = (screen_info.current_w - cuadrados_verdes_size * num_columnas) // (num_columnas + 1)
espacio_entre_cuadrados_y = (screen_info.current_h - cuadrados_verdes_size * num_filas) // (num_filas + 1)
# Calculamos la posición de los cuadrados verdes en una fila en la parte inferior de la pantalla
posicion_cuadrados_verdes = [(espacio_entre_cuadrados_x * (i % num_columnas + 1) + cuadrados_verdes_size * (i % num_columnas),
                              screen_info.current_h // 4 + espacio_entre_cuadrados_y * (i // num_columnas + 1)) for i in range(num_cuadrados_verdes)]

# Ajuste en la parte inferior
mensaje_margin = 50

# Bucle principal del juego
ejecutando = True
arrastrando = False
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if not arrastrando:
                pos_mouse = pygame.mouse.get_pos()
                for i, pos in enumerate(posiciones_rutinas):
                    rect = pygame.Rect(pos[0], pos[1], rutina_imagenes[rutinas[i]].get_width(), rutina_imagenes[rutinas[i]].get_height())
                    if rect.collidepoint(pos_mouse):
                        rutina_seleccionada = rutinas[i]
                        indice_seleccionado = i
                        offset_arrastre = (pos[0] - pos_mouse[0], pos[1] - pos_mouse[1])
                        arrastrando = True
                        break
        elif evento.type == pygame.MOUSEBUTTONUP:
            if arrastrando:
                arrastrando = False
                pos_mouse = pygame.mouse.get_pos()
                for i, cuadrado_verde_pos in enumerate(posicion_cuadrados_verdes):
                    if cuadrado_verde_pos[0] < pos_mouse[0] < cuadrado_verde_pos[0] + cuadrados_verdes_size and cuadrado_verde_pos[1] < pos_mouse[1] < cuadrado_verde_pos[1] + cuadrados_verdes_size:
                        if rutina_seleccionada == orden_correcto[i]:
                            posiciones_rutinas[indice_seleccionado] = (cuadrado_verde_pos[0] + (cuadrados_verdes_size - rutina_imagenes[rutina_seleccionada].get_width()) // 2, cuadrado_verde_pos[1] + (cuadrados_verdes_size - rutina_imagenes[rutina_seleccionada].get_height()) // 2)
                            rutinas_colocadas.append(rutina_seleccionada)
                            if len(rutinas_colocadas) == len(orden_correcto):  # Todas las rutinas colocadas correctamente
                                # Verificar si las rutinas colocadas coinciden con el orden correcto
                                if rutinas_colocadas == orden_correcto:
                                    pass  # El orden es correcto
                                else:
                                    # Si el orden es incorrecto, restablecer el juego
                                    random.shuffle(rutinas)
                                    rutinas_colocadas.clear()
                                    posiciones_rutinas = calcular_posiciones_cuadricula([rutina_imagenes[r] for r in rutinas], 8, 20)
                        else:
                            # Si la rutina colocada es incorrecta, restablecer el juego
                            random.shuffle(rutinas)
                            rutinas_colocadas.clear()
                            posiciones_rutinas = calcular_posiciones_cuadricula([rutina_imagenes[r] for r in rutinas], 8, 20)

        elif evento.type == pygame.MOUSEMOTION:
            if arrastrando:
                pos_mouse = pygame.mouse.get_pos()
                posiciones_rutinas[indice_seleccionado] = (pos_mouse[0] + offset_arrastre[0], pos_mouse[1] + offset_arrastre[1])

    screen.fill((0, 98, 255))  # Rellena la pantalla con azul (RGB: 0, 0, 255)

    # Dibujar el título "Mañana" en la esquina inferior izquierda
    titulo = title_font.render("Tarde", True, BLANCO)
    screen.blit(titulo, (20, screen_info.current_h - titulo.get_height() - mensaje_margin))

    # Dibujar las rutinas
    for i, pos in enumerate(posiciones_rutinas):
        screen.blit(rutina_imagenes[rutinas[i]], pos)

    # Dibujar los cuadrados verdes
    for i, cuadrado_verde_pos in enumerate(posicion_cuadrados_verdes):
        pygame.draw.rect(screen, VERDE, (cuadrado_verde_pos[0], cuadrado_verde_pos[1], cuadrados_verdes_size, cuadrados_verdes_size), 2)

    # Mostrar el mensaje de salida
    mensaje = font.render("Presiona ESC para salir", True, ROJO)
    screen.blit(mensaje, (screen_info.current_w - mensaje.get_width() - 20, screen_info.current_h - mensaje.get_height() - mensaje_margin))

    # Actualizar la pantalla
    pygame.display.flip()

# Finalizar Pygame y salir del programa
pygame.quit()
sys.exit()