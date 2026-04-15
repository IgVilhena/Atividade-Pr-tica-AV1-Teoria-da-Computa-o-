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
   P1     - potencia com contagem CRESCENTE (count: 0 -> exp)
   P_iter - forma monolitica normalizada do iterativo.py (L1-L7)
            usado para demonstrar EQUIVALENCIA FORTE com P1
   P3     - potencia com contagem DECRESCENTE (count: exp -> 0)

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
        """Exibe a cadeia de tracas no formato de tabela vertical."""
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

    def imprimir_fita(self, cadeia: list[dict], entrada: dict):
        """
        Exibe a cadeia de tracas no formato de sequencia de fita.

        Formato canonico:
          (L1,{})  ⊢
          (L2,{result=1})  ⊢
          ...
          (L7,{result=8, count=3})      <- HALT

        O simbolo ⊢ le-se "resulta em" (step/yields).
        Variaveis de entrada (base, exp) sao omitidas do estado
        exibido para manter a fita legivel — apenas as variaveis
        modificadas pelo programa (result, count) sao mostradas.
        """
        largura = 62
        print()
        print("=" * largura)
        print(f"  Programa : {self.nome}  [FORMATO DE FITA]")
        print(f"  Entrada  : {entrada}")
        print("=" * largura)

        for i, config in enumerate(cadeia):
            rotulo = f"L{config['rotulo']}"

            # Exibe apenas variaveis de programa (exclui entradas base/exp)
            variaveis_prog = {
                k: v for k, v in sorted(config['estado'].items())
                if k not in ('base', 'exp')
            }

            if variaveis_prog:
                estado_str = ", ".join(f"{k}={v}" for k, v in variaveis_prog.items())
                config_str = f"({rotulo}, {{{estado_str}}})"
            else:
                config_str = f"({rotulo}, {{}})"

            if i < len(cadeia) - 1:
                print(f"  {config_str}  ⊢")
            else:
                print(f"  {config_str}      <- HALT")

        print("=" * largura)
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
}, nome="P1 (monolitico: contagem crescente, count 0 -> exp)")


#
# P_iter - Forma monolitica normalizada do programa iterativo (iterativo.py)
#
# O programa iterativo em Python:
#   result = 1
#   count  = 0
#   while count < exp:
#       result = result * base
#       count  = count + 1
#   return result
#
# Transcrito para instrucoes atomicas L1-L7:
#   L1: result <- 1                        (result = 1)
#   L2: count  <- 0                        (count  = 0)
#   L3: SE count >= exp ENTAO GOTO L7      (negacao da guarda: while count < exp)
#   L4: result <- result * base            (corpo do while)
#   L5: count  <- count + 1               (corpo do while)
#   L6: GOTO L3                            (retorno implicito ao teste do while)
#   L7: HALT                               (fim do while / return)
#
# A condicao do while Python e `count < exp`, cuja negacao e `count >= exp`,
# correspondendo exatamente ao desvio de L3. As instrucoes normalizadas sao
# identicas as de P1 — portanto P1 e P_iter sao FORTEMENTE EQUIVALENTES.
#
P_iter = MaquinaDeTracas({
    1: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: 1},
    2: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: 0},
    3: {'tipo': 'IF_GOTO', 'cond': lambda s: s['count'] >= s['exp'], 'destino': 7},
    4: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: s['result'] * s['base']},
    5: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['count'] + 1},
    6: {'tipo': 'GOTO',    'destino': 3},
    7: {'tipo': 'HALT'},
}, nome="P_iter (iterativo.py normalizado para L1-L7)")


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
    2: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['exp']},
    3: {'tipo': 'IF_GOTO', 'cond': lambda s: s['count'] <= 0, 'destino': 7},
    4: {'tipo': 'ATRIB',   'var': 'result', 'expr': lambda s: s['result'] * s['base']},
    5: {'tipo': 'ATRIB',   'var': 'count',  'expr': lambda s: s['count'] - 1},
    6: {'tipo': 'GOTO',    'destino': 3},
    7: {'tipo': 'HALT'},
}, nome="P3 (contagem decrescente: count exp -> 0)")


# ============================================================
# Comparacao de cadeias: equivalencia forte
# ============================================================

def comparar(cadeia_a: list, cadeia_b: list,
             nome_a: str, nome_b: str, entrada: dict):
    """
    Compara duas cadeias de tracas.
    Dois programas sao FORTEMENTE EQUIVALENTES se e somente se,
    para toda entrada, suas cadeias de tracas sao identicas
    configuracao a configuracao.
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
        print(f"\n  ✓  FORTEMENTE EQUIVALENTES")
        print(f"     Ambas as cadeias possuem {len(cadeia_a)} configuracoes identicas.")
        print(f"     Para toda entrada, {nome_a} ≡ {nome_b} (mesma cadeia, mesmo resultado).")
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

    SEP = "\n" + "#" * 62

    # ----- Entrada de teste principal -----
    entrada = {'base': 2, 'exp': 3}
    print(SEP)
    print(f"#  MAQUINA DE TRACAS — Potenciacao Inteira")
    print(f"#  Entrada: base={entrada['base']}, exp={entrada['exp']}")
    print(f"#  Esperado: {entrada['base']}^{entrada['exp']} = {entrada['base']**entrada['exp']}")
    print(SEP)

    # Executa os tres programas
    cadeia_P1    = P1.executar(entrada)
    cadeia_Piter = P_iter.executar(entrada)
    cadeia_P3    = P3.executar(entrada)

    # ---- Tabelas verticais de P1 e P3 ----
    print(SEP)
    print("#  CADEIAS DE TRACAS — formato tabela")
    print(SEP)
    P1.imprimir_cadeia(cadeia_P1, entrada)
    P3.imprimir_cadeia(cadeia_P3, entrada)

    # ---- Formato de fita de P1 e P3 ----
    print(SEP)
    print("#  CADEIAS DE TRACAS — formato de fita (canonico)")
    print(SEP)
    P1.imprimir_fita(cadeia_P1, entrada)
    P3.imprimir_fita(cadeia_P3, entrada)

    # ---- Caso 1: EQUIVALENCIA FORTE (P1 vs P_iter) ----
    print(SEP)
    print("#  CASO 1: Equivalencia forte  —  P1 vs P_iter")
    print("#  P_iter e a forma normalizada L1-L7 do iterativo.py")
    print(SEP)
    comparar(cadeia_P1, cadeia_Piter, "P1", "P_iter", entrada)

    # ---- Caso 2: NAO-EQUIVALENCIA FORTE (P1 vs P3) ----
    print(SEP)
    print("#  CASO 2: Nao-equivalencia forte  —  P1 vs P3")
    print(SEP)
    comparar(cadeia_P1, cadeia_P3, "P1", "P3", entrada)

    # ---- Teste adicional: exp=0 (caso base) ----
    print(SEP)
    print("#  TESTE EXTRA: exp = 0  (caso base)")
    print(SEP)
    entrada0 = {'base': 5, 'exp': 0}
    c1 = P1.executar(entrada0)
    c3 = P3.executar(entrada0)
    P1.imprimir_fita(c1, entrada0)
    P3.imprimir_fita(c3, entrada0)
    comparar(c1, c3, "P1", "P3", entrada0)
