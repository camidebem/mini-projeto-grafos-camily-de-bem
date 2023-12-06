import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import community

# Lendo os vértices do arquivo
nodes_file_path = 'fb-pages-food.nodes'
nodes_df = pd.read_csv(nodes_file_path)

# Lendo os arestas do arquivo
edges_file_path = 'fb-pages-food.edges'
edges_df = pd.read_csv(edges_file_path, header=None,
                       names=['source', 'target'])

# Contagem do número de conexões para cada página
influence_count = pd.concat(
    [edges_df['source'], edges_df['target']]).value_counts()

# Obtenção das 10 páginas mais influentes
top_10_influencers = influence_count.head(10)

# Obtendo os nomes das páginas correspondentes aos IDs
top_10_names = nodes_df.set_index(
    'new_id').loc[top_10_influencers.index]['name']

# Plotando o gráfico de barras para as 10 páginas mais influentes
plt.figure(figsize=(15, 8))

plt.subplot(2, 2, 1)
top_10_influencers.plot(kind='bar', color='skyblue')
plt.title('Top 10 Páginas Mais Influentes no Meio Culinário')
plt.xlabel('ID da Página')
plt.ylabel('Número de Conexões')
plt.xticks(rotation=45)

# Exibindo os nomes das páginas correspondentes ao top 10
plt.subplot(2, 2, 2)
plt.table(cellText=top_10_names.reset_index().values,
          colLabels=['ID da Página', 'Nome'],
          cellLoc='center',
          loc='center')
plt.axis('off')
plt.title('Nomes das Páginas Correspondentes ao Top 100')

# Criação do grafo não direcionado a partir das arestas
G = nx.from_pandas_edgelist(
    edges_df, 'source', 'target', create_using=nx.Graph())

# Detecção de comunidades usando o algoritmo Louvain
communities = community.best_partition(G)

# Adiciona as comunidades aos dados do nó
nodes_df['community'] = nodes_df['new_id'].map(communities)

# Contagem do número de conexões para cada página
influence_count = pd.concat(
    [edges_df['source'], edges_df['target']]).value_counts()

# Obtenção das 10 páginas mais influentes
top_10_influencers = influence_count.head(10)

# Obtendo os nomes das páginas correspondentes aos IDs
top_10_names = nodes_df.set_index(
    'new_id').loc[top_10_influencers.index]['name']

# Cálculo da centralidade de intermediação
betweenness_centrality = nx.betweenness_centrality(G)

# Adiciona a centralidade de intermediação aos dados do nó
nodes_df['betweenness_centrality'] = nodes_df['new_id'].map(
    betweenness_centrality)

# Identifica páginas de transição (pontes)
bridge_pages = nodes_df.sort_values(
    by='betweenness_centrality', ascending=False).head(5)

# Avaliação da resiliência da rede


def evaluate_resilience(graph, nodes_to_remove):
    connected_components_sizes = []
    removed_nodes_list = []  # Lista para armazenar os nós removidos em cada etapa
    G_copy = graph.copy()
    for node in nodes_to_remove:
        G_copy.remove_node(node)
        connected_components = list(nx.connected_components(G_copy))
        connected_components_sizes.append(len(connected_components))
        # Adiciona os nós removidos à lista
        removed_nodes_list.append(node)
    return connected_components_sizes, removed_nodes_list


# Remove os 5 nós com maior centralidade de grau (páginas estratégicas)
strategic_nodes = list(G.degree(weight='weight'))
strategic_nodes.sort(key=lambda x: x[1], reverse=True)
strategic_nodes = [node[0] for node in strategic_nodes[:5]]

# Avaliação da resiliência
resilience_results, removed_nodes_list = evaluate_resilience(
    G, strategic_nodes)

# Plotando Gráfico da Avaliação da resiliência da rede
plt.subplot(2, 2, 3)
plt.plot(resilience_results, marker='o', linestyle='-', color='orange')
plt.title('Avaliação da Resiliência da Rede')
plt.xlabel('Número de Nós Removidos')
plt.ylabel('Número de Componentes Conectados')

# Exibindo os nomes das páginas correspondentes às páginas de transição
plt.subplot(2, 2, 4)
removed_nodes_df = nodes_df.set_index('new_id').loc[removed_nodes_list][[
    'name', 'community', 'betweenness_centrality']]
plt.table(cellText=removed_nodes_df.values,
          colLabels=['Nome', 'Comunidade', 'Betweenness Centrality'],
          cellLoc='center',
          loc='center')
plt.axis('off')
plt.title('Informações das Páginas Removidas por Ordem de Remoção')

plt.tight_layout()
plt.savefig('graphs.pdf'format='pdf')
