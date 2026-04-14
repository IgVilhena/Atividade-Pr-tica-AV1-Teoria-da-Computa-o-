"""
============================================================
 MAQUINA DE TRACAS - Potenciacao Inteira (base^exp)
 Disciplina: Teoria da Computabilidade
 Metodo: Maquina de Tracas (Trace Machine)
============================================================

 A Maquina de Tracas executa um programa monolitico normalizado
 passo a passo e registra cada configuracao (PC, estado das
 variaveis) como um elemento da cadeia de traco.

 Cadeia: sigma0 -> sigma1 -> sigma2 -> ... -> sigmaN
 Cada sigma_i = (rotulo_i, {var: valor, ...})

 Programas analisados:
   P1 - potencia com contagem CRESCENTE via goto/rotulos (monolitico C)
   P2 - potencia iterativa Python NORMALIZADA para L1-L7 (equivalente a P1)
   P3 - potencia com contagem DECRESCENTE (nao equivalente a P1)

 Executar: python3 maquina_de_tracas.py

============================================================
"""

from copy import deepcopy


# ============================================================
# Estrutura de instrucoes do programa monolitico normalizado
# ============================================================

class MaquinaDeTracas:
    """
    Simula a execucao de um programa monolitico normalizado
    e registra a cadeia completa de configuracoes (tracas).
    """

    def __init__(self, instrucoes: dict, nome: str = "P"):
        """
        instrucoes: dict {rotulo: {'tipo': ..., ...}}
        Tipos suportados: ATRIB, IF_GOTO, GOTO, HALT
        """
        self.instrucoes = instrucoes
        self.nome = nome

    def executar(self, entrada: dict, max_passos: int = 500) -> list[dict]:
        """
        Executa o programa com o estado inicial `entrada`
        e retorna a lista de configuracoes (cadeia de tracas).
        """
        estado = deepcopy(entrada)
        pc     = 1          # program counter: comeca no rotulo 1
        cadeia = []

        for _ in range(max_passos):
            # Registra configuracao ANTES da execucao da instrucao
            cadeia.append({'rotulo': pc, 'estado': deepcopy(estado)})

            instrucao = self.instrucoes.get(pc)
            if instrucao is None:
                break

            tipo = instrucao['tipo']

            if tipo == 'HALT':
                break

            elif tipo == 'ATRIB':
                estado[instrucao['var']] = instrucao['expr'](estado)
                pc += 1

            elif tipo == 'IF_GOTO':
                if instrucao['cond'](estado):
                    pc = instrucao['destino']
                else:
                    pc += 1

            elif tipo == 'GOTO':
                pc = instrucao['destino']

        return cadeia

    def imprimir_cadeia(self, cadeia: list[dict], entrada: dict):
        """Exibe a cadeia de tracas no formato de fita."""
        largura = 62
        print()
        print("=" * largura)
        print(f"  Programa : {self.nome}")
        print(f"  Entrada  : {entrada}")
        print("=" * largura)
        print(f"  {'sigma':>6}  {'Rotulo':>6}  Estado das Variaveis")
        print("-" * largura)
        for i, config in enumerate(cadeia):
            estado_str = "  ".join(f"{k}={v}" for k, v in sorted(config['estado'].items()))
            print(f"  σ{i:<5}   L{config['rotulo']:<5}   {estado_str}")
        print("=" * largura)

        # Resultado final
        ultimo = cadeia[-1]['estado']
        if 'result' in ultimo:
            print(f"  Resultado final : result = {ultimo['result']}")
        print("=" * largura)


# ============================================================
# Definicao dos programas monoliticos normalizados
# ============================================================

#
# P1 - Potencia com contagem CRESCENTE
# Instrucoes:
#   L1: result <- 1
#   L2: count  <- 0
#   L3: SE count >= exp ENTAO GOTO L7
#   L4: result <- result * base
#   L5: count  <- count + 1
#   L6: GOTO L3
#   L7: HALT
#
P1 = MaquinaDeTracas({
    1: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: 1},
    2: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: 0},
    3: {'tipo': 'IF_GOTO', 'cond': lambda s: s['count'] >= s['exp'], 'destino': 7},
    4: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: s['result'] * s['base']},
    5: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['count'] + 1},
    6: {'tipo': 'GOTO',    'destino': 3},
    7: {'tipo': 'HALT'},
}, nome="P1 (contagem crescente: count 0 → exp)")


