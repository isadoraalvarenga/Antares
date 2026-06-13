import pygame
import random

from src.config import (
    LARGURA_TELA,
    ALTURA_TELA,
    FPS,
    TITULO_JOGO,
    CAMINHO_RECORDE,
    FONTE,
    RED_ANTARES,
    BRANCO,
    PRETO,
    CAMINHO_SPRITES,
    CONFIG_FASES
)

from src.funcoes import (
    jogador_perdeu,
    limitar_valor,
    verificar_colisao,
    tomar_dano,
    verificar_vida_baixa,
    calcular_pontos
)
from src.sprites import pegar_sprite, Obstacle, Enemies
from src.dados import (
    salvar_recorde,
    carregar_recorde,
)

def tela_fim_jogo(tela, fundo, relogio):
    """Mostra a tela de fim de jogo. Retorna True para reiniciar, False para sair."""
    # Fontes e textos fixos sao criados uma vez, fora do loop.
    fonte_titulo = pygame.font.Font(FONTE, 100)
    fonte_subtitulo = pygame.font.Font(FONTE, 50)
    fonte_botao = pygame.font.Font(FONTE, 30)

    # Tudo e posicionado a partir do centro da tela, para se adaptar a qualquer
    # resolucao em vez de ficar preso no topo.
    centro_x = LARGURA_TELA // 2
    centro_y = ALTURA_TELA // 2

    titulo = fonte_titulo.render("Antares", True, RED_ANTARES)
    rect_titulo = titulo.get_rect(center=(centro_x, centro_y - 180))

    subtitulo = fonte_subtitulo.render("Game over", True, RED_ANTARES)
    rect_subtitulo = subtitulo.get_rect(center=(centro_x, centro_y - 100))

    rotulo_jogar = fonte_botao.render("Jogar", True, BRANCO)
    rotulo_sair = fonte_botao.render("Sair", True, BRANCO)

    # Areas dos botoes (servem para desenhar e para detectar o clique).
    botao_jogar = pygame.Rect(0, 0, 240, 60)
    botao_jogar.center = (centro_x, centro_y + 30)
    botao_sair = pygame.Rect(0, 0, 240, 60)
    botao_sair.center = (centro_x, centro_y + 120)

    while True:
        relogio.tick(FPS)

        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_jogar.collidepoint(evento.pos):
                    return True
                if botao_sair.collidepoint(evento.pos):
                    return False

        # Cor mais clara quando o mouse esta sobre o botao (efeito hover).
        cor_jogar = (90, 90, 90) if botao_jogar.collidepoint(pos_mouse) else (50, 50, 50)
        cor_sair = (90, 90, 90) if botao_sair.collidepoint(pos_mouse) else (50, 50, 50)

        tela.blit(fundo, (0, 0))
        tela.blit(titulo, rect_titulo)
        tela.blit(subtitulo, rect_subtitulo)

        pygame.draw.rect(tela, cor_jogar, botao_jogar)
        pygame.draw.rect(tela, cor_sair, botao_sair)

        # Centraliza o rotulo dentro do retangulo de cada botao.
        tela.blit(rotulo_jogar, rotulo_jogar.get_rect(center=botao_jogar.center))
        tela.blit(rotulo_sair, rotulo_sair.get_rect(center=botao_sair.center))

        pygame.display.flip()




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

def tela_loading(tela, fase_atual, relogio):
    """Tela de loading/reparo entre as fases."""
    fonte = pygame.font.Font(FONTE, 50)
    texto = fonte.render(f"FASE {fase_atual} CONCLUIDA! Iniciando Sistemas...", True, BRANCO)
    rect_texto = texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    
    tela.fill(PRETO)
    tela.blit(texto, rect_texto)
    pygame.display.flip()
    
    pygame.time.wait(2000)

def tela_fase_cinema(tela, fase_atual):
    fonte_grande = pygame.font.Font(FONTE, 80)
    
    tela.fill(PRETO)
    
    txt_fase = fonte_grande.render(f"FASE {fase_atual}", True, RED_ANTARES)
    rect_fase = txt_fase.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    
    tela.blit(txt_fase, rect_fase)
    pygame.display.flip()
    
    pygame.time.wait(1500)

