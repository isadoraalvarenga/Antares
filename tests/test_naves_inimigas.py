import pygame
from src.sprites import Enemies

def inicializar_ambiente():
    """Prepara o Pygame em segundo plano para podermos criar os Sprites."""
    pygame.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME)

def testar_comportamento_do_inimigo():
    print("Iniciando testes da nave inimiga...")

    # 1. Configuração dos dados de teste
    largura_tela = 1280
    altura_tela = 720
    velocidade = 10
    
    # 2. Cria o objeto para testar
    inimigo = Enemies(largura_tela, altura_tela, velocidade)

    # 3. Teste de Spawn - O inimigo deve nascer da metade da tela para a direita
    assert inimigo.rect.x >= largura_tela, f"Erro: Inimigo nasceu na posição X {inimigo.rect.x}, devia ser fora da tela."
    assert 0 <= inimigo.rect.y <= altura_tela, f"Erro: Inimigo nasceu fora dos limites verticais (Y: {inimigo.rect.y})."
    print("Teste de spawn passou!")

    # 4. Teste de Movimentação
    posicao_x_inicial = inimigo.rect.x
    lista_lasers_falsa = []
    
    # Simula a atualização de 1 frame do jogo
    inimigo.atualizar(lista_lasers_falsa)
    
    # Como ele se move para a esquerda, o X novo deve ser menor que o anterior
    assert inimigo.rect.x < posicao_x_inicial, "Erro: O inimigo não se moveu para a esquerda."
    assert inimigo.rect.x == (posicao_x_inicial - velocidade), f"Erro: Velocidade errada. Esperado: {posicao_x_inicial - velocidade}, Obtido: {inimigo.rect.x}"
    print("Teste de movimentação passou!")

    # 5. Teste de Disparo
    lista_lasers = []
    for _ in range(1000):
        inimigo.atualizar(lista_lasers)
        if len(lista_lasers) > 0:
            break
            
    assert len(lista_lasers) > 0, "Erro: O inimigo passou por 100 frames e não disparou nenhum laser."
    print("Teste de disparo passou!")

    print("Todos os testes da classe Enemies passaram perfeitamente!")

if __name__ == "__main__":
    inicializar_ambiente()
    try:
        testar_comportamento_do_inimigo()
    except AssertionError as erro:
        print(f"\n[FALHA NO TESTE] {erro}")
    finally:
        pygame.quit()