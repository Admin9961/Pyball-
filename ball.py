import pygame
import sys
import random

pygame.init()

nero = (0, 0, 0)
bianco = (255, 255, 255)
rosso = (255, 0, 0)

larghezza, altezza = 800, 600
schermo = pygame.display.set_mode((larghezza, altezza))
pygame.display.set_caption("Avoid the Red Balls")

barra_larghezza, barra_altezza = 100, 10
barra = pygame.Rect(larghezza // 2 - barra_larghezza // 2, altezza - 20, barra_larghezza, barra_altezza)

palla_diametro = 20
palla_velocita_y = 3
palla_velocita_x = 1

palla = pygame.Rect(larghezza // 2, 0, palla_diametro, palla_diametro)

class Spara:
    def __init__(self, rect, direction):
        self.rect = rect
        self.direction = direction

palle_rosse = [pygame.Rect(random.randint(0, larghezza - palla_diametro), random.randint(0, altezza // 2), palla_diametro, palla_diametro) for _ in range(2)]
velocita_palle_rosse_x = [random.choice([-1, 1]) for _ in range(2)]
velocita_palle_rosse_y = [random.uniform(0.5, 1.5) for _ in range(2)]

sparate = []

incremento_velocita = 0.1
velocita_massima = 10

altezza_sparata = 10
lunghezza_sparata = 20

punteggio = 0
punteggio_max = 1000000

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                sparata = pygame.Rect(barra.centerx - 2, barra.y - altezza_sparata, 4, altezza_sparata)
                sparate.append(Spara(sparata, 1))

    tasti = pygame.key.get_pressed()
    if tasti[pygame.K_LEFT] and barra.left > 0:
        barra.x -= 7
    if tasti[pygame.K_RIGHT] and barra.right < larghezza:
        barra.x += 7

    palla.y += palla_velocita_y
    palla.x += palla_velocita_x

    if palla.colliderect(barra):
        palla.y = barra.y - palla_diametro
        palla_velocita_y = -abs(palla_velocita_y)
        punteggio += 500
        if punteggio > punteggio_max:
            punteggio = punteggio_max

    for i, palla_rossa in enumerate(palle_rosse):
        palla_rossa.y += velocita_palle_rosse_y[i]
        palla_rossa.x += velocita_palle_rosse_x[i]
        palla_rossa.clamp_ip(schermo.get_rect())

        for sparata in sparate:
            distanza = pygame.math.Vector2(palla_rossa.center) - pygame.math.Vector2(sparata.rect.center)

            soglia_distanza = 600
            if distanza.length() < soglia_distanza:
                sparate.remove(sparata)
                palle_rosse[i] = pygame.Rect(random.randint(0, larghezza - palla_diametro), random.randint(0, altezza // 2), palla_diametro, palla_diametro)
                punteggio += 500
                if punteggio > punteggio_max:
                    punteggio = punteggio_max
                break

        if (
            palla_rossa.colliderect(barra) and
            palla_rossa.bottom >= barra.top and
            palla_rossa.top <= barra.bottom and
            velocita_palle_rosse_y[i] > 0
        ):
            print(f"Hai perso! Colpito da una palla rossa.")
            pygame.quit()
            sys.exit()

        if palla_rossa.right >= larghezza or palla_rossa.left <= 0:
            velocita_palle_rosse_x[i] = -velocita_palle_rosse_x[i]

        if palla_rossa.top <= 0 or palla_rossa.bottom >= altezza:
            velocita_palle_rosse_y[i] = -velocita_palle_rosse_y[i]

    sparate = [s for s in sparate if s.rect.y > 0]

    if palla.bottom > altezza:
        print(f"Hai perso! La palla è caduta. Punteggio finale: {punteggio}")
        pygame.quit()
        sys.exit()

    if palla.left <= 0 or palla.right >= larghezza:
        palla_velocita_x = -palla_velocita_x
    if palla.top <= 0:
        palla_velocita_y = abs(palla_velocita_y)

    if abs(palla_velocita_x) < velocita_massima:
        palla_velocita_x += incremento_velocita

    if abs(palla_velocita_y) < velocita_massima:
        palla_velocita_y += incremento_velocita

    schermo.fill(nero)
    pygame.draw.rect(schermo, bianco, barra)
    pygame.draw.ellipse(schermo, bianco, palla)

    for i, palla_rossa in enumerate(palle_rosse):
        pygame.draw.ellipse(schermo, rosso, palla_rossa)

    for sparata in sparate:
        pygame.draw.rect(schermo, bianco, sparata.rect)

    font = pygame.font.Font(None, 36)
    testo_punteggio = font.render(f"Punteggio: {punteggio}", True, bianco)
    schermo.blit(testo_punteggio, (10, 10))

    for sparata in sparate:
        pygame.draw.rect(schermo, bianco, (sparata.rect.x, sparata.rect.y - altezza_sparata, sparata.rect.width, sparata.rect.height + altezza_sparata))

    pygame.display.flip()
    pygame.time.Clock().tick(30)