/*
 * ============================================================
 *  Programa MONOLITICO - Potenciacao Inteira (base^exp)
 *  Disciplina: Teoria da Computabilidade
 *  Estilo: Monolitico (fluxo de controle via goto/rotulos)
 * ============================================================
 *
 *  Instrucoes rotuladas (forma normalizada para Maquina de Tracas):
 *   L1: result <- 1
 *   L2: count  <- 0
 *   L3: SE count >= exp ENTAO GOTO L7
 *   L4: result <- result * base
 *   L5: count  <- count + 1
 *   L6: GOTO L3
 *   L7: HALT
 *
 *  Compilar: gcc monolitico.c -o monolitico
 *  Executar: ./monolitico
 * ============================================================
 */

#include <stdio.h>

int main(void) {
    int base, exp, result, count;

    printf("=== Potenciacao Monolitica ===\n");
    printf("Base   : ");
    scanf("%d", &base);
    printf("Expoente: ");
    scanf("%d", &exp);

    /* Validacao simples */
    if (exp < 0) {
        printf("Erro: expoente negativo nao suportado.\n");
        return 1;
    }

    /* --------------------------------------------------
     * Programa monolitico normalizado com GOTO
     * Cada rotulo corresponde a uma instrucao atomica
     * -------------------------------------------------- */

L1: result = 1;
L2: count  = 0;

L3: if (count >= exp) goto L7;

L4: result = result * base;
L5: count  = count + 1;
L6: goto L3;

L7:
    printf("\nResultado: %d^%d = %d\n", base, exp, result);
    printf("\nPressione Enter para sair...");
    getchar(); getchar();
    return 0;
}
