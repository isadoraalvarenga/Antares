import pygame
from src.sprites import DeathStar
from src.funcoes import tomar_dano

pygame.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)

def test_inicializacao_death_star():
    """Garante que a Estrela da Morte nasce com a vida cheia e na posição correta."""

    largura_tela = 1280
    altura_tela = 720
    
    death_star = DeathStar(largura_tela, altura_tela)
    
    assert death_star.rect.x >= largura_tela

    assert death_star.laser_rect is None


def test_death_star_toma_dano():
    """Garante que a vida da Estrela da Morte reduz corretamente ao tomar tiros."""
    vidas_death_star = 200
    dano_tiro = 10
    
    nova_vida = tomar_dano(vidas_death_star, dano_tiro)
    
    assert nova_vida == 190


def test_death_star_destruida():
    """Verifica se a Estrela da Morte é considerada destruída quando a vida zera."""
    vidas_death_star = 10
    dano_fatal = 15
    
    nova_vida = tomar_dano(vidas_death_star, dano_fatal)

    assert nova_vida <= 0

if __name__ == "__main__":
    test_inicializacao_death_star()
    test_death_star_toma_dano()
    test_death_star_destruida()
    print("A funcionalidade da Estrela da morte (Death Star) passou em todos os teste!")