import networkx as nx
from database.DAO import DAO
import copy

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllNodes(self, s):
        nodes = DAO.getAllNodes(s)
        for i in nodes:
            self._idMap[i.order_id] = i
        return nodes

    def getAllEdges(self, s, k):
        RawEdges = DAO.getAllEdges(s, k)
        edges = []
        for i in RawEdges:
            if i[0] in self._idMap and i[1] in self._idMap:
                weight_decimal = i[2]
                weight = int(weight_decimal) if weight_decimal is not None else 0
                edges.append((self._idMap[i[0]], self._idMap[i[1]], {'weight': weight}))
        print(edges)
        return edges

    def creaGrafo(self, s, k):
        self._grafo.add_nodes_from(self.getAllNodes(s))
        self._grafo.add_edges_from(self.getAllEdges(s, k))
        return True, self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getCamminoLungo(self, n):
        reachable_nodes = nx.descendants(self._grafo, n)
        reachable_nodes.add(n)
        tree = self._grafo.subgraph(reachable_nodes).copy()  # copia per sicurezza e mantieni i dati
        cammino = nx.dag_longest_path(tree, weight="weight")
        print(cammino)
        peso = nx.path_weight(tree, cammino, weight="weight")
        return cammino, peso


    def getSequenzaOttima(self, n):
        self._sequenzaOttima = []
        self._costoMax = -1
        self.ricorsione([n], list(self._grafo.neighbors(n)))
        return self._sequenzaOttima, self._costoMax

    def ricorsione(self, parziale, sequenza):
        if len(sequenza) == 0:
            costo = self.costo(parziale)
            if costo > self._costoMax:
                self._costoMax = costo
                self._sequenzaOttima = copy.deepcopy(parziale)
                print(f"aggiornamento ({len(self._sequenzaOttima)}): {self._costoMax} - {self._sequenzaOttima}")
        else:
            for i in sequenza:
                if self.vincoli(parziale, i):
                    parziale.append(i)
                    self.ricorsione(parziale, list(self._grafo.neighbors(parziale[-1])))
                    parziale.pop()

    def vincoli(self, parziale, i):
        if i in parziale:
            return False
        if len(parziale) >= 2:
            if self._grafo[parziale[-2]][parziale[-1]]['weight'] < self._grafo[parziale[-1]][i]['weight']:
                return False
        return True

    def costo(self, parziale):
        costoTot = 0
        for i in range(0, len(parziale)-1):
            costoTot += self._grafo[parziale[i]][parziale[i+1]]['weight']
        return costoTot





