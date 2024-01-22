# TCC

# PROJETO DESENVOLVIMENTO DE PROTÓTIPO DE SISTEMA DE INSPEÇÃO ÓPTICA DE PLACAS DE CIRCUITO IMPRESSO PARA LINHAS DE PRODUÇÃO COM INSERÇÃO MANUAL DE COMPONENTES
## RESUMO:
**

O presente trabalho teve como objetivo o desenvolvimento de um protótipo de sistema de inspeção óptica de placas de circuito impresso para linhas de produção com inserção manual de componentes. Inicialmente será apresentada a fundamentação teórica para o desenvolvimento deste trabalho: estudo sobre o processo de fabricação de placas de circuito impresso, métodos de inspeção para placas de circuito impresso, processamento digital de imagem, linguagem de programação Python e bibliotecas, e, por fim, o estudo a respeito da Raspberry Pi. Em seguida é descrito os estágios de desenvolvimento do projeto. No primeiro estágio é desenvolvido o sistema de iluminação e preparação do enclausuramento como ambiente para a realização da captura de imagens das placas de circuito impresso. Após esse estágio é feito ajuste de câmera e iluminação, assim como o algoritmo utilizando processamento digital de imagem. No último estágio é feito o cadastro das placas de circuito impresso definindo as regiões de interesse na mesma. Por fim, por meio da interface homem-máquina é possível analisar a presença dos componentes inseridos manualmente.
**

## Componentes utilizados
1. Placa Arduíno Mega
2. Display LDC 16x2
3. Shield L293D - Ponte H
4. Motor DC 12V - C9045 60001 RD548311
5. Fonte 12VDC (Motor)
6. Módulo I2C
7. Sensor de Efeito Hall - Módulo 3144
8. Led Azul
9. Led Verde
10. Led Vermelho
11. Botão Push 1 - Sentido Horário
12. Botão Push 2 - Sentido Anti-Horário
13. Botão Push 3 - Velocidade - 3 velocidades (opcional)
14. Botão Push 4 - Incremento (Calibração)
15. Botão Push 5 - Decremento (Calibração)
16. Interruptor ON/OFF
17. Sensor Ultrassônico HC-SR04
18. Buzzer
19. Bateria
20. Resistores

## Objetivo
- Leitura da rotação por minuto (RPM) de um motor 12v utilizando um sensor de efeito hall
- Sensor ultrassônico HC-SR04 para segurança, quando abre a caixa do projeto, tendo assim acesso ao motor, quando abre a tampa o sensor para o motor

## Funcionamento do programa descrito

Ao pressionar o botão 1, o buzzer emite um som e o led vermelho é acionado, depois de 1 segundo buzzer e led vermelho apagam, led verde acende e motor começa a rotacionar sentido horário com uma rotação baixa. Ao pressionar o botão de velocidade a rotação irá aumentar para uma rotação média, e ao pressionar o botão novamente a rotação muda para a rotação máxima.

Ao pressionar o botão 2, o buzzer emite um som e o led vermelho é acionado, depois de 1 segundo, buzzer e led vermelho apagam, led azul acende e motor começa a rotacionar sentido anti-horário com uma rotação baixa. Ao pressionar o botão de velocidade a rotação irá aumentar para uma rotação média, e ao pressionar o botão novamente a rotação muda para a rotação máxima.

Ao eixo do motor estará fixado um imã, este imã irá ficar rotacionando, e a cada ciclo completo o imã fica posicionado a frente do sensor de efeito Hall. O sensor detecta o ciclo realizado pelo imã e envia a leitura do RPM realizado. 

![image](https://user-images.githubusercontent.com/61547619/124055793-8b75d380-d9f2-11eb-83db-faa4a7390e9e.png)

### Segurança
O motor fica isolado em uma caixa, e considerando como um item que pode vir a causar acidentes foi implementado um sistema de segurança, quando a tampa da caixa é aberta o sensor ultrassônico realiza uma leitura fora do parâmetro, emitindo uma mensagem de alerta no display e para o motor.

### 1. Calibração
Para realizar a calibração foi utilizado a lógica de incrementar ou decrementar o valor lido para realar a compensação de leitura do sensor.

## Detalhamento técnico
### 1. Sensor Efeito Hall
O sensor de efeito Hall é um sensor de campo magnético. Podenso ser utilizado para detectar a rotação de um objeto, posicionamento do objeto ou detectar movimento.
O efeito hall é resultado pela força de Lorentz no movimento de elétrons a um campo magnético, onde se tem uma tensão de hall proporcional ao campo magnético aplicado. 

### 1.1. Teoria de Efeito Hall

O fluxo de corrente em um material sem o efeito de uma campo magnético, tem suas linhas equipotenciais que se cruzam formando um ângulo de 90°.

Fb = q*V*B*senO

Onde 

- Fb: força magnética [N]
- q: módulo carga elétrica [C]
- v: velocidade da carga [m/s]
- B: campo magnético [T]
- senO: ângulo entre direção da velocidade e a direção do campo magnético

Com um fluxo de corrente em um objeto sujeito a um campo magnético formando 90°, o ângulo do fluxo da corrente é alterado (sofrendo o efeito do campo magnético), que se é conhecido como ângulo Hall. Sendo assim as linhas equipotenciais se inclinam, causando uma tensão de Hall ao longo do objeto.
### 1.1.1 Vantagens
- Alta sensibilidade
- Erros despreziveis de linearidade
- Erros desprezíveis em relação a vibração
- Repitibilidade
- Estabilidade
