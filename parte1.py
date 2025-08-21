import pygame
import random
import math

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

pontoInicial, pontoFinal = (margem, margem), (largura - margem, altura - margem)

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
                        for o in obstaculos:
                            x, y, r = o["pos"][0], o["pos"][1], o["raio"]
                            pontos = [
                                (x, y - r),  
                                (x, y + r),  
                                (x - r, y),  
                                (x + r, y)   
                            ]
                            pontosObstaculos.append(pontos)
                        
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
        
    textoQuant = fonte.render(f"Obstáculos: {len(obstaculos)} | Raio atual: {raio}", True, (255,255,255))
    janela.blit(textoQuant, (largura - 350,10))
        
    pygame.display.update()
    
pygame.quit()
