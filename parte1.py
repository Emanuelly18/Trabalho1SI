import pygame
import random
import math

pygame.init()

# tamanho inicial da janela
largura = 800
altura = 600
janela = pygame.display.set_mode((largura, altura))
margem = 40
fonte = pygame.font.SysFont(None, 30)

# titulo da janela
pygame.display.set_caption("Robozinho")

# parametros dos obstaculos
obstaculos = []
corObstaculo = (139,0,139)
quantObstaculos = 0
distanciaMinima = 30
tentativasMAX = 20

# limites máximos de tela e raio
larguraMax = 1600
alturaMax = 1200
raio = 30   # raio fixo


# input para a quantidade de obstaculos
inputA = True
inputD = ""

def distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def gerarObstaculos(quantidade, raio):
    global largura, altura, janela
    novos = []
    
    while len(novos) < quantidade:
        tentativas = 0
        inserido = False
        
        while tentativas < tentativasMAX and not inserido:
            x = random.randint(margem + raio, largura - margem - raio)
            y = random.randint(margem + raio, altura - margem - raio)
            pos = (x, y)
            
            valido = True
            for o in novos:
                if distancia(pos, o["pos"]) < (2*raio + distanciaMinima):
                    valido = False
                    break
            if valido:
                novos.append({"pos": pos, "raio": raio, "cor": corObstaculo})
                inserido = True
            else:
                tentativas += 1
        
        # se não conseguiu inserir
        if not inserido:
            if largura < larguraMax and altura < alturaMax:
                largura += 100
                altura += 100
                janela = pygame.display.set_mode((largura, altura))
            else:
                break  # não tem mais o que fazer

    return novos, raio

start = True
while start:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            start = False

        elif inputA:  # pede apenas a quantidade
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if inputD.isdigit():
                        quantObstaculos = int(inputD)
                        obstaculos, raio = gerarObstaculos(quantObstaculos, raio)
                        inputA = False
                elif evento.key == pygame.K_BACKSPACE:
                    inputD = inputD[:-1]
                else:
                    if evento.unicode.isdigit():
                        inputD += evento.unicode
    
    # cor da janela
    janela.fill((0,0,0))
    # add borda
    pygame.draw.rect(janela, (0,255,127), (0,0,largura,altura),5)
    
    if inputA:
        instrucao = fonte.render("Digite a quantidade de obstáculos e pressione ENTER:", True, (255,255,255))
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
        
        # gera obstaculos
        for o in obstaculos:
            pygame.draw.circle(janela, o["cor"], o["pos"], o["raio"])
            
        textoQuant = fonte.render(f"Obstáculos: {len(obstaculos)} | Raio atual: {raio}", True, (255,255,255))
        janela.blit(textoQuant, (largura - 350,10))
        
    pygame.display.update()
    
pygame.quit()
