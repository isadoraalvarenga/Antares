import pygame
import random
import math
from src.config import CAMINHO_DEATH_STAR

def pegar_sprite(local_arquivo, x, y, width, height, scale=1):
    """Corta um único elemento de uma spritesheet BMP e remove o fundo."""
    
    # 1. Carrega o BMP e usa .convert() (sem alpha) para otimizar a velocidade
    sheet = pygame.image.load(local_arquivo).convert_alpha()

    # 2. Cria uma superfície padrão para o recorte (não precisa de SRCALPHA aqui)
    image = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # 3. Copia o pedaço da folha BMP para a nossa nova imagem
    image.blit(sheet, (0, 0), (x, y, width, height))
    
    # 4. CONFIGURAÇÃO DA TRANSPARÊNCIA (O segredo para o BMP)
    # Pegamos a cor do pixel no canto superior esquerdo (0,0) do recorte, 
    # assumindo que o fundo do seu sprite começa ali.
    cor_do_fundo = image.get_at((0, 0))
    
    # Dizemos ao Pygame para ignorar essa cor específica na hora de desenhar
    image.set_colorkey(cor_do_fundo)
    
    # 5. Aplica o redimensionamento, se houver
    if scale != 1:
        novo_largura = int(width * scale)
        novo_altura = int(height * scale)
        image = pygame.transform.scale(image, (novo_largura, novo_altura))
        
    return image

class DeathStar:
    def __init__(self, ancora_x, ancora_y):
        self.image = pegar_sprite(CAMINHO_DEATH_STAR, x=0, y=0, width=424, height=412, scale=1)

        self.rect = self.image.get_rect()

        # Recorte do conteudo visivel dentro da imagem (ignora o padding transparente).
        # Serve de base para a hitbox seguir a esfera, e nao o quadrado de 512x512.
        self._bounds = self.image.get_bounding_rect()

        # Nasce centralizada no eixo Y e encostada na borda direita (fora da tela)
        self.rect.y = (ancora_y - self.rect.height) / 2
        self.rect.x = ancora_x

        # Posição X de destino: para de entrar quando estiver totalmente visível à direita
        self.destino_x = ancora_x - self.rect.width
        self.velocidade_entrada = 3
        self.entrando = True

        self.base_y = self.rect.y
        self.angulo = 0
        self.amplitude = 25
        self.velocidade_balanco = 0.02

    @property
    def hitbox(self):
        # Recorte visível posicionado no mundo: acompanha o rect, mas sem o
        # padding transparente, então o tiro só some ao encostar na esfera.
        return self._bounds.move(self.rect.x, self.rect.y)

    def atualizar(self):
        if self.entrando:
            # Desliza para a esquerda até chegar no destino
            self.rect.x -= self.velocidade_entrada
            if self.rect.x <= self.destino_x:
                self.rect.x = self.destino_x
                self.entrando = False
        else:
            # Já entrou: oscila levemente para cima e para baixo
            self.angulo += self.velocidade_balanco
            self.rect.y = self.base_y + math.sin(self.angulo) * self.amplitude

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)


class Obstacle:
    TIPOS = [
        (0.6, 5),   # pequeno → -5%
        (1.0, 10),  # médio   → -10%
        (1.5, 15),  # grande  → -15%
    ]

    def __init__(self, ancho_tela=800, alto_tela=600):
        scale, self.dano = random.choice(self.TIPOS)
        self.image = pegar_sprite(
            "assets/imagens/asteroide_sheet.png",
            x=0, y=0, width=48, height=48, scale=scale
        )
        
        self.rect = self.image.get_rect()
        
        # Sorteia a posição Y de nascimento do asteroide
        self.rect.y = random.randint(0, alto_tela - self.rect.height)

        # Surge o obstáculo da direita para a esquerda
        self.rect.x = ancho_tela
        
        # Sorteia a velocidade de queda
        self.velocidad = random.randint(4, 7)
        
    def atualizar(self):
        # Faz o obstáculo cair no eixo X
        self.rect.x -= self.velocidad
        
    def desenhar(self, tela):
        # Desenha o obstáculo na tela
        tela.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = pegar_sprite(
            "assets/imagens/bullet.png",
            x=0, y=0, width=154, height=64, scale=0.1
        )
        # Reduz o tamanho da bala
        self.rect = self.image.get_rect(midleft=(x, y))
        self.velocidade = 15
        self.dano = 5

    def atualizar(self):
        self.rect.x += self.velocidade

    def desenhar(self, tela):
        tela.blit(self.image, self.rect)

    