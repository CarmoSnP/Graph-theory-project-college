# UNIVALI – POLITECNICA Kobrasol – Ciência da Computação – 2026/1

## GRAFOS T1 – profª Fernanda Cunha

## Alunos : Igor do Carmo e Wellington Moura

---

Dado que um grafo G = (V, A) consiste em:

- um conjunto finito de pontos V. Os elementos de V são chamados de vértices de G.
- um conjunto finito A de pares (v,w) de V, que são chamados de arestas/arcos de G. Uma aresta a contida em A é um par não ordenado (v, w) de vértices v, w em V, que são chamados de extremidades de a. Um arco a contido em A é um par ordenado (v, w) de vértices v, w em V, que são chamados de extremidades de a.

Um vértice v contido em V é vizinho (adjacente) de outro vértice w em V se existir uma aresta a contida em A incidente com v e w.

Uma aresta/arco a contida em A é chamada de incidente sobre um vértice v contido em V, se v for uma extremidade de a.

Todo vértice deve ter um identificador. Toda aresta/arco deve ter um identificador e um valor numérico (custo/peso).

---

Elabore um tipo/classe para representar grafos, dirigidos e não dirigidos, de qualquer tamanho, usando obrigatoriamente **LISTA DE ADJACÊNCIA**. Reflita sobre quais são os atributos necessários para representar um grafo.

---

Sua implementação deverá apresentar as operações (após cada item tem-se sua pontuação):

- inserir no grafo um novo vértice isolado v; (0,5)
- inserir no grafo uma aresta/arco entre os vértices v-w; (0,5)
- remover o vértice v (e suas ligações por consequência); (0,5)
- remover a ligação (aresta/arco) a; (0,5)
- mostrar graficamente o grafo, com as informações de vértices e ligações (aresta/arco); (1,5)

**Obs.:** em substituição a este item, o programa deverá montar/mostrar a matriz de adjacência do grafo e montar/mostrar a matriz de incidência do grafo (valendo apenas 0,5 por matriz).

- aplicar o algoritmo de PRIM no grafo e mostrar graficamente a Árvore Geradora Mínima (AGM) e seu custo; (1,5)

- aplicar a Busca em Largura no grafo, definindo o vértice de saída e de chegada (busca guiada), e mostrar graficamente árvore gerada; (1,5)

- aplicar a Busca em Profundidade no grafo, definindo o vértice de saída e de chegada (busca guiada), e mostrar graficamente árvore gerada; (1,5)

- aplicar o algoritmo de Roy para determinar as componentes conexas/fortemente conexas do grafo e mostrar os conjuntos. (1,5)

---

Desenvolva um programa com interface básica (tela com moldura e menu) para acessar estas operações e visualização do grafo ativo. Caso isso não ocorra, será descontado 1,5 da nota final.

---

Serão considerados para efeitos de avaliação: a corretude e a otimização do programa; a adequação da interface; e as respostas do aluno aos questionamentos durante a defesa.

---

O TRABALHO SERÁ DESENVOLVIDO OBRIGATORIAMENTE EM DUPLA. A dupla deverá postar o código fonte e um executável do trabalho no link da avaliação até as 18h de 10/04/2026.

A defesa do trabalho será feita no laboratório 311 na mesma data conforme cronograma divulgado no AVA. No momento da defesa a dupla deverá entregar o código impresso.

---

Cfe. regimento interno da universidade e plano de ensino da disciplina:

> “Qualquer atividade avaliativa receberá nota 0 (zero) caso apresente sinais de cópia. Isso vale tanto para o copiado como para o copiador.”

Além disso, os trabalhos não defendidos também receberão nota 0 (zero).
