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
            direcao = f"{v} <--> {w}"

        tipo = "Arco" if self.dirigido else "Aresta"
        print(f"[+] {tipo} '{id_aresta}' ({direcao}, peso={peso}) inserida")

    def remover_vertice(self, v):
        """
        remover o vertice e todos ligados a ele.
        """
        if v not in self.vertices:
            print(f"[!] Vertice '{v}' nao encontrado")
            return

        # encontra todas as arestas que estao ligadas ao vertices
        ids_remover = []
        for id_aresta, (origem, destino, peso) in self.arestas.items():
            if origem == v or destino == v:
                ids_remover.append(id_aresta)
        # laco para remover as arestas
        for id_aresta in ids_remover:
            self.remover_aresta(id_aresta)

        # remover o vertice
        del self.vertices[v]
        del self.adj[v]

        print(f"[-] Vertice '{v}' e arestas ligados a ele foram removidos")

    def remover_aresta(self, id_aresta):
        """
        remover aresta ou arco pelo vertice
        """
        if id_aresta not in self.arestas:
            print(f" [!] Aresta '{id_aresta}' nao encontrada")
            return
        # pega as infos da aresta
        v, w, peso = self.arestas[id_aresta]

        # remove da lista de adjacencia do vertice
        self.adj[v] = [
            (vizinho, aid, p) for (vizinho, aid, p) in self.adj[v] if aid != id_aresta
        ]

        # se nao dirigiro, remove da lista de adj
        if not self.dirigido:
            self.adj[w] = [
                (vizinho, aid, p)
                for (vizinho, aid, p) in self.adj[w]
                if aid != id_aresta
            ]
        # remove da lista de arestas
        del self.arestas[id_aresta]

        # seta para dirigido e nao dirigido
        if self.dirigido:
            direcao = f"{v} --> {w}"
        else:
            direcao = f"{v} <--> {w}"
        tipo = "Arco" if self.dirigido else "Aresta"
        print(f" [-] {tipo} '{id_aresta}' ({direcao}) removida.")
