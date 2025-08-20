# Busca por um Caminho Ótimo

Este projeto tem como objetivo encontrar o caminho ótimo entre dois pontos fixos, traçando arestas do **ponto inicial (I)** até o **ponto final (F)**, desviando de obstáculos.

## Parte 1 – Geração do Cenário

- Definir dois pontos fixos:
  - **I** → Ponto inicial  
  - **F** → Ponto final  

- Gerar obstáculos:
  - Os obstáculos são **circunferências de raio fixo**, distribuídas aleatoriamente.  
  - Não podem colidir entre si, nem com os pontos inicial e final.  

- Inserção de obstáculos:
  - O usuário informa a **quantidade de obstáculos** desejada.  
  - O programa tenta posicioná-los no cenário:  
    - Se não houver espaço, a **área da tela é aumentada** gradualmente até o limite máximo.  
    - Caso o limite seja atingido e ainda não seja possível posicionar todos, o programa **reduz o raio dos obstáculos (-1 a cada tentativa)** até conseguir inserir todos ou até que o raio se torne inviável.
   
      <img width="1495" height="786" alt="image" src="https://github.com/user-attachments/assets/f78d116a-ecc7-4ed6-97b0-dbc34342ba59" />


## Requisitos

- **Python 3.x**
- **Pygame**

Para instalar o Pygame, execute:

```bash
pip install pygame

