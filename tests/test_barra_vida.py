from src.funcoes import tomar_dano, limitar_valor


def test_tomar_dano_reduz_a_vida():
    """Deve diminuir a vida atual pelo valor do dano recebido."""
    assert tomar_dano(100.0, 15.0) == 85.0


def test_tomar_dano_acumulado():
    """Varios danos seguidos devem reduzir a vida de forma acumulada."""
    vidas = 100.0
    vidas = tomar_dano(vidas, 15.0)
    vidas = tomar_dano(vidas, 5.0)
    vidas = tomar_dano(vidas, 3.0)
    assert vidas == 77.0


def test_barra_nunca_fica_negativa():
    """Mesmo com dano maior que a vida, a barra e limitada a zero (nao negativa)."""
    vidas = tomar_dano(5.0, 10.0)            # -5.0 antes de limitar
    vidas = limitar_valor(vidas, 0, 100.0)
    assert vidas == 0


def test_cura_nao_passa_da_vida_maxima():
    """Ao curar, a vida e limitada ao maximo da barra (100)."""
    vidas = limitar_valor(90.0 + 20.0, 0, 100.0)
    assert vidas == 100.0


def test_dano_seguido_de_cura():
    """Tomar dano e depois curar deve refletir o saldo correto na barra."""
    vidas = 100.0
    vidas = tomar_dano(vidas, 40.0)
    vidas = limitar_valor(vidas + 20.0, 0, 100.0)
    assert vidas == 80.0
