class Grafo:
    # method init usado para principalmente para criar objetos em python
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

    def insert_vertice(self, v):
        """
        metodo para inserir um vertice isolado no grafo.
        v = identificador do vértice (ex: 'a', 1, 'SC')
        """
        if v in self.vertices:
            print(f"[!] Vertice '{v}' ja existe")
            return
        self.vertices[v] = str(
            v
        )  # adiciona vertice, usa o str para passar para string.
        self.adj[v] = []  # cria a lista de adjacencia

        print(f"[+] Vertice '{v}' adicionado")

    def insert_aresta(self, v, w, peso=1):
        """
        insere uma aresta ou um arco entre os vertices
        peso = custo das ligações

        usando append para adicionar ao final
        """
        if v not in self.vertices or w not in self.vertices:
            print(f"[!] Vertice '{v}' ou '{w}' nao existem")
            return
        # gera o id da aresta conforme o contador
        id_aresta = f"a{self._cont_aresta}"
        self._cont_aresta += 1

        # salva a aresta com o peso dela
        self.arestas[id_aresta] = (v, w, peso)

        # adiona a lista de adjacencia de v
        self.adj[v].append((w, id_aresta, peso))

        # se for nao dirigido ele adiciona tambem em w a ligacao fica dos dois lados
        if not self.dirigido:
            self.adj[w].append((v, id_aresta, peso))

        if self.dirigido:
            # se for dirigido a seta apenas para a ligacao do proximo
            direcao = f"{v} --> {w}"
        else:
            # se for nao dirigido a seta e uma via de mao dupla
            direcao = f"{v} <-> {w}"

        tipo = "Arco" if self.dirigido else "Aresta"
        print(f"[+] {tipo} '{id_aresta}' ({direcao}, peso={peso}) inserida")
