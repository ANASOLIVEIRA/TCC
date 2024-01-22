# TCC

# PROJETO DESENVOLVIMENTO DE PROTÓTIPO DE SISTEMA DE INSPEÇÃO ÓPTICA DE PLACAS DE CIRCUITO IMPRESSO PARA LINHAS DE PRODUÇÃO COM INSERÇÃO MANUAL DE COMPONENTES
## RESUMO:

O presente trabalho apresenta o desenvolvimento de um protótipo de sistema de inspeção óptica de placas de circuito impresso para linhas de produção com inserção manual de componentes. Inicialmente será apresentada a fundamentação teórica para o desenvolvimento deste trabalho: estudo sobre o processo de fabricação de placas de circuito impresso, métodos de inspeção para placas de circuito impresso, processamento digital de imagem, linguagem de programação Python e bibliotecas, e, por fim, o estudo a respeito da Raspberry Pi. Em seguida é descrito os estágios de desenvolvimento do projeto. No primeiro estágio é desenvolvido o sistema de iluminação e preparação do enclausuramento como ambiente para a realização da captura de imagens das placas de circuito impresso. Após esse estágio é feito ajuste de câmera e iluminação, assim como o algoritmo utilizando processamento digital de imagem. No último estágio é feito o cadastro das placas de circuito impresso definindo as regiões de interesse na mesma. Por fim, por meio da interface homem-máquina é possível analisar a presença dos componentes inseridos manualmente.

## Componentes utilizados
1 mini computador Raspberry Pi 4 Modelo B
1 protoboard 830 furos MB-102
1 mini fonte chaveada de 5VDC
1 mini fonte chaveada de 12VDC
2 módulos relé 5V de 1 canal
10 leds branco de alto brilho 3V
4 resistores de 2kΩ de 1/4W
Fios para conexão
Para o enclausuramento e bases para posicionar as PCBs e câmera, foram necessários os seguintes itens:
1 caixa de papelão de material não reflexivo
2 berços para placas 1 e 2 de papelão de material não reflexivo
1 câmera Logitech C922 Pro HD Stream 1080p Webcam
Para a realização da implementação foram utilizadas duas PCB’s para a cadastro no sistema e validação de funcionamento do mesmo. Na Figura 21, temos a placa 1, que é uma placa de amplificador de som.

## Formulação do Problema
O processo de fabricação industrial de placa de circuito impresso é realizado, em sua
grande parte, por meio do uso da tecnologia de montagem em superfície, entretanto, devido a
robustez exigida por determinados componentes eletrônicos, principalmente no setor de
eletrônica de potência, faz-se necessária utilização de componentes montados utilizando a
tecnologia de montagem através de furos por inserção manual pelos operadores (HOOF, 2018).
Devido a aplicação de mão-de-obra humana para a inserção de componentes, tem-se a
necessidade da inspeção visual da placa de circuito impresso.
Com isso, defeitos ou erros de montagem podem passar despercebidos devido a
característica de repetitividade desta ação, sendo este efeito conhecido como fadiga mental, ou
cognitiva, que ocorre quando os olhos e o cérebro se tornam menos sensíveis e receptivos a
estímulos visual após um longo tempo de exposição a processos repetitivos ou monótonos, o
que resulta em uma diminuição da capacidade de detectar e classificar defeitos de forma precisa
e consistente (PINHEIRO, 2007).

## Hipotése
É possível desenvolver um protótipo sistema de inspeção óptica automatizada, capaz de
realizar inspeções ópticas de componentes eletrônicos inseridos manualmente na placa de
circuito impresso, através da tecnologia de montagem através do furo, durante o processo de
fabricação. O sistema será composto pelo computador de baixo custo Raspberry Pi 4 model B,
equipado com uma câmera responsável por realizar a captura de imagem da placa de circuito
impresso, com intuito de validar de forma automatizada a presença e polaridade, quando
aplicável, dos componentes inseridos manualmente.

## Objetivo
Desenvolver um protótipo sistema de inspeção óptica em ambiente controlado. Utilizando o minicomputador Rasperry Pi, que receberá como entrada as imagens
captadas via câmera e realizará o processamento digital de imagem. O resultado será
apresentado em uma interface para interação com o usuário.

## Justificativa
O presente projeto de pesquisa se justifica por disponibilizar uma alternativa à inspeção
visual manual realizada em linhas de produção com inserção manual de componentes. Uma
falha no processo de fabricação pode ocasionar em um mal funcionamento do produto final ou
o descarte de componentes, gerando retrabalho e aumento de custos para o processo de
fabricação. Em um processo de fabricação quanto mais cedo um defeito for detectado na linha
de montagem, menor será o custo para o seu reparo, esses que podem chegar a dez vezes o
capital investido usando a fórmula “Regra 10X” (BURR, 1997), gerando uma utilização mais
eficaz de recursos e aumento na eficiência do processo de inspeção comparado com a inspeção
visual manual.
O desenvolvimento de um protótipo de sistema de inspeção óptica de placas de circuito
impresso para linhas de produção com inserção manual de componentes, envolve a utilização
de vários conceitos estudados nas disciplinas de Engenharia Eletrônica, tais como:
Fundamentos de Eletrônica, Análise de Circuitos Elétricos, Técnicas de Programação em
Engenharia Eletrônica, Microprocessadores e Microcontroladores, Sensores e Instrumentação
Eletrônica, Processamento Digital de Sinais, Sistemas Eletrônicos de Imagens e Sistemas
Operacionais Embarcados.
