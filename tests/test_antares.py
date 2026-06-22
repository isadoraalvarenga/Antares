from src.funcoes import _gerar_matriz_estrela, _obter_paleta_antares, _misturar_cor, iniciar_legenda


def test_matriz_estrela_tem_o_tamanho_da_grade_pedido():
    """A matriz gerada deve ter NxN celulas, onde N e o tamanho da grade."""
    matriz = _gerar_matriz_estrela(tamanho_grade=14)
    assert len(matriz) == 14
    assert all(len(linha) == 14 for linha in matriz)


def test_matriz_estrela_usa_apenas_codigos_validos():
    """Cada celula deve ser um dos codigos conhecidos: vazio, contorno, nucleo, brilho ou destaque."""
    matriz = _gerar_matriz_estrela()
    codigos_validos = {0, 1, 2, 3, 4}
    codigos_usados = {valor for linha in matriz for valor in linha}
    assert codigos_usados.issubset(codigos_validos)


def test_matriz_estrela_tem_nucleo_brilhante_no_centro():
    """O centro da estrela deve ser preenchido com o codigo de brilho interno (3)."""
    matriz = _gerar_matriz_estrela(tamanho_grade=14)
    assert matriz[6][6] == 3
    assert matriz[7][7] == 3


def test_matriz_estrela_tem_exatamente_um_ponto_de_destaque():
    """Deve existir o pixel de reflexo (codigo 4) na matriz, usado pelo brilho do avatar."""
    matriz = _gerar_matriz_estrela()
    total_destaques = sum(linha.count(4) for linha in matriz)
    assert total_destaques == 1


def test_paleta_antares_fase_1_tem_cores_escuras_de_inicio():
    """Na fase 1 a Antares deve estar com a paleta vermelho/laranja escura."""
    paleta = _obter_paleta_antares(1)
    assert paleta["contorno"] == (90, 20, 0)
    assert paleta["nucleo"] == (178, 38, 0)


def test_paleta_antares_fica_mais_clara_em_fases_avancadas():
    """A cor de destaque deve clarear conforme a fase avanca (1 -> 4)."""
    destaque_fase_1 = _obter_paleta_antares(1)["destaque"]
    destaque_fase_4 = _obter_paleta_antares(4)["destaque"]
    assert sum(destaque_fase_4) > sum(destaque_fase_1)


def test_paleta_antares_com_fase_invalida_usa_fase_1_como_padrao():
    """Uma fase nao mapeada deve cair na paleta da fase 1, sem quebrar o jogo."""
    assert _obter_paleta_antares(99) == _obter_paleta_antares(1)


def test_misturar_cor_com_fator_zero_retorna_a_primeira_cor():
    """Fator 0 nao deve misturar nada, retornando a cor de origem."""
    assert _misturar_cor((10, 20, 30), (110, 120, 130), 0) == (10, 20, 30)


def test_misturar_cor_com_fator_um_retorna_a_segunda_cor():
    """Fator 1 deve retornar totalmente a cor de destino."""
    assert _misturar_cor((10, 20, 30), (110, 120, 130), 1) == (110, 120, 130)


def test_misturar_cor_com_fator_meio_faz_a_media_das_cores():
    """Fator 0.5 deve resultar no ponto intermediario entre as duas cores."""
    assert _misturar_cor((0, 0, 0), (200, 200, 200), 0.5) == (100, 100, 100)


def test_iniciar_legenda_preenche_o_estado_corretamente():
    """Deve armazenar o texto e resetar os contadores do efeito de digitacao."""
    estado_legenda = {}
    resultado = iniciar_legenda(estado_legenda, "Voce nao vai escapar de mim.")

    assert resultado["texto"] == "Voce nao vai escapar de mim."
    assert resultado["caracteres_visiveis"] == 0
    assert resultado["temporizador"] == 0
    assert resultado["tempo_parada"] == 0
    assert resultado["ativa"] is True


def test_iniciar_legenda_toca_o_som_quando_fornecido():
    """Se um som for passado, ele deve ser tocado ao iniciar a fala."""

    class SomFalso:
        def __init__(self):
            self.tocado = False

        def play(self):
            self.tocado = True

    som = SomFalso()
    iniciar_legenda({}, "Fala qualquer", som=som)

    assert som.tocado is True


def test_iniciar_legenda_nao_quebra_quando_som_nao_e_fornecido():
    """Sem som (None), a funcao deve apenas atualizar o estado, sem erro."""
    estado_legenda = iniciar_legenda({}, "Fala sem som")
    assert estado_legenda["ativa"] is True