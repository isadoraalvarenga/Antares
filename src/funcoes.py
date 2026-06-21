import pygame
import random
from pygame import mixer


class _SomMudo:
    """Evita que a inicialização do aúdio em SO sem driver de aúdio disponível crashe a aplicação"""

    def play(self, *args, **kwargs):
        return None

    def stop(self, *args, **kwargs):
        return None

    def set_volume(self, *args, **kwargs):
        return None


_ARQUIVOS_SONS = {
    "coleta_gema": "assets/sons/coleta_gema.mp3",
    "colisao_nave": "assets/sons/colisao_asteroide-nave.mp3",
    "conclusao_jogo": "assets/sons/conclusao_jogo.mp3",
    "fase_deathstar": "assets/sons/fase_deathstar.mp3",
    "laser_deathstar": "assets/sons/laser_deathstar.mp3",
    "tela_reparo": "assets/sons/tela_reparo.mp3",
    "musica_fase_123": "assets/sons/somdefundo123.ogg",
    "tiro_jogador": "assets/sons/somtironossanave.wav",
    "tiro_inimigo": "assets/sons/somtironaveinimiga_1.wav",
    "morte_personagens": "assets/sons/sommorteinimigo.wav",
    "conclusao_fase": "assets/sons/passadefase.wav"
}


def carregar_sons():
    """Carrega os sons gerais do jogo"""
    try:
        mixer.init()
    except pygame.error:
        return {nome: _SomMudo() for nome in _ARQUIVOS_SONS}

    sons = {nome: pygame.mixer.Sound(caminho) for nome, caminho in _ARQUIVOS_SONS.items()}
    for som in sons.values():
        som.set_volume(0.15)
    return sons


sons_jogo = carregar_sons()

def calcular_pontos(pontos_atual, pontos_ganhos):
    """Soma os pontos ganhos à pontuação atual."""
    return pontos_atual + pontos_ganhos


def tomar_dano(vida_atual, dano):
    """Reduz a vida atual com base no dano recebido."""
    return vida_atual - dano


def jogador_perdeu(vidas):
    """Indica se o jogador ficou sem vidas."""
    return vidas <= 0


def limitar_valor(valor, minimo, maximo):
    """Mantém um valor dentro do intervalo [minimo, maximo]."""
    if valor < minimo:
        return minimo
    if valor > maximo:
        return maximo
    return valor


def verificar_colisao(retangulo_1, retangulo_2):
    """Verifica sobreposição entre dois retângulos do Pygame."""
    return retangulo_1.colliderect(retangulo_2)


def iniciar_entrada(jogador, ALTURA_TELA):
    """Posiciona a nave fora da tela (à esquerda, centralizada no Y) para a
    animação de entrada e retorna True para o estado 'entrando'."""
    jogador["rect"].y = (ALTURA_TELA - jogador["rect"].height) / 2
    jogador["rect"].x = -jogador["rect"].width - 5
    return True


def verificar_vida_baixa(vidas):
    return vidas <= 35.0


