import matplotlib.pyplot as plt
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


""" quantObst = int(input("Informe a quatidade de obstáculos: "))
tamRaio = float(input("Informe o tamanho do raio dos obstáculos: ")) """



os.system(f"xdg-open {grafico}")
