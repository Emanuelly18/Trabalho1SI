import pygame
import random
import math
from collections import deque

pygame.init()

# tamanho inicial da janela
largura = 800
altura = 400
janela = pygame.display.set_mode((largura, altura))
margem = 30
fonte = pygame.font.SysFont(None, 25)

# titulo da janela
pygame.display.set_caption("Robozinho")

# parametros dos obstaculos
obstaculos = []
corObstaculo = (139,0,139)
quantObstaculos = 0
distanciaMinima = 0
tentativasMAX = 20

# limites máximos de tela e raio
larguraMax = 1500
alturaMax = 750
raio = 30   

# input para a quantidade de obstaculos
inputA = True
inputD = ""

# vertices dos obstaculos
pontosObstaculos = [] 
arestas = []

pontoInicial, pontoFinal = (margem, margem), (largura - margem, altura - margem)

def bfsComVolta(grafo, inicio, fim, parOposto):
    
    fila = deque([inicio])
    pai = {inicio: None}

    while fila:
        atual = fila.popleft()
        if atual == fim:
            break

        
        if atual in parOposto and pai[atual] != parOposto[atual]:
            op = parOposto[atual]
            if op not in pai:
                pai[op] = atual
                fila.append(op)
           
            continue

        
        vizinhos = list(grafo.get(atual, []))
        
        if pai[atual] is not None and pai[atual] in vizinhos:
            vizinhos.remove(pai[atual])
        random.shuffle(vizinhos)

        for v in vizinhos:
            if v not in pai:
                pai[v] = atual
                fila.append(v)

    if fim not in pai:
        return []

    #reconstrói o caminho
    caminho = []
    n = fim
    while n is not None:
        caminho.append(n)
        n = pai[n]
    caminho.reverse()
    return caminho

def construirGrafo(arestas, parOposto):
   
    grafo = {}
    def add(u, v):
        grafo.setdefault(u, []).append(v)
        grafo.setdefault(v, []).append(u)

    for v1, v2 in arestas:
        add(v1, v2)

    
    vistos = set()
    for v, op in parOposto.items():
        if (v, op) in vistos or (op, v) in vistos:
            continue
        add(v, op)
        vistos.add((v, op))
    return grafo


def passoInterno(u, v, parOposto, obstaculos):
    if parOposto.get(u) == v or parOposto.get(v) == u:
        return True
    
    for o in obstaculos:
        if intersectaCirculo(u, v, o["pos"], o["raio"]):
            return True
    return False

def intersectaCirculo(p1, p2, centro, raio):
    (x1, y1), (x2, y2) = p1, p2
    (cx, cy) = centro

    dx, dy = x2 - x1, y2 - y1 #vetor da direcao da reta
    fx, fy = x1 - cx, y1 - cy #vetor do centro até o ponto inicial

    a = dx*dx + dy*dy # at^2 + bt + c = 0
    b = 2 * (fx*dx + fy*dy)
    c = fx*fx + fy*fy - raio*raio

    discriminante = b*b - 4*a*c
    if discriminante < 0:
        return False 

    discriminante = math.sqrt(discriminante)

    t1 = (-b - discriminante) / (2*a)
    t2 = (-b + discriminante) / (2*a)

    
    if (0 < t1 < 1) or (0 < t2 < 1):
        return True

    return False





def ehVisivel(p1, p2, obstaculos):
    for o in obstaculos:
        if intersectaCirculo(p1, p2, o["pos"], o["raio"]):
            return False
    return True


def criarArestas(pontosObstaculos, obstaculos):
    vertices = [pontoInicial, pontoFinal]
    for pontos in pontosObstaculos:
        vertices.extend(pontos)

    arestasLocal = []

    #percorre todos os pares de vértices
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            v1 = vertices[i]
            v2 = vertices[j]

            # descarta se forem do mesmo obstáculo
            for pontos in pontosObstaculos:
                if v1 in pontos and v2 in pontos:
                    #p1 e p2 pertencem ao mesmo círculo
                    break
            else:
                #só testa visibilidade se não for do mesmo obstáculo
                if ehVisivel(v1, v2, obstaculos):
                    arestasLocal.append((v1, v2))

    return arestasLocal