def executar_jogo():
    """Executa o loop principal do jogo e controla estado, colisões e pontuação."""
    pygame.init()

    tela = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA),
        pygame.FULLSCREEN
    )
    pygame.display.set_caption(TITULO_JOGO)

    relogio = pygame.time.Clock()

    # --- Recursos que vivem o programa inteiro (carregados uma unica vez) ---

    # Jogador: usando tamanho 110x110 para capturar o quadrado perfeitamente
    player_image = pegar_sprite("assets/imagens/millenium_falcon_fr.bmp", x=0, y=0, width=118, height=32, scale=1)

    # Ferramenta de Reparo
    ferramenta_image = pegar_sprite(CAMINHO_SPRITES, x=900, y=690, width=200, height=200, scale=0.15)

    # 2. Criando a estrutura de Sprites usando Dicionários
    jogador = {
        "imagem": player_image,
        "rect": player_image.get_rect(topleft=(100, 100))
    }

    FREQUENCIA_ASTEROIDE = 40

    velocidade = 10
    fundo_x = 0
    velocidade_fundo = 5

    recorde = carregar_recorde(CAMINHO_RECORDE)

    imagem_original = pygame.image.load("assets/imagens/starsky.jpg").convert()
    imagem_original = pygame.transform.scale(imagem_original, (LARGURA_TELA, ALTURA_TELA))

    # Loop externo: cada volta e uma nova partida.
    jogando = True
    fase_atual = 1
    while jogando:
        # --- Reset: variaveis que vivem apenas uma partida nascem do zero ---
        lista_obstaculos = []
        lista_enemies = []
        lista_lasers_enemies = []
        lista_lasers_jogador = []

        cooldown_tiro_jogador = 0
        contador_tempo = 0
        pontos = 0
        vidas = 100.0
        ferramenta_coletada_na_fase = False
        jogador["rect"].topleft = (100, 100)


        ferramenta_na_tela = False
        ferramenta_rect = pygame.Rect(0, 0, 0, 0)
        ferramenta_velocidade = 5
        chances_perdidas = 0

        regras_fase = CONFIG_FASES[fase_atual]
        enemies_restantes_para_nascer = regras_fase["total_enemies"]
        total_enemies_da_fase = regras_fase["total_enemies"]
        intervalo_spawn = regras_fase["intervalo_spawn"] * 1000
        velocidade_enemy = regras_fase["vel_enemy"]

        enemies_mortos = 0

        ultimo_spawn_enemy = pygame.time.get_ticks()

        # Loop interno (partida): processa entrada, atualiza estado e renderiza.
        rodando = True
        while rodando:
            relogio.tick(FPS)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                    jogando = False
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando = False

            
            fundo_x -= velocidade_fundo
            if fundo_x <= -LARGURA_TELA:
                fundo_x = 0

            teclas = pygame.key.get_pressed()

            if cooldown_tiro_jogador > 0:
                cooldown_tiro_jogador -= 1

            if teclas[pygame.K_SPACE] and cooldown_tiro_jogador == 0:
                # Cria um retângulo temporário para o laser saindo da frente da sua nave
                novo_laser = pygame.Rect(jogador["rect"].right, jogador["rect"].centery, 15, 4)
                lista_lasers_jogador.append(novo_laser)
                cooldown_tiro_jogador = 15

            # Movimentação alterando direto os eixos X e Y do retângulo do jogador
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

            tempo_atual = pygame.time.get_ticks()

            if enemies_restantes_para_nascer > 0:
                if tempo_atual - ultimo_spawn_enemy >= intervalo_spawn:
                    
                    lista_enemies.append(Enemies(LARGURA_TELA, ALTURA_TELA, velocidade_enemy))
                    enemies_restantes_para_nascer -= 1
                    ultimo_spawn_enemy = tempo_atual 

            for enemy in lista_enemies[:]:
                enemy.atualizar(lista_lasers_enemies)

                if verificar_colisao(jogador["rect"], enemy.rect):
                    vidas = tomar_dano(vidas, 15.0) 
                    lista_enemies.remove(enemy)
                    enemies_restantes_para_nascer += 1 
                    continue

                if enemy.rect.x < -enemy.rect.width:
                    lista_enemies.remove(enemy)
                    enemies_restantes_para_nascer += 1

            for laser_en in lista_lasers_enemies[:]:
                laser_en.atualizar()

                if verificar_colisao(jogador["rect"], laser_en.rect):
                    vidas = tomar_dano(vidas, 5.0) # Cada tiro tira 5% de vida
                    lista_lasers_enemies.remove(laser_en)
                    continue
                
                if laser_en.rect.x < -laser_en.rect.width:
                    lista_lasers_enemies.remove(laser_en)

            for laser_pl in lista_lasers_jogador[:]:
                laser_pl.x += 15 
                
                if laser_pl.x > LARGURA_TELA:
                    lista_lasers_jogador.remove(laser_pl)
                    continue
                
                for enemy in lista_enemies[:]:
                    if verificar_colisao(laser_pl, enemy.rect):
                        pontos = calcular_pontos(pontos, 100)
                        enemies_mortos += 1 
                        lista_enemies.remove(enemy)
                        if laser_pl in lista_lasers_jogador:
                            lista_lasers_jogador.remove(laser_pl)
                        break

            if enemies_mortos >= total_enemies_da_fase:
                tela_loading(tela, fase_atual, relogio)
                fase_atual += 1 
                
                if fase_atual > 4:
                    rodando = False
                    fase_atual = 1 
                else:
                    tela_fase_cinema(tela, fase_atual)

                    regras_fase = CONFIG_FASES[fase_atual]
                    enemies_restantes_para_nascer = regras_fase["total_enemies"]
                    total_enemies_da_fase = regras_fase["total_enemies"]
                    intervalo_spawn = regras_fase["intervalo_spawn"] * 1000
                    velocidade_enemy = regras_fase["vel_enemy"]

                    lista_enemies.clear()
                    lista_lasers_enemies.clear()
                    lista_obstaculos.clear()

                    enemies_mortos = 0
                    ultimo_spawn_enemy = pygame.time.get_ticks()
                    ferramenta_coletada_na_fase = False

            contador_tempo += 1
            if contador_tempo >= FREQUENCIA_ASTEROIDE:
                lista_obstaculos.append(Obstacle(LARGURA_TELA, ALTURA_TELA))
                contador_tempo = 0

            if verificar_vida_baixa(vidas) and not ferramenta_na_tela and not ferramenta_coletada_na_fase:
                if random.random() < 0.005:
                    ferramenta_rect = ferramenta_image.get_rect()
                    ferramenta_rect.x = LARGURA_TELA 
                    ferramenta_rect.y = random.randint(0, ALTURA_TELA - ferramenta_rect.height)
                    ferramenta_na_tela = True

            if ferramenta_na_tela:
                ferramenta_rect.x -= ferramenta_velocidade
                
                if verificar_colisao(jogador["rect"], ferramenta_rect):
                    vidas = limitar_valor(vidas + 20.0, 0, 100.0)
                    ferramenta_coletada_na_fase = True
                    ferramenta_na_tela = False
                
                elif ferramenta_rect.x < -ferramenta_rect.width:
                    ferramenta_na_tela = False
                    chances_perdidas += 1
                    if chances_perdidas >= 3:
                        vidas = tomar_dano(vidas, 3.0)
                        chances_perdidas = 0

            for obstaculo in lista_obstaculos[:]:
                obstaculo.atualizar()

                if verificar_colisao(jogador["rect"], obstaculo.rect):
                    vidas = tomar_dano(vidas, obstaculo.dano)
                    lista_obstaculos.remove(obstaculo)

                elif obstaculo.rect.y > ALTURA_TELA:
                    lista_obstaculos.remove(obstaculo)

            if jogador_perdeu(vidas):
                 
                 rodando = False

            if pontos > recorde:
                recorde = pontos
                salvar_recorde(CAMINHO_RECORDE, recorde)

            tela.blit(imagem_original, (fundo_x, 0))
            tela.blit(imagem_original, (fundo_x + LARGURA_TELA, 0))

            for laser_en in lista_lasers_enemies:
                laser_en.desenhar(tela)

            for enemy in lista_enemies:
                enemy.desenhar(tela)

            for laser_pl in lista_lasers_jogador:
                pygame.draw.rect(tela, (0, 255, 0), laser_pl)

            tela.blit(jogador["imagem"], jogador["rect"])

            if ferramenta_na_tela:
                tela.blit(ferramenta_image, ferramenta_rect)
                          
            for obstaculo in lista_obstaculos:
                obstaculo.desenhar(tela)

            desenhar_barra_vida(tela, 20, 20, vidas, vidas_maximas=100)

            fonte_hud = pygame.font.Font(FONTE, 24)

            texto_fase = fonte_hud.render(f"FASE {fase_atual}", True, BRANCO)
            rect_fase = texto_fase.get_rect()
           
            rect_fase.topright = (LARGURA_TELA - 20, 20)
            tela.blit(texto_fase, rect_fase)
            
            texto_alvo = fonte_hud.render(f"ALVOS: {enemies_mortos}/{total_enemies_da_fase}", True, BRANCO)
            rect_alvo = texto_alvo.get_rect()
            
            rect_alvo.topright = (LARGURA_TELA - 20, rect_fase.bottom + 5)
            tela.blit(texto_alvo, rect_alvo)

            pygame.display.flip()

        # A partida acabou. Se o jogador nao fechou a janela, mostra a tela de fim.
        if jogando:
            jogando = tela_fim_jogo(tela, imagem_original, relogio)

    pygame.quit()

if __name__ == "__main__":
    executar_jogo()