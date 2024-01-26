# FLIA
Repositório destinado aos trabalhos desenvolvidos na disciplina de Fundamentos Lógicos de Inteligência Artificial.

## PDDL - Lightsout
O primeiro projeto prático da disciplina põe em prática os conhecimentos adquiridos na linguagem de PDDL (Planning Domain Definition Language), com o intuito de resolver o jogo [Lightsout](https://www.logicgamesonline.com/lightsout/) adaptado.

Foi desenvolvido um domínio e um parser que gera e resolve automaticamente problemas para este domínio, recebendo como entrada o mapa de jogo. Para receber um plano de resolução na saída, faz-se necessário possuir um planejador baixado em sua máquina e colocar sua rota dentro do parser.

O arquivo de domínio mapeia as células com os subtipos x_position e y_position e define por predicados onde estão células de vértice e de parede do mapa, para assim se dividir em 3 actions: invert_cell, invert_edge e invert_vertice.

- invert_cell: quando ocorre um clique em uma célula de meio de mapa, ou seja, 5 células terão suas luzes invertidas.
- invert_edge: quando ocorre um clique em uma célula de parede do mapa, ou seja, 4 células terão suas luzes invertidas.
- invert_vertice: quando ocorre um clique em uma célula de vértice do mapa, ou seja, 3 células terão suas luzes invertidas.
  
No arquivo de parser, são definidos os predicados iniciais de acordo com a entrada, que são os incrementos e decrementos dos X e Y, de forma que se mapeie qual linha leva qual linha e qual coluna leva para qual coluna. Após isso, são definidos as células ligadas e quais células possuem um botão nela. Quando uma célula possui um botão nela, ao ser clicada, a célula em si não é invertida, apenas suas adjacentes. Para inverter um botão, faz-se necessário clicar em uma célula vizinha a ele.

## HDDL - Sudoku
O segundo projeto prático da disciplina põe em prática os conhecimentos adquiridos na linguagem HDDL (Hierarquical Domain Definition Language) com o intuito de resolver o jogo [Sudoku](https://pt.wikipedia.org/wiki/Sudoku).

Foi desenvolvido apenas o código que resolve o sudoku, e o mesmo só funcionará quando compilado utilizando um planejador hierarquico, como o [Panda-PI](https://github.com/panda-planner-dev?tab=repositories).

Foram definidos 4 tipos principais para o problema, com o intuito de facilitar o mapeamento do mesmo, que são : "row", "col", "digit" e "box", que representam respectivamente a linha, coluna, o digito e o sub-grid ou caixa (lembrando que o sudoku é baseado em um mapa 9x9 em que é dividido em 9 sub-grids 3x3).

Uma característica interessante do domínio é a forte presença de constantes, visto que os números possíveis para colocar em cada célula são sempre de 1 a 9, ou como existem as mesmas 9 box/sub-grids, ou como sempre são 9 linhas e 9 colunas.

Alguns predicados essenciais são:
- digit-at: predicado que define qual número está em determinada célula;
- filled: predicado que define quando a célula está preenchida;
- digit-at-box: predicado que ajuda na checagem se um número já está presente em determinada box;
- inc-row e inc-col: definem quais rows e cols são adjacentes.

Lembrando que um código em HDDL, diferentemente do PDDL, não necessariamente possui um "goal" no arquivo problema. Com isso em mente, o objetivo do jogo em si é ter todas as células preenchidas, respeitando as regras de não ter o mesmo número na mesma linha, coluna ou box.
