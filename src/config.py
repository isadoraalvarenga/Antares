# Configurações centrais do jogo (tela, cores e caminhos de arquivos).
import pygame

# Resolução dinâmica: usa o tamanho real do monitor (sem barras pretas em
# nenhuma proporção). Precisamos inicializar só o subsistema de vídeo para
# conseguir consultar a resolução do desktop antes de criar a janela.
pygame.display.init()
_info = pygame.display.Info()
LARGURA_TELA = _info.current_w
ALTURA_TELA = _info.current_h

FPS = 60

TITULO_JOGO = "Antares"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
RED_ANTARES = (178, 38, 0)
WALLPAPER = "assets/imagens/starsky.jpg"

CAMINHO_RECORDE = "data/recorde.txt"
CAMINHO_SPRITES = "assets/imagens/spritesheet.bmp"
FONTE = "assets/fontes/Starjout.ttf"

CONFIG_FASES = {
    1: {"total_inimigos": 8, "intervalo_spawn": 2.0, "vel_inimigo": 4},
    2: {"total_inimigos": 15, "intervalo_spawn": 1.25, "vel_inimigo": 5},
    3: {"total_inimigos": 22, "intervalo_spawn": 0.90, "vel_inimigo": 6},
    4: {"total_inimigos": 1, "intervalo_spawn": 999.0, "vel_inimigo": 2}#Estrela da morte
}