def tela_reparo(tela, relogio, perguntas_disponiveis, print_jogo, LARGURA_TELA, ALTURA_TELA, FPS, FONTE, BRANCO):
    """Abre uma janela de quiz com uma pergunta aleatória por cima do jogo pausado."""
    if not perguntas_disponiveis:
        return False, None
    
    fonte_pergunta = pygame.font.SysFont("Arial", 22, bold=True)
    fonte_opcao = pygame.font.SysFont("Courier New", 18)
    fonte_aviso = pygame.font.SysFont("Arial", 26, bold=True)
    
    questao = random.choice(perguntas_disponiveis)
    
    largura_janela, altura_janela = 920, 600
    x_janela = (LARGURA_TELA - largura_janela) // 2
    y_janela = (ALTURA_TELA - altura_janela) // 2
    rect_janela = pygame.Rect(x_janela, y_janela, largura_janela, altura_janela)
    
    def desenhar_texto_multi_linha(superficie, texto, fonte, cor, x, y, largura_maxima):
        palavras = texto.split(' ')
        linhas = []
        linha_atual = ""
        
        for palavra in palavras:
            testar_linha = linha_atual + palavra + " "
            if fonte.size(testar_linha)[0] < largura_maxima:
                linha_atual = testar_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        linhas.append(linha_atual)
        
        offset_y = 0
        for linha in linhas: # <--- CORRIGIDO AQUI (de 'lines' para 'linhas')
            render_linha = fonte.render(linha.strip(), True, cor)
            superficie.blit(render_linha, (x, y + offset_y))
            offset_y += fonte.get_linesize()
        return offset_y

    retangulos_opcoes = []
    for i in range(len(questao["opcoes"])):
        rect_opcao = pygame.Rect(x_janela + 60, y_janela + 220 + (i * 75), largura_janela - 120, 55)
        retangulos_opcoes.append(rect_opcao)

    respondendo = True
    acertou = False

    imagem_fundo_reparo = pygame.image.load("assets/imagens/imagem-tela-de-reparo.png").convert_alpha()
    imagem_fundo_reparo = pygame.transform.scale(imagem_fundo_reparo, (largura_janela, altura_janela))

    def desenhar_botao_pixel_art(superficie, rect, cor_fundo, cor_borda_escura, cor_borda_clara, espessura=4):
        # Corpo principal do botão
        pygame.draw.rect(superficie, cor_fundo, rect)
        
        # Linhas de sombra/borda escura (inferior e direita)
        pygame.draw.line(superficie, cor_borda_escura, (rect.left, rect.bottom - 1), (rect.right, rect.bottom - 1), espessura)
        pygame.draw.line(superficie, cor_borda_escura, (rect.right - 1, rect.top), (rect.right - 1, rect.bottom), espessura)
        
        # Linhas de luz/borda clara (superior e esquerda)
        pygame.draw.line(superficie, cor_borda_clara, (rect.left, rect.top), (rect.right, rect.top), espessura)
        pygame.draw.line(superficie, cor_borda_clara, (rect.left, rect.top), (rect.left, rect.bottom), espessura)

    # Cores no estilo Sci-Fi / Cyberpunk Pixel Art
    COR_FUNDO_BTN = (20, 20, 35)
    COR_BORDA_ESCURA = (5, 5, 15)
    COR_BORDA_CLARA = (0, 180, 255)
    COR_HOVER_CLARA = (0, 255, 200)

    largura_caixa_pergunta, altura_caixa_pergunta = largura_janela - 120, 130
    rect_pergunta = pygame.Rect(x_janela + 60, y_janela + 40, largura_caixa_pergunta, altura_caixa_pergunta)

    while respondendo:
        relogio.tick(FPS)
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                for idx_clique, rect_opcao in enumerate(retangulos_opcoes):
                    if rect_opcao.collidepoint(evento.pos):
                        
                        # Preparação prévia do fundo do Pop-up para o aviso
                        tela.blit(print_jogo, (0, 0))
                        tela.blit(imagem_fundo_reparo, rect_janela.topleft)

                        if idx_clique == questao["correta"]:
                            acertou = True
                            texto_aviso = fonte_aviso.render("CORRETO! +20% DE SINAL RECUPERADO", True, (0, 255, 0))
                        else:
                            texto_aviso = fonte_aviso.render("SISTEMA FALHOU! REPARO INDISPONÍVEL", True, (255, 0, 0))
                        
                        # Desenha o aviso centralizado
                        rect_aviso = texto_aviso.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
                        tela.blit(texto_aviso, rect_aviso)
                        
                        # Força o display a atualizar antes do wait travar a execução
                        pygame.display.update()
                        
                        # Tela estática por 1.5 segundos após responder
                        pygame.time.wait(1500)
                        respondendo = False
        
        # Desenho padrão do loop enquanto o usuário escolhe a resposta
        if respondendo:
            tela.blit(print_jogo, (0, 0))
            tela.blit(imagem_fundo_reparo, rect_janela.topleft)
            
            desenhar_botao_pixel_art(tela, rect_pergunta, COR_FUNDO_BTN, COR_BORDA_ESCURA, COR_BORDA_CLARA)
            desenhar_texto_multi_linha(tela, questao["pergunta"], fonte_pergunta, BRANCO, rect_pergunta.x + 25, rect_pergunta.y + 25, largura_caixa_pergunta - 50)
            
            letras_prefixo = ["A) ", "B) ", "C) ", "D) "]
            for i, opcao in enumerate(questao["opcoes"]):
                rect_opcao = retangulos_opcoes[i]
                
                if rect_opcao.collidepoint(pos_mouse):
                    desenhar_botao_pixel_art(tela, rect_opcao, (30, 30, 55), COR_BORDA_ESCURA, COR_HOVER_CLARA)
                else:
                    desenhar_botao_pixel_art(tela, rect_opcao, COR_FUNDO_BTN, COR_BORDA_ESCURA, COR_BORDA_CLARA)
                
                texto_formatado = f"{letras_prefixo[i]}{opcao}"
                texto_opcao = fonte_opcao.render(texto_formatado, True, BRANCO)
                
                y_centro_texto = rect_opcao.y + (rect_opcao.height - texto_opcao.get_height()) // 2
                tela.blit(texto_opcao, (rect_opcao.x + 25, y_centro_texto))
                
            pygame.display.flip()
        
    return acertou, questao