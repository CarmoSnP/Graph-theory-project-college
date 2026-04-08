class Grafo:
    def __init__(self, dirigido=False):
        """
        inincia o grafo
        dirigido = false -> grafo comum arestas
        dirigido = true -> digrafo arcos
        """
        self.dirigido = dirigido

        # vertices do grafo
        self.vertices = {}
        # arestas do grafo "linhas"
        self.arestas = {}
        # listas de adjacencia
        self.adj = {}
        # contador de arestas para ids de arestas.
        self._cont_aresta = 1