#
# P2 - Iterativo Normalizado (transcricao do while Python para L1-L7)
#
# O programa iterativo Python:
#   result = 1                →  L1: result ← 1
#   count  = 0                →  L2: count  ← 0
#   while count < exp:        →  L3: SE count ≥ exp ENTAO GOTO L7
#       result = result * base →  L4: result ← result × base
#       count  = count + 1    →  L5: count  ← count + 1
#   # (retorno implicito ao while) → L6: GOTO L3
#   # (fim do while / return)      → L7: HALT
#
# A guarda "count < exp" no while e equivalente ao desvio
# "SE count >= exp ENTAO GOTO L7" — negacao da mesma condicao.
# A cada iteracao, as atribuicoes ocorrem na mesma ordem (L4 → L5)
# e o retorno ao teste e implicito no loop, correspondendo a L6.
# Portanto, as instrucoes normalizadas sao IDENTICAS as de P1.
#
P2 = MaquinaDeTracas({
    1: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: 1},
    2: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: 0},
    3: {'tipo': 'IF_GOTO', 'cond': lambda s: s['count'] >= s['exp'], 'destino': 7},
    4: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: s['result'] * s['base']},
    5: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['count'] + 1},
    6: {'tipo': 'GOTO',    'destino': 3},
    7: {'tipo': 'HALT'},
}, nome="P2 — Iterativo Normalizado (while Python → L1-L7)")


#
# P3 - Potencia com contagem DECRESCENTE
# Instrucoes:
#   L1: result <- 1
#   L2: count  <- exp          <-- diferente de P1 (inicializa com exp)
#   L3: SE count <= 0 ENTAO GOTO L7
#   L4: result <- result * base
#   L5: count  <- count - 1   <-- diferente de P1 (decrementa)
#   L6: GOTO L3
#   L7: HALT
#
P3 = MaquinaDeTracas({
    1: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: 1},
    2: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['exp']},       # count = exp
    3: {'tipo': 'IF_GOTO', 'cond': lambda s: s['count'] <= 0, 'destino': 7},   # testa <= 0
    4: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: s['result'] * s['base']},
    5: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['count'] - 1}, # decrementa
    6: {'tipo': 'GOTO',    'destino': 3},
    7: {'tipo': 'HALT'},
}, nome="P3 (contagem decrescente: count exp → 0)")


# ============================================================
# Comparacao de cadeias: equivalencia forte
# ============================================================

def comparar(cadeia_a: list, cadeia_b: list,
             nome_a: str, nome_b: str, entrada: dict):
    """
    Compara duas cadeias de tracas.
    Dois programas sao FORTEMENTE EQUIVALENTES se e somente se,
    para toda entrada, suas cadeias de tracas sao identicas.
    """
    largura = 62
    print()
    print("=" * largura)
    print(f"  COMPARACAO: {nome_a}  vs  {nome_b}")
    print(f"  Entrada: {entrada}")
    print("=" * largura)

    if len(cadeia_a) != len(cadeia_b):
        print(f"  Tamanho das cadeias: {nome_a}={len(cadeia_a)}  |  {nome_b}={len(cadeia_b)}")

    ponto_divergencia = None
    limite = min(len(cadeia_a), len(cadeia_b))

    for i in range(limite):
        if cadeia_a[i] != cadeia_b[i]:
            ponto_divergencia = i
            break

    if ponto_divergencia is None and len(cadeia_a) == len(cadeia_b):
        print(f"\n  ✓  CADEIAS IDENTICAS PARA ESTA ENTRADA")
        print(f"     Ambas as cadeias possuem {len(cadeia_a)} configuracoes identicas.")
        print(f"     Para a entrada dada, {nome_a} ≡ {nome_b}:")
        print(f"     mesma sequencia de rotulos e estados em cada sigma_i.")
    else:
        idx = ponto_divergencia if ponto_divergencia is not None else limite
        print(f"\n  ✗  NAO FORTEMENTE EQUIVALENTES")
        print(f"     Divergencia detectada em σ{idx}:\n")
        if idx < len(cadeia_a):
            ea = cadeia_a[idx]['estado']
            print(f"     {nome_a}: L{cadeia_a[idx]['rotulo']}  estado={ea}")
        if idx < len(cadeia_b):
            eb = cadeia_b[idx]['estado']
            print(f"     {nome_b}: L{cadeia_b[idx]['rotulo']}  estado={eb}")
        print()
        print(f"     Embora ambos computem o mesmo RESULTADO FINAL,")
        print(f"     os estados intermediarios diferem: os programas")
        print(f"     NAO sao fortemente equivalentes.")

    print("=" * largura)


