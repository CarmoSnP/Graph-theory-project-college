import networkx as nx  # manipular grafos
import matplotlib.pyplot as plt  # desenhar grafos
import heapq  # da prioriadade para o algoritmo de prim
from collections import deque  # fila de Busca em largura

"""
estrutura de variaveis
    v        = vertice de origem          ex: 'A'
    w        = vertice de destino         ex: 'C'
    peso     = custo/peso da aresta       ex: 4
    aid      = identificador da aresta    ex: 'a1'
    idx      = indice do vertice na matriz ex: 0, 1, 2...
    pai      = dicionario de quem descobriu cada vertice no BFS/DFS
    heap     = fila de prioridade do Prim (sempre retorna o menor)
    alcanca  = matriz de alcancabilidade do Roy (True/False)
    visitados= conjunto de vertices ja processados
    caminho  = lista de vertices do caminho encontrado (BFS/DFS)
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

        v = v.upper()

        if not v:
            print("[!] ID do vertice nao pode ser vazio.")
            return

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
        v = v.upper()
        w = w.upper()

        if not v or not w:
            print("[!] Vertice de origem ou destino nao pode ser vazio.")
            return

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

        v = v.upper()

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

        id_aresta = id_aresta.lower()

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
            chave = (v, w)
            chave_inv = (w, v)
            if chave in labels_arestas:
                # ja existe label nessa aresta, adiciona na mesma linha
                labels_arestas[chave] += f"\n{aid} (w={peso})"
            elif chave_inv in labels_arestas:
                # ja existe aresta no sentido inverso, adiciona lá
                labels_arestas[chave_inv] += f"\n{aid} (w={peso})"
            else:
                # primeira aresta dos vertices
                labels_arestas[chave] = f"{aid} (w={peso})"

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
            G,
            pos,
            edge_color=cores,
            width=2,
            arrows=self.dirigido,
            arrowsize=20,
            connectionstyle="arc3,rad=0.2",  # curvas na setas
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
            return [], 0

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

        if not arestas_agm:
            return

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

        fila = deque([origem])  # começa com a origem na fila
        visitados = {origem}  # marca origem como visitada
        pai = {origem: None}  # guardar o pai de cada vertice
        arestas_arvore = []  # arestas que formam a árvore BFS

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

        if not caminho:
            print("caminho nao foi encontrado")
            return

        print(f" Arvore de busca em largura: =='{origem}' --> '{destino}'==")
        if caminho:
            print(f"Caminho: {'->' .join(map(str, caminho))}")
        else:
            print("caminho nao encontrado")
            return

        self.mostrar_grafo(
            titulo=f"BFS: {origem} -> {destino} | Caminho: {'->'.join(map(str, caminho))}",
            destaque_arestas=arestas_arvore,
        )

    def dfs(self, origem, destino):
        """
        busca em profundidade, vai o mais fundo possivel antes de voltar
        usa pilha nao fila
        """

        if origem not in self.vertices or destino not in self.vertices:
            print(f"[!] Vertice de inicio ou de fim invalido")
            return [], []

        pilha = [origem]  # começa com a origem na pilha
        visitados = {origem}  # marca origem como visitada
        pai = {origem: None}  # guarda quem descobriu cada vértice
        arestas_arvore = []  # arestas que formam a árvore DFS

        encontrado = False
        while pilha:
            v = pilha.pop()

            if v == destino:
                encontrado = True
                break
            for w, aid, _ in self.adj[v]:
                if w not in visitados:
                    visitados.add(w)
                    pai[w] = v
                    arestas_arvore.append((v, w))
                    pilha.append(w)  # adiciona ao topo
        caminho = []
        if encontrado:
            cur = destino
            while cur is not None:
                caminho.append(cur)
                cur = pai[cur]
            caminho.reverse()

        return caminho, arestas_arvore

    def mostrar_dfs(self, origem, destino):
        """
        executa DFS e exibe a arvore
        """

        caminho, arestas_arvore = self.dfs(origem, destino)

        if not caminho:
            print("caminho nao foi encontrado")
            return

        print(f"\n = DFS: '{origem}' --> '{destino}' =")
        if caminho:
            print(f" Caminho: {'->'.join(map(str, caminho))}")
        else:
            print(" Caminho nao encontrado.")
            return
        self.mostrar_grafo(
            titulo=f"DFS: {origem} -> {destino} | Caminho: {' -> '.join(map(str, caminho))}",
            destaque_arestas=arestas_arvore,
        )

    def roy(self):
        """
        encontra componentes conexas ou fortemente conexas
        """
        verts = list(self.vertices.keys())
        n = len(verts)
        idx = {v: i for i, v in enumerate(verts)}  # mapeia vertice e indice

        # matriz de alcancabilidade - alcanca[i][i] = true se i chega em j
        alcanca = [[False] * n for _ in range(n)]

        # todo vertice alcanca a si mesmo
        for i in range(n):
            alcanca[i][i] = True

        for v, w, _ in self.arestas.values():
            alcanca[idx[v]][idx[w]] = True
            if not self.dirigido:
                alcanca[idx[w]][idx[v]] = True

        # fechamento transitivo de Roy
        # se i alcança k E k alcança j → i alcança j
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if alcanca[i][k] and alcanca[k][j]:
                        alcanca[i][j] = True

        # agrupa componentes
        componentes = []
        nao_visitados = set(range(n))

        while nao_visitados:
            i = next(iter(nao_visitados))
            componente = set()
            for j in list(nao_visitados):
                if self.dirigido:
                    # fortemente conexo: i→j E j→i
                    if alcanca[i][j] and alcanca[j][i]:
                        componente.add(j)
                else:
                    # conexo: i→j (basta alcançar)
                    if alcanca[i][j]:
                        componente.add(j)
            componentes.append({verts[j] for j in componente})
            nao_visitados -= componente

        return componentes

    def mostrar_roy(self):
        """
        Executa Roy e exibe os conjuntos de componentes.
        """
        comps = self.roy()
        tipo = "Fortemente Conexas" if self.dirigido else "Conexas"
        print(f"\n  === Componentes {tipo} (Roy) ===")
        for i, comp in enumerate(comps, 1):
            print(f"  Componente {i}: {sorted(comp, key=str)}")


def cabecalho():
    print("\n" + "=" * 60)
    print("        TRABALHO T1 - GRAFOS")
    print("   UNIVALI 2026/1 | Profa Fernanda Cunha")
    print("=" * 60)


def menu():
    print("\n" + "-" * 60)
    print("  MENU PRINCIPAL")
    print("-" * 60)
    print("  [1]  Inserir vertice")
    print("  [2]  Inserir aresta/arco")
    print("  [3]  Remover vertice")
    print("  [4]  Remover aresta/arco")
    print("  [5]  Mostrar grafo")
    print("  [6]  Algoritmo de Prim (AGM)")
    print("  [7]  Busca em Largura - BFS")
    print("  [8]  Busca em Profundidade - DFS")
    print("  [9]  Componentes Conexas - Roy")
    print("  [0]  Sair")
    print("-" * 60)


def info_grafo(g):
    tipo = "Dirigido" if g.dirigido else "Nao-Dirigido"
    print(f"\n  Grafo atual: {tipo}")
    print(f"  Vertices ({len(g.vertices)}): {list(g.vertices.keys())}")
    print(f"  Arestas  ({len(g.arestas)}): {list(g.arestas.keys())}")


def main():
    cabecalho()

    print("\n  Tipo de grafo:")
    print("  [1] Nao-dirigido (arestas)")
    print("  [2] Dirigido (arcos/digrafo)")
    escolha = input("  Escolha: ").strip()
    dirigido = escolha == "2"
    g = Grafo(dirigido=dirigido)
    tipo_str = "Dirigido" if dirigido else "Nao-Dirigido"
    print(f"\n  Grafo {tipo_str} criado!")

    while True:
        info_grafo(g)
        menu()
        opcao = input("  Opcao: ").strip()

        if opcao == "1":
            v = input("  ID do vertice: ").strip().upper()
            g.insert_vertice(v)

        elif opcao == "2":
            v = input("  Vertice de origem: ").strip().upper()
            w = input("  Vertice de destino: ").strip().upper()
            try:
                peso = float(input("  Peso (padrao=1): ").strip() or 1)
            except ValueError:
                peso = 1
            g.insert_aresta(v, w, peso=peso)

        elif opcao == "3":
            v = input("  ID do vertice a remover: ").strip().upper()
            g.remover_vertice(v)

        elif opcao == "4":
            aid = input("  ID da aresta a remover (ex: a1): ").strip().upper()
            g.remover_aresta(aid)

        elif opcao == "5":
            if not g.vertices:
                print("  [!] Grafo vazio.")
            else:
                g.mostrar_grafo(titulo="Grafo Atual")

        elif opcao == "6":
            if g.dirigido:
                print("  [!] Prim apenas para grafos nao-dirigidos.")
            else:
                inicio = input("  Vertice inicial: ").strip().upper()
                g.mostrar_prim(inicio)

        elif opcao == "7":
            origem = input("  Vertice de origem: ").strip().upper()
            destino = input("  Vertice de destino: ").strip().upper()
            g.mostrar_bfs(origem, destino)

        elif opcao == "8":
            origem = input("  Vertice de origem: ").strip().upper()
            destino = input("  Vertice de destino: ").strip().upper()
            g.mostrar_dfs(origem, destino)

        elif opcao == "9":
            g.mostrar_roy()

        elif opcao == "0":
            print("\n  Code by Igor Carmo and Wellington Moura!\n")
            break

        else:
            print("  [!] Opcao invalida.")

        input("\n  Pressione ENTER para continuar...")


# ponto de entrada do programa
if __name__ == "__main__":
    main()


# teste rapido
# g = Grafo(dirigido=False)
# g.insert_vertice("A")
# g.insert_vertice("B")
# g.insert_vertice("C")
# g.insert_vertice("D")
# g.insert_aresta("A", "B", peso=4)
# g.insert_aresta("A", "C", peso=2)
# g.insert_aresta("B", "C", peso=5)
# g.insert_aresta("B", "D", peso=10)
# g.insert_aresta("C", "D", peso=3)
# g.mostrar_bfs("A", "D")
