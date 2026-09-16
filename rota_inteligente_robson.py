
import math
from sklearn.cluster import KMeans
import numpy as np

pontos_entrega = {
    "Base Central": (1, 8),
    "Vila Industrial": (3, 6),
    "Jardim Horizonte": (5, 8),
    "Parque Verde": (8, 7),
    "Vila das Acacias": (9, 4),
    "Jardim Imperial": (6, 3),
    "Vila Bela": (3, 2),
    "Jardim Novo": (1, 4)
}

grafo = {
    "Base Central": {"Vila Industrial": 3, "Jardim Novo": 4},
    "Vila Industrial": {
        "Base Central": 3,
        "Jardim Horizonte": 3,
        "Vila Bela": 4
    },
    "Jardim Horizonte": {
        "Vila Industrial": 3,
        "Parque Verde": 4
    },
    "Parque Verde": {
        "Jardim Horizonte": 4,
        "Vila das Acacias": 3
    },
    "Vila das Acacias": {
        "Parque Verde": 3,
        "Jardim Imperial": 4
    },
    "Jardim Imperial": {
        "Vila das Acacias": 4,
        "Vila Bela": 3
    },
    "Vila Bela": {
        "Jardim Imperial": 3,
        "Vila Industrial": 4,
        "Jardim Novo": 3
    },
    "Jardim Novo": {
        "Base Central": 4,
        "Vila Bela": 3
    }
}

def distancia_entre_pontos(ponto1, ponto2):
    x1, y1 = pontos_entrega[ponto1]
    x2, y2 = pontos_entrega[ponto2]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def heuristica(local_atual, destino):
    return distancia_entre_pontos(local_atual, destino)

def a_estrela(inicio, destino):
    abertos = [inicio]
    custo = {inicio: 0}
    caminho_anterior = {}

    while abertos:
        atual = min(
            abertos,
            key=lambda local: custo[local] + heuristica(local, destino)
        )

        if atual == destino:
            caminho = []

            while atual in caminho_anterior:
                caminho.append(atual)
                atual = caminho_anterior[atual]

            caminho.append(inicio)
            caminho.reverse()

            return caminho, custo[destino]

        abertos.remove(atual)

        for vizinho, distancia in grafo[atual].items():
            novo_custo = custo[atual] + distancia

            if vizinho not in custo or novo_custo < custo[vizinho]:
                custo[vizinho] = novo_custo
                caminho_anterior[vizinho] = atual

                if vizinho not in abertos:
                    abertos.append(vizinho)

    return None, float("inf")


inicio = "Base Central"
destino = "Vila das Acacias"

rota, distancia = a_estrela(inicio, destino)

locais = list(pontos_entrega.keys())
coordenadas = np.array([pontos_entrega[local] for local in locais])

kmeans = KMeans(n_clusters=3, random_state=10, n_init=10)
grupos = kmeans.fit_predict(coordenadas)

print("ROTA OTIMIZADA:")
print(" -> ".join(rota))
print("Distância total:", distancia, "km")

print("\nAGRUPAMENTO DAS ENTREGAS:")
for local, grupo in zip(locais, grupos):
    print(local, "-> Grupo", grupo + 1)