# ============================================================
# Execucao principal
# ============================================================

if __name__ == "__main__":

    SEPARADOR = "\n" + "#" * 62

    # ----- Entrada de teste principal -----
    entrada = {'base': 2, 'exp': 3}
    print(SEPARADOR)
    print(f"#  MAQUINA DE TRACAS — Potenciacao Inteira")
    print(f"#  Entrada: base={entrada['base']}, exp={entrada['exp']}")
    print(f"#  Esperado: {entrada['base']}^{entrada['exp']} = {entrada['base']**entrada['exp']}")
    print(SEPARADOR)

    # Executa os tres programas
    cadeia_P1 = P1.executar(entrada)
    cadeia_P2 = P2.executar(entrada)
    cadeia_P3 = P3.executar(entrada)

    # Exibe as cadeias de P1, P2 e P3
    P1.imprimir_cadeia(cadeia_P1, entrada)
    P2.imprimir_cadeia(cadeia_P2, entrada)
    P3.imprimir_cadeia(cadeia_P3, entrada)

    # ---- Caso 1: EQUIVALENCIA FORTE (P1 vs P2 — Iterativo Normalizado) ----
    print(SEPARADOR)
    print("#  CASO 1: Equivalencia forte")
    print("#  P1 (monolitico C/goto)  vs  P2 (iterativo Python normalizado para L1-L7)")
    print("#")
    print("#  P1 e P2 sao programas de ORIGENS DIFERENTES (goto vs while),")
    print("#  mas ao normalizar o while em instrucoes atomicas L1-L7,")
    print("#  as cadeias de tracas resultam identicas para toda entrada.")
    print(SEPARADOR)
    comparar(cadeia_P1, cadeia_P2, "P1", "P2-IterNorm", entrada)
    print("  ► Conclusao: P1 e P2 sao FORTEMENTE EQUIVALENTES.")
    print("    Programas de origens distintas (goto vs while) produzem")
    print("    cadeias identicas quando normalizados — equivalencia nao-trivial.")

    # ---- Caso 2: NAO-EQUIVALENCIA FORTE (P1 vs P3) ----
    print(SEPARADOR)
    print("#  CASO 2: Nao-equivalencia forte  —  P1 vs P3")
    print(SEPARADOR)
    comparar(cadeia_P1, cadeia_P3, "P1", "P3", entrada)

    # ---- Teste adicional: entrada com exp=0 ----
    print(SEPARADOR)
    print("#  TESTE EXTRA: exp = 0  (caso base)")
    print(SEPARADOR)
    entrada0 = {'base': 5, 'exp': 0}
    c1 = P1.executar(entrada0)
    c3 = P3.executar(entrada0)
    P1.imprimir_cadeia(c1, entrada0)
    P3.imprimir_cadeia(c3, entrada0)
    comparar(c1, c3, "P1", "P3", entrada0)
    print("  ► ATENCAO: cadeias identicas para exp=0 NAO implicam equivalencia forte.")
    print("    Para exp=3 as cadeias divergem em sigma2 — basta uma entrada diferente")
    print("    para refutar a equivalencia forte (P1 e P3 NAO sao fortemente equiv.).")
