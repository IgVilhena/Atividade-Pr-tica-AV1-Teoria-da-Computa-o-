"""
============================================================
 Programa RECURSIVO - Potenciacao Inteira (base^exp)
 Disciplina: Teoria da Computabilidade
 Estilo: Recursivo (chamadas recursivas + condicao-base)
============================================================

 Executar: python3 recursivo.py

============================================================
"""


def potencia_recursiva(base: int, exp: int) -> int:
    """
    Calcula base^exp de forma recursiva.

    Entradas : base (int), exp (int >= 0)
    Saida    : base elevado a exp (int)

    Condicao-base  : exp == 0  -->  retorna 1
                     (qualquer numero elevado a 0 eh 1)

    Chamada recursiva: base * potencia_recursiva(base, exp - 1)
                       (reduz o problema: base^n = base * base^(n-1))

    Propriedade matematica explorada:
        base^0       = 1
        base^exp     = base * base^(exp-1)
    """

    # ---- CONDICAO-BASE ----
    if exp == 0:
        return 1                                         # caso base: encerra a recursao

    # ---- CHAMADA RECURSIVA ----
    return base * potencia_recursiva(base, exp - 1)     # reducao do subproblema


# ---------------------------------------------------------
# Versao com rastreamento de chamadas (verbose)
# ---------------------------------------------------------
def potencia_recursiva_verbose(base: int, exp: int, nivel: int = 0) -> int:
    """Mesma funcao com impressao da pilha de chamadas."""
    indent = "  " * nivel
    print(f"{indent}potencia_recursiva({base}, {exp})")

    if exp == 0:
        print(f"{indent}=> caso base: retorna 1")
        return 1

    sub = potencia_recursiva_verbose(base, exp - 1, nivel + 1)
    resultado = base * sub
    print(f"{indent}=> {base} * {sub} = {resultado}")
    return resultado


# ---------------------------------------------------------
# Execucao principal com exemplos de entrada e saida
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== Potenciacao Recursiva ===\n")

    casos = [
        (2, 0),
        (2, 1),
        (2, 3),
        (3, 4),
        (5, 3),
        (10, 2),
    ]

    for base, exp in casos:
        resultado = potencia_recursiva(base, exp)
        print(f"  potencia_recursiva({base:2d}, {exp}) = {resultado}")

    print("\n--- Rastreamento de chamadas para 2^3 ---\n")
    potencia_recursiva_verbose(2, 3)

    print("\n--- Entrada interativa ---")
    base = int(input("\nBase   : "))
    exp  = int(input("Expoente: "))
    if exp < 0:
        print("Erro: expoente negativo nao suportado.")
    else:
        print(f"\nResultado: {base}^{exp} = {potencia_recursiva(base, exp)}")
