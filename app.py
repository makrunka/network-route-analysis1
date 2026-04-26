import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.set_page_config(page_title="Аналіз маршрутів мережі", layout="wide")

# ----------------------------
# Створення корпоративної мережі (30 вузлів)
# ----------------------------

def create_network():
    G = nx.Graph()

    edges = [
    # Core
    ("Core","R1",2),
    ("Core","R2",3),
    ("Core","R3",2),
    ("Core","R4",4),

    # Серверний сегмент
    ("R1","DB_Server",1),
    ("R1","Web_Server",2),
    ("R1","Mail_Server",2),
    ("R1","DNS_Server",1),

    # Комутатори
    ("R2","SW1",2),
    ("R2","SW2",3),
    ("R3","SW3",2),
    ("R4","SW4",3),

    # Клієнтські вузли
    ("SW1","PC1",1),
    ("SW1","PC2",1),
    ("SW1","PC3",2),
    ("SW1","PC4",2),

    ("SW2","PC5",1),
    ("SW2","PC6",2),
    ("SW2","PC7",1),
    ("SW2","PC8",2),

    ("SW3","PC9",1),
    ("SW3","PC10",2),
    ("SW3","PC11",1),
    ("SW3","PC12",2),

    ("SW4","PC13",1),
    ("SW4","PC14",2),
    ("SW4","PC15",1),

    # Резервні зв'язки
    ("R2","R3",4),
    ("R3","R4",3),
    ("R2","R4",5),

    ("Firewall1","Core",2),
    ("Firewall2","Core",2),

    ("Firewall1","Internet",3),
    ("Firewall2","Internet",3)
    ]

    G.add_weighted_edges_from(edges)
    return G

G = create_network()

nodes = sorted(G.nodes())

# ----------------------------
# Функції
# ----------------------------

def shortest_path(start,end):
    path = nx.dijkstra_path(G,start,end)
    length = nx.dijkstra_path_length(G,start,end)
    return path,length

def backup_path(start,end):
    paths=list(nx.shortest_simple_paths(G,start,end,weight='weight'))
    if len(paths)>1:
        return paths[1]
    return None

def network_connected():
    return nx.is_connected(G)

def critical_nodes():
    return list(nx.articulation_points(G))

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("Налаштування")

start = st.sidebar.selectbox(
"Початковий вузол",
nodes
)

end = st.sidebar.selectbox(
"Кінцевий вузол",
nodes,
index=5
)

failed_node=st.sidebar.selectbox(
"Симуляція відмови вузла",
["Немає"]+nodes
)

# Симуляція відмови
if failed_node!="Немає":
    G.remove_node(failed_node)

# ----------------------------
# Аналіз маршруту
# ----------------------------

st.title("Аналіз маршрутів корпоративної мережі")

if st.button("Запустити аналіз"):

    try:
        path,length=shortest_path(start,end)

        st.success(f"Найкоротший маршрут: {' -> '.join(path)}")
        st.info(f"Вартість маршруту: {length}")

        reserve=backup_path(start,end)
        if reserve:
            st.write(
            "Резервний маршрут:",
            " -> ".join(reserve)
            )

        st.write(
        "Зв'язність мережі:",
        "Так" if network_connected() else "Ні"
        )

        st.write(
        "Критичні вузли:",
        critical_nodes()
        )

        # Візуалізація
        pos=nx.spring_layout(G,seed=42)

        plt.figure(figsize=(14,8))

        nx.draw(
            G,pos,
            with_labels=True,
            node_size=1000
        )

        path_edges=list(zip(path,path[1:]))

        nx.draw_networkx_edges(
            G,pos,
            edgelist=path_edges,
            width=3
        )

        edge_labels=nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(
            G,pos,
            edge_labels=edge_labels
        )

        st.pyplot(plt)

    except:
        st.error("Маршрут не знайдено.")

# Тестування
if st.checkbox("Показати тестування"):

    tests=[
        ("PC1","DB_Server"),
        ("PC8","DNS_Server"),
        ("PC14","Mail_Server"),
        ("PC5","PC12")
    ]

    for a,b in tests:
        try:
            p,l=shortest_path(a,b)

            st.success(
                f"{a} -> {b}\n"
                f"Маршрут: {p}\n"
                f"Довжина={l}"
            )

        except nx.NetworkXNoPath:
            st.warning(
                f"{a} -> {b}: маршрут відсутній "
                f"(можлива відмова вузла)"
            )

        except:
            st.error(
                f"Помилка тесту {a}->{b}"
            )