def atualizarPontos():
    global pontoInicial, pontoFinal
    pontoInicial = (margem, margem)
    pontoFinal = (largura - margem, altura - margem)

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def gerarObstaculos(quantidade, raio):
    global largura, altura, janela
    while raio >= 2:
        novos = []
        
        while len(novos) < quantidade:
            tentativas = 0
            inserido = False
            
            while tentativas < tentativasMAX and not inserido:
                x = random.randint(raio, largura - raio)
                y = random.randint(raio, altura - raio)
                pos = (x, y)
                
                valido = True
                for o in novos:
                    if distancia(pos, o["pos"]) < (2*raio + distanciaMinima):
                        valido = False
                        break
                    
                seguro = raio + 30  
                if distancia(pos, pontoInicial) < seguro or distancia(pos, pontoFinal) < seguro:
                    valido = False
                    
                if valido:
                    novos.append({"pos": pos, "raio": raio, "cor": corObstaculo})
                    inserido = True
                else:
                    tentativas += 1
            
            # se não conseguiu inserir
            if not inserido:
                # aumenta a tela
                if largura < larguraMax and altura < alturaMax:
                    largura += 100
                    altura += 50
                    janela = pygame.display.set_mode((largura, altura), pygame.RESIZABLE)
                    atualizarPontos()
                # chegou ao limite de tela
                else:
                    raio -= 1
                    if raio < 2:  
                        return novos, raio
                    novos = []
                    break  

        if len(novos) == quantidade:
            return novos, raio
    return novos, raio

start = True
caminho = []

while start:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            start = False

        elif inputA:  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if inputD.isdigit():
                        quantObstaculos = int(inputD)
                        obstaculos, raio = gerarObstaculos(quantObstaculos, raio)
                        
                        pontosObstaculos = [] 
                        parOposto = {}
                        
                        for o in obstaculos:
                            x, y, r = o["pos"][0], o["pos"][1], o["raio"]
                            topo    = (x, y - r)
                            base    = (x, y + r)
                            esquerda= (x - r, y)
                            direita = (x + r, y)

                            pontos = [topo, base, esquerda, direita]
                            pontosObstaculos.append(pontos)

                            #mapeia pares opostos
                            parOposto[topo] = base
                            parOposto[base] = topo
                            parOposto[esquerda] = direita
                            parOposto[direita]  = esquerda
                            
                        #construir arestas
                        arestas = criarArestas(pontosObstaculos, obstaculos)
                        print("Arestas visíveis:", len(arestas))
                        
                        #grafo para busca 
                        grafo = construirGrafo(arestas, parOposto)

                        caminho = bfsComVolta(grafo, pontoInicial, pontoFinal, parOposto)
                        print("Caminho encontrado:", caminho)
                        
                        inputA = False
                elif evento.key == pygame.K_BACKSPACE:
                    inputD = inputD[:-1]
                else:
                    if evento.unicode.isdigit():
                        inputD += evento.unicode
    
    # cor da janela
    janela.fill((0,0,0))
    
    
    if inputA:
        instrucao = fonte.render("Digite a quantidade de obstáculos e pressione ENTER:", True, (255,255,255))
        janela.blit(instrucao, (50, altura//2 - 50))
        entrada = fonte.render(inputD, True, (0,255,0))
        janela.blit(entrada, (largura//2 - 20, altura//2))
        
    else:
        # ponto de inicio e ponto final
        pygame.draw.circle(janela, (0,0,255), pontoInicial, 8)
        textoI = fonte.render("I", True, (255,255,255))
        rectI = textoI.get_rect(center=(pontoInicial[0], pontoInicial[1] - 20))
        janela.blit(textoI, rectI)

        pygame.draw.circle(janela, (0,0,255), pontoFinal, 8)
        textoF = fonte.render("F", True, (255,255,255))
        rectF = textoF.get_rect(center=(pontoFinal[0], pontoFinal[1] - 20))
        janela.blit(textoF, rectF)
    
    # desenha obstaculos
    for o in obstaculos:
        pygame.draw.circle(janela, o["cor"], o["pos"], o["raio"])
        
    # desenha vertices
    for pontos in pontosObstaculos:
        for p in pontos:
            pygame.draw.circle(janela, (139,0,0), p, 4)
            
    # desenha arestas
    for a in arestas:
        pygame.draw.line(janela, (0,255,0), a[0], a[1], 1)
        
    # desenha caminho 
    if caminho:
        for i in range(len(caminho) - 1):
            u, v = caminho[i], caminho[i+1]
            if passoInterno(u, v, parOposto, obstaculos):
                continue  #nao desenha
            pygame.draw.line(janela, (0,0,255), u, v, 3)
        
    textoQuant = fonte.render(f"Obstáculos: {len(obstaculos)} | Raio atual: {raio}", True, (255,255,255))
    janela.blit(textoQuant, (largura - 350,10))
        
    pygame.display.update()
    
pygame.quit()
