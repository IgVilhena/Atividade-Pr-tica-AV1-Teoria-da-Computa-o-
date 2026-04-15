# Trabalho AV1 — Teoria da Computabilidade

## Integrantes da equipe
- Andrey Lourival Andrade Garcia
- Filipe César Maciel Sucupira
- Everton Gustavo de Oliveira
- Igor Cecim Vilhena

## Linguagens utilizadas
- **C**: programa monolítico
- **Python 3**: programa iterativo, programa recursivo e Máquina de Traços

## Função implementada
A equipe implementou a **potenciação inteira**:

**f(base, exp) = base^exp**, com **exp >= 0**.

Entradas:
- `base`: número inteiro
- `exp`: inteiro não negativo

Saída:
- resultado de `base` elevado a `exp`

## Organização dos arquivos
- `monolitico.c` → implementação monolítica em C com uso explícito de `goto`
- `iterativo.py` → implementação iterativa em Python com `while`
- `recursivo.py` → implementação recursiva em Python
- `maquina_de_tracas.py` → implementação da Máquina de Traços e comparação de equivalência / não-equivalência
- `apresentacao.pdf` → apresentação utilizada em sala
- `README.md` → instruções e documentação mínima da entrega

## Instruções de compilação e execução

### 1) Programa monolítico (C)
Compilar:
```bash
gcc monolitico.c -o monolitico
```

Executar:
```bash
./monolitico
```

### 2) Programa iterativo (Python)
Executar:
```bash
python3 iterativo.py
```

### 3) Programa recursivo (Python)
Executar:
```bash
python3 recursivo.py
```

### 4) Máquina de Traços (Python)
Executar:
```bash
python3 maquina_de_tracas.py
```

## Observação sobre a análise formal
A Máquina de Traços foi utilizada para:
- demonstrar um **caso de equivalência** entre o programa monolítico normalizado e a versão iterativa normalizada;
- demonstrar um **caso de não-equivalência forte** por meio de uma variação com contagem decrescente, mostrando divergência nos estados intermediários.

## Uso de IA
Ferramenta utilizada:
- Claude

Finalidade de uso:
- apoio à revisão textual;
- organização do material;
- apoio na estruturação do README e do material explicativo;
- apoio à explicação conceitual sobre os estilos de programa e Máquina de Traços.

Trechos/ideias aproveitados:
- sugestões de redação;
- melhoria de organização textual;
- apoio na documentação da entrega.

Validação pela equipe:
- o conteúdo foi revisado, ajustado e validado pela equipe antes da entrega.
