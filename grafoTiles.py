import time

class Grafo():
    def __init__(self, dicTiles):
        self.vertices = list(dicTiles.keys())
        self.vizinhos = list(dicTiles.values())
        
    def Dijkstra(self, vertice, final = None):

        V = self.vertices
        parents = [0] * len(V)
        dist = [float('inf')] * len(V)
        S = []
        dist[vertice] = 0
        parents[vertice] = -1 
        while (len(S) == len(set(S))):
            diff = list(set(V) - set(S))
            minDist = float('inf')
            for k in diff:
                if dist[k] < minDist:
                    minDist = dist[k]
                    u = k
            
            S.append(u)
            if (u == final):
                break
            for vizinho in self.vizinhos[u]:
                if dist[vizinho] > dist[u] + 1:
                    dist[vizinho] = dist[u] + 1
                    parents[vizinho] = u 
        
        return dist, parents

