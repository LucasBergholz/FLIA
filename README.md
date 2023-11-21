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
