import networkx as nx
import pandas as pd

def create_network():
    G = nx.Graph()
    # Використовуємо твій повний список з'єднань (з app.py)
    edges = [
        ("Core","R1",2), ("Core","R2",3), ("Core","R3",2), ("Core","R4",4),
        ("R1","DB_Server",1), ("R1","Web_Server",2), ("R1","Mail_Server",2), ("R1","DNS_Server",1),
        ("R2","SW1",2), ("R2","SW2",3), ("R3","SW3",2), ("R4","SW4",3),
        ("SW1","PC1",1), ("SW1","PC2",1), ("SW1","PC3",2), ("SW1","PC4",2),
        ("SW2","PC5",1), ("SW2","PC6",2), ("SW2","PC7",1), ("SW2","PC8",2),
        ("SW3","PC9",1), ("SW3","PC10",2), ("SW3","PC11",1), ("SW3","PC12",2),
        ("SW4","PC13",1), ("SW4","PC14",2), ("SW4","PC15",1),
        ("R2","R3",4), ("R3","R4",3), ("R2","R4",5),
        ("Firewall1","Core",2), ("Firewall2","Core",2),
        ("Firewall1","Internet",3), ("Firewall2","Internet",3)
    ]
    G.add_weighted_edges_from(edges)
    return G

def shortest_path(G, start, end):
    path = nx.dijkstra_path(G, start, end)
    length = nx.dijkstra_path_length(G, start, end)
    return path, length

def backup_path(G, start, end):
    paths = list(nx.shortest_simple_paths(G, start, end, weight='weight'))
    if len(paths) > 1:
        return paths[1]
    return None

def network_connected(G):
    return nx.is_connected(G)

def critical_nodes(G):
    return list(nx.articulation_points(G))

# --- НОВІ ФУНКЦІЇ ДЛЯ ВИМОГ ВИКЛАДАЧА ---

def get_network_density(G):
    # Щільність графа
    return nx.density(G)

def get_connected_components(G):
    # Компоненти зв'язності (аналіз розпаду)
    return list(nx.connected_components(G))

def get_mst(G):
    # Мінімальне остовне дерево (MST)
    # Якщо граф розпався, це побудує мінімальний остовний ліс
    return nx.minimum_spanning_tree(G, weight='weight')

def get_node_metrics(G):
    # Формальний аналіз ступенів та центральності
    degree_physical = dict(G.degree())
    degree_cent = nx.degree_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G, weight='weight')
    closeness_cent = nx.closeness_centrality(G, distance='weight')

    df = pd.DataFrame({
        "Вузол": list(G.nodes()),
        "Фізичний ступінь (К-сть лінків)": [degree_physical[n] for n in G.nodes()],
        "Degree Centrality": [round(degree_cent[n], 4) for n in G.nodes()],
        "Betweenness (Транзитність)": [round(betweenness_cent[n], 4) for n in G.nodes()],
        "Closeness (Близькість)": [round(closeness_cent[n], 4) for n in G.nodes()]
    }).set_index("Вузол")
    
    # Сортуємо за найважливішим показником транзитності
    df = df.sort_values(by="Betweenness (Транзитність)", ascending=False)
    return df
