"""import matplotlib.pyplot as plt
import os

pi = (1, 1)
pf = (50, 50)

# Criando o gráfico:
plt.figure(figsize=(4, 4))
plt.plot(*pi, 'bo', label="Ponto inicial") 
plt.plot(*pf, 'mo', label="Ponto final")   

plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.legend()
plt.title("Ponto inicial e FINAL ")
print("OLA")


# Salvando o gráfico
grafico = "grafico.png"
plt.savefig(grafico)
print("Gráfico criado com sucesso!")


quantObst = int(input("Informe a quatidade de obstáculos: "))
tamRaio = float(input("Informe o tamanho do raio dos obstáculos: ")) 

os.system(f"xdg-open {grafico}")"""

import pygame
import random
import math

pygame.init()

# definir o tamanho da janela, margem e fonte
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
margem = 40
fonte = pygame.font.SysFont(None, 30)

#titulo da janela
pygame.display.set_caption("Robozinho")

#paramentos dos obstaculos
obstaculos = []
raio = 40
corObstaculo = (139,0,139)
quantObstaculos = 0
distanciaMinima = 50
tentativasMAX = 10

distanciaCentroMinima = 2*raio + distanciaMinima

#input para a quantidade de obstaculos
inputA = True
inputD = ""

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def gerarObstaculos(quantidade):
    novos = []
    
    for _ in range(quantidade):
        tentativas = 0
        inserido = False
        
        while tentativas < tentativasMAX and not inserido:
            x = random.randint(margem + raio, largura - margem - raio)
            y = random.randint(margem + raio, altura - margem - raio)
            pos = (x, y)
            
            #verificação
            
            valido = True
            for o in novos:
                if distancia(pos, o["pos"]) < distanciaCentroMinima:
                    valido = False
                    break
            if valido:
                novos.append({"pos": pos, "raio": raio, "cor": corObstaculo})
                inserido = True
            else:
                tentativas += 1
    return novos

start = True
while start:
    for evento in pygame.event.get():
        # para fechar a janela
        if evento.type == pygame.QUIT:
            start = False
            
        #captura o teclado
        if inputA:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: #o enter
                    if inputD.isdigit():
                        quantObstaculos = int(inputD)
                        obstaculos = gerarObstaculos(quantObstaculos)
                        inputA = False
                elif evento.key == pygame.K_BACKSPACE:
                    inputD = inputD[:-1]
                else:
                    if evento.unicode.isdigit():
                        inputD += evento.unicode
    
    #cor da janela
    janela.fill((0,0,0))
    #add borda
    pygame.draw.rect(janela, (0,255,127), (0,0,largura,altura),5)
    
    if inputA:
        instrucao = fonte.render("Digite a quantidade de círculos e pressione ENTER:", True, (255,255,255))
        janela.blit(instrucao, (50, altura//2 - 50))
        
        entrada = fonte.render(inputD, True, (0,255,0))
        janela.blit(entrada, (largura//2 - 20, altura//2))
    else:
        # ponto de inicio e ponto final
        pontoInicial = (margem, margem) 
        pygame.draw.circle(janela, (0,0,255), pontoInicial, 8)

        textoI = fonte.render("I", True, (255,255,255))
        rectI = textoI.get_rect(center=(pontoInicial[0], pontoInicial[1] - 20))
        janela.blit(textoI, rectI)
        
        pontoFinal = (largura - margem, altura - margem)
        pygame.draw.circle(janela, (255,0,0), pontoFinal, 8)

        textoF = fonte.render("F", True, (255,255,255))
        rectF = textoF.get_rect(center=(pontoFinal[0], pontoFinal[1] - 20))
        janela.blit(textoF, rectF)
        
        #gera obstaculos
        for o in obstaculos:
            pygame.draw.circle(janela, o["cor"], o["pos"], o["raio"])
            
        textoQuant = fonte.render(f"Obstáculos: {len(obstaculos)}", True, (255,255,255))
        janela.blit(textoQuant, (largura - 200,10))
        
    pygame.display.update()
    
pygame.quit()