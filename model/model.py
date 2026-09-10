import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMapNodes = {}
        self._bestPath = []

    def getAllRatings(self):
        return DAO.getAllRatings()

    def buildGraph(self, r1, r2):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(r1, r2)
        self._graph.add_nodes_from(self._nodes)
        for n in self._nodes:
            self._idMapNodes[n.id] = n

        allEdges = DAO.getAllEdges(r1, r2, self._idMapNodes)
        for e in allEdges:
            self._graph.add_edge(e[0], e[1], weight=e[2])

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getArchiMaggiori(self):
        edges = sorted(
            self._graph.edges(data=True),
            key=lambda x: x[2]["weight"],
            reverse=True
        )
        return edges[:5]  # in questo caso sono i 5 archi di peso maggiore

    def getConnectedComponents(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        return components, largest

    def getBestPath(self):

        self._bestPath = []

        for start in self._graph.nodes():
            partial = [start]
            self._ricorsione(partial)

        return self._bestPath

    def _ricorsione(self, partial):

        if len(partial) > len(self._bestPath):
            self._bestPath = list(partial)

        current = partial[-1]

        for _, successor in self._graph.edges(current):

            # vincolo: età decrescente
            if successor not in partial and successor.birth_date > current.birth_date:
                partial.append(successor)

                self._ricorsione(partial)

                partial.pop()

