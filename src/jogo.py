import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
)

from src.funcoes import (
    calcular_pontos,
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
)
from src.sprites import pegar_sprite, Obstacle
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)


def desenhar_barra_vida(superficie, x, y, vidas_atuais, vidas_maximas=3):
    comprimento_barra = 150
    altura_barra = 15
    proporcao = max(0, vidas_atuais) / vidas_maximas
    largura_vida = int(comprimento_barra * proporcao)
    
    rect_fundo = pygame.Rect(x, y, comprimento_barra, altura_barra)
    rect_vida = pygame.Rect(x, y, largura_vida, altura_barra)
    
    pygame.draw.rect(superficie, (255, 0, 0), rect_fundo)
    pygame.draw.rect(superficie, (0, 255, 0), rect_vida)
    pygame.draw.rect(superficie, (255, 255, 255), rect_fundo, 2)


def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()
    rodando = True

    # 1. Carregando as imagens recortadas do Spritesheet

    # Jogador: usando tamanho 110x110 para capturar o quadrado perfeitamente
    player_image = pegar_sprite("assets/imagens/millenium_falcon_fr.bmp", x=0, y=0, width=118, height=32, scale=1)

    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }

    lista_obstaculos = []
    contador_tempo = 0
    FREQUENCIA_ASTEROIDE = 40

    velocidade = 10
    pontos = 0
    vidas = 3
    recorde = carregar_recorde(CAMINHO_RECORDE)

    imagem_original = pygame.image.load("assets/imagens/starsky.jpg").convert()
    imagem_original = pygame.transform.scale(imagem_original, (800, 600))

    # Loop principal: processa entrada, atualiza estado e renderiza a cena.
    while rodando:
        relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando = False

        teclas = pygame.key.get_pressed()

        # Movimentação alterando direto os eixos X e Y do retângulo do jogador
        # CORRIGIDO: Mudei de 'velocidad' para 'velocidade' para não travar o loop
        if teclas[pygame.K_LEFT]:
            jogador["rect"].x -= velocidade
        if teclas[pygame.K_RIGHT]:
            jogador["rect"].x += velocidade
        if teclas[pygame.K_UP]:
            jogador["rect"].y -= velocidade
        if teclas[pygame.K_DOWN]:
            jogador["rect"].y += velocidade

        # Limitando o jogador dentro das bordas da tela usando as propriedades do Rect
        jogador["rect"].x = limitar_valor(jogador["rect"].x, 0, LARGURA_TELA - jogador["rect"].width)
        jogador["rect"].y = limitar_valor(jogador["rect"].y, 0, ALTURA_TELA - jogador["rect"].height)

        contador_tempo += 1
        if contador_tempo >= FREQUENCIA_ASTEROIDE:
            lista_obstaculos.append(Obstacle(LARGURA_TELA))
            contador_tempo = 0

        for obstaculo in lista_obstaculos[:]:
            obstaculo.atualizar()

            if verificar_colisao(jogador["rect"], obstaculo.rect):
                vidas = tomar_dano(vidas, 1)
                lista_obstaculos.remove(obstaculo)

            elif obstaculo.rect.y > ALTURA_TELA:
                lista_obstaculos.remove(obstaculo)

        # Regras de fim de jogo e recorde
        if jogador_perdeu(vidas):
            rodando = False

        if pontos > recorde:
            recorde = pontos
            salvar_recorde(CAMINHO_RECORDE, recorde)

        tela.blit(imagem_original, (0, 0))

        tela.blit(jogador["imagem"], jogador["rect"])

        for obstaculo in lista_obstaculos:
            obstaculo.desenhar(tela)

        desenhar_barra_vida(tela, 20, 20, vidas, vidas_maximas=3)

        pygame.display.flip()

    pygame.quit()