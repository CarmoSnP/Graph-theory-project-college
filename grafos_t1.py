import networkx as nx  # manipular grafos
import matplotlib.pyplot as plt  # desenhar grafos
import heapq  # da prioriadade para o algoritmo de prim
from collections import deque  # fila de Busca em largura

"""
estrutura de variaveis
peso = 2
v    = 'A'   (origem)
w    = 'C'   (destino)
aid  = 'a2'  (identificador)
"""


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

    def mostrar_grafo(self, titulo="Grafo", destaque_arestas=None):
        """
        exibe o grafo na tela usando o mathplotlib
        """
        if self.dirigido:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        # adiciona todos os vertices no objeto
        G.add_nodes_from(self.vertices.keys())

        labels_arestas = {}
        for aid, (v, w, peso) in self.arestas.items():
            G.add_edge(v, w, weight=peso)
            labels_arestas[(v, w)] = f"{aid} (w={peso})"

        # define o layout na tela a posicao
        pos = nx.spring_layout(G, seed=42)

        # desenha o grafo
        plt.figure(figsize=(10, 7))
        plt.title(titulo, fontsize=14, fontweight="bold")

        # desenha os vertices
        nx.draw_networkx_nodes(G, pos, node_color="steelblue", node_size=1500)

        # monstra o nome do vertice
        nx.draw_networkx_labels(
            G,
            pos,
            labels={v: v for v in self.vertices},
            font_color="white",
            font_size=11,
            font_weight="bold",
        )

        # destaque as linhas para mostar o prim
        cores = []
        for v, w in G.edges():
            if destaque_arestas and (
                (v, w) in destaque_arestas or (w, v) in destaque_arestas
            ):
                cores.append("red")
            else:
                cores.append("gray")

        # desenha as linhas
        nx.draw_networkx_edges(
            G, pos, edge_color=cores, width=2, arrows=self.dirigido, arrowsize=20
        )

        # desenha o id e peso das linhas
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_arestas, font_size=8)

        plt.axis("off")  # off para retirar os eixos x e y
        plt.tight_layout()  # ajusto espacamento
        plt.show()  # exibir na tela

    def prim(self, inicio):
        """
        encontrar a arvore minima a partir de qualquer vertice
        """

        if inicio not in self.vertices:
            print(f"[!] Vertice '{inicio}' nao existe dentro do grafo.")
            return

        visitados = {inicio}
        arestas_agm = []
        custo_total = 0

        # aqui estamos usando o heap para dentro de uma fila ele sempre retornar o menor elemento.
        # formato usado {peso, vertice_origem, vertice_destino, id_aresta}
        heap = []
        for w, aid, peso in self.adj[inicio]:
            heapq.heappush(heap, (peso, inicio, w, aid))

        while heap and len(visitados) < len(self.vertices):
            # aqui pegamos sempre a menor aresta do heap
            peso, v, w, aid = heapq.heappop(heap)

            # verificacao se foi visitado a aresta
            if w in visitados:
                continue

            # adicona a lista de visitados
            visitados.add(w)
            arestas_agm.append((v, w, peso, aid))
            custo_total += peso

            # adiciona a aresta de w para o heap explorar
            for vizinho, aid2, peso2 in self.adj[w]:
                if vizinho not in visitados:
                    heapq.heappush(heap, (peso2, w, vizinho, aid2))

        return arestas_agm, custo_total

    def mostrar_prim(self, inicio):
        """
        exibir o grafo de prim, arvore
        """
        arestas_agm, custo = self.prim(inicio)

        print(f"\n Vertice inicial de prim '{inicio}'")
        for v, w, peso, aid in arestas_agm:
            print(f"{v} --[{aid}, peso={peso}]-->{w}")
        print(f"custo total de prim: {custo}")

        # destaque da arestas de prim
        destaque = [(v, w) for (v, w, _, _) in arestas_agm]
        self.mostrar_grafo(
            titulo=f"AGM Prim (inicio: {inicio} | custo total: {custo})",
            destaque_arestas=destaque,
        )

    def bsf(self, origem, destino):
        """
        busca em largura, achar o menor caminho entre 2 pontos
        """
        if origem not in self.vertices or destino not in self.vertices:
            print(f"[!] Vertice de incio ou fim invalido.")
            return [], []

        fila = deque([origem])
        visitados = {origem}
        pai = {origem: None}  # guardar o pai de cada vertice
        arestas_arvore = []

        encontrado = False
        while fila:
            v = fila.popleft()  # fifo

            if v == destino:
                encontrado = True
                break
            for w, aid, _ in self.adj[v]:
                if w not in visitados:
                    visitados.add(w)
                    pai[w] = v
                    arestas_arvore.append((v, w))
                    fila.append(w)
        caminho = []
        if encontrado:
            cur = destino
            while cur is not None:
                caminho.append(cur)
                cur = pai[cur]
            caminho.reverse()  # inverte pois construimos de tras pra frente

        return caminho, arestas_arvore

    def mostrar_bfs(self, origem, destino):
        """
        executa BFS e exibe a arvore graficamente
        usa fila, busca em largura
        """
        caminho, arestas_arvore = self.bsf(origem, destino)
        print(f"\ Arvore de busca em largura: =='{origem}' --> '{destino}'==")
        if caminho:
            print(f"Caminho: {'->' .join(map(str, caminho))}")
        else:
            print("caminho nao encontrado")

        self.mostrar_grafo(
            titulo=f"BFS: {origem} -> {destino} | Caminho: {'->'.join(map(str, caminho))}",
            destaque_arestas=arestas_arvore,
        )


# teste rápido
g = Grafo(dirigido=False)
g.insert_vertice("A")
g.insert_vertice("B")
g.insert_vertice("C")
g.insert_vertice("D")
g.insert_aresta("A", "B", peso=4)
g.insert_aresta("A", "C", peso=2)
g.insert_aresta("B", "C", peso=5)
g.insert_aresta("B", "D", peso=10)
g.insert_aresta("C", "D", peso=3)
g.mostrar_bfs("A", "D")
