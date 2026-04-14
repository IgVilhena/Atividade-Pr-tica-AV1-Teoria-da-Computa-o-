"""
============================================================
 Programa ITERATIVO - Potenciacao Inteira (base^exp)
 Disciplina: Teoria da Computabilidade
 Estilo: Iterativo (estrutura de repeticao explicita: while)
============================================================

 Executar: python3 iterativo.py

============================================================
"""


def potencia_iterativa(base: int, exp: int) -> int:
    """
    Calcula base^exp de forma iterativa.

    Entradas : base (int), exp (int >= 0)
    Saida    : base elevado a exp (int)
    Condicao : exp >= 0

    Estrutura de repeticao: while (loop explicito)
    Variavel de controle: count (incrementada a cada iteracao)
    """
    result = 1          # acumulador inicializado em 1 (elemento neutro da multiplicacao)
    count  = 0          # contador de iteracoes

    while count < exp:              # teste de parada: count atingiu exp?
        result = result * base      # operacao central: acumula multiplicacao
        count  = count + 1          # avanca o contador

    return result                   # retorna o resultado apos exp multiplicacoes


# ---------------------------------------------------------
# Execucao principal com exemplos de entrada e saida
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== Potenciacao Iterativa ===\n")

    casos = [
        (2, 0),   # caso base: qualquer numero elevado a 0 = 1
        (2, 1),   # expoente 1: resultado = base
        (2, 3),   # caso tipico: 2^3 = 8
        (3, 4),   # 3^4 = 81
        (5, 3),   # 5^3 = 125
        (10, 2),  # 10^2 = 100
    ]

    for base, exp in casos:
        resultado = potencia_iterativa(base, exp)
        print(f"  potencia_iterativa({base:2d}, {exp}) = {resultado}")

    print("\n--- Entrada interativa ---")
    base = int(input("Base   : "))
    exp  = int(input("Expoente: "))
    if exp < 0:
        print("Erro: expoente negativo nao suportado.")
    else:
        print(f"\nResultado: {base}^{exp} = {potencia_iterativa(base, exp)}")
