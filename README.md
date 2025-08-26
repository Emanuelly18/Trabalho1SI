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

---

  <img width="1495" height="786" alt="image" src="https://github.com/user-attachments/assets/f78d116a-ecc7-4ed6-97b0-dbc34342ba59" />

## Parte 2 - Adição dos Vértices

- Para cada obstáculo gerado, são adicionados **4 vértices auxiliares**:
  - **Cima** (x, y - raio)  
  - **Baixo** (x, y + raio)  
  - **Esquerda** (x - raio, y)  
  - **Direita** (x + raio, y)  

- Esses vértices são desenhados como pontos vermelhos em torno de cada obstáculo.  
- Além disso, o programa gera uma lista com as coordenadas de todos os vértices, organizada por obstáculo.

---

  <img width="1000" height="535" alt="image" src="https://github.com/user-attachments/assets/9c62a6bb-87ea-4ac1-bbb5-e746dfac570b" />

## Parte 3 - Adição das Arestas

- Nesta etapa, são criadas **arestas entre os vértices visíveis** do ponto inicial **I** para o ponto final **F**:    
  - São considerados como vértices:  
    - O ponto inicial (**I**)  
    - O ponto final (**F**)  
    - Os 4 vértices auxiliares de cada obstáculo  

- Para cada par de vértices:  
  - Se não pertencem ao **mesmo obstáculo**  
  - E se o segmento de reta que os liga **não intercepta nenhum círculo (obstáculo)**  
  - Então uma **aresta é adicionada ao grafo**.  

- As arestas visíveis são desenhadas na tela em **verde**, conectando todos os vértices que podem se "enxergar" sem que um obstáculo esteja no caminho.

---

<img width="996" height="537" alt="image" src="https://github.com/user-attachments/assets/08fe9396-8dcc-45d2-a77a-985113977adf" />


## Requisitos

- **Python 3.x**
- **Pygame**

Para instalar o Pygame, execute:

```bash
pip install pygame

