import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import main  # Імпортуємо наш файл з логікою

st.set_page_config(page_title="Аналіз маршрутів мережі", layout="wide")

# Завантажуємо базовий граф
G_base = main.create_network()
nodes = sorted(G_base.nodes())

# ----------------------------
# Sidebar (Налаштування)
# ----------------------------
st.sidebar.header("Налаштування")

start = st.sidebar.selectbox("Початковий вузол", nodes)
end = st.sidebar.selectbox("Кінцевий вузол", nodes, index=5)
failed_node = st.sidebar.selectbox("Симуляція відмови вузла", ["Немає"] + nodes)

# Робимо копію графа для аналізу, щоб не зламати оригінал при видаленні вузла
G = G_base.copy()
if failed_node != "Немає":
    G.remove_node(failed_node)

# ----------------------------
# Головне вікно аналізу
# ----------------------------
st.title("Аналіз маршрутів та топології корпоративної мережі")

if st.button("Запустити аналіз"):
    
    # БЛОК 1: Базовий пошук маршрутів
    st.subheader("1. Пошук маршрутів")
    try:
        path, length = main.shortest_path(G, start, end)
        st.success(f"Найкоротший маршрут: {' -> '.join(path)}")
        st.info(f"Вартість маршруту: {length}")

        reserve = main.backup_path(G, start, end)
        if reserve:
            st.write("**Резервний маршрут:**", " -> ".join(reserve))

    except nx.NetworkXNoPath:
        st.error("Маршрут не знайдено. Вузли ізольовані один від одного.")
    except nx.NodeNotFound:
        st.error("Один з обраних вузлів недоступний (ймовірно, він відключений під час симуляції).")

    # БЛОК 2: Розширений аналіз топології (для викладача)
    st.subheader("2. Аналіз мережевої топології")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Щільність графа", f"{main.get_network_density(G):.4f}")
    
    is_connected = main.network_connected(G)
    col2.metric("Зв'язність мережі", "Так" if is_connected else "Ні (Розпад)")
    
    components = main.get_connected_components(G)
    col3.metric("Кількість компонент зв'язності", len(components))

    st.write("**Критичні вузли (Articulation Points):**", main.critical_nodes(G))
    
    if not is_connected:
        with st.expander("Деталі розпаду графа (ізольовані сегменти)"):
            for i, comp in enumerate(components):
                st.write(f"**Сегмент {i+1}:** {list(comp)}")

    # БЛОК 3: Аналіз ступенів та центральності
    st.subheader("3. Формальний аналіз вузлів (Centrality & Degrees)")
    metrics_df = main.get_node_metrics(G)
    st.dataframe(metrics_df, use_container_width=True)

    # БЛОК 4: Візуалізація
    st.subheader("4. Візуалізація мережі")
    
    tab1, tab2 = st.tabs(["Основна топологія", "Мінімальне остовне дерево (MST)"])
    pos = nx.spring_layout(G, seed=42)
    
    with tab1:
        fig1, ax1 = plt.subplots(figsize=(14, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1000, ax=ax1)
        if 'path' in locals():
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='red', ax=ax1)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax1)
        st.pyplot(fig1)

    with tab2:
        fig2, ax2 = plt.subplots(figsize=(14, 8))
        mst_graph = main.get_mst(G)
        nx.draw(mst_graph, pos, with_labels=True, node_color='lightgreen', node_size=1000, edge_color='green', width=2, ax=ax2)
        mst_labels = nx.get_edge_attributes(mst_graph, 'weight')
        nx.draw_networkx_edge_labels(mst_graph, pos, edge_labels=mst_labels, ax=ax2)
        st.pyplot(fig2)

# ----------------------------
# Тестування
# ----------------------------
st.markdown("---")
if st.checkbox("Показати результати тестування"):
    tests = [
        ("PC1","DB_Server"),
        ("PC8","DNS_Server"),
        ("PC14","Mail_Server"),
        ("PC5","PC12")
    ]

    for a, b in tests:
        try:
            p, l = main.shortest_path(G_base, a, b)
            st.success(f"{a} -> {b} | Маршрут: {p} | Довжина: {l}")
        except nx.NetworkXNoPath:
            st.warning(f"{a} -> {b}: маршрут відсутній")
        except Exception as e:
            st.error(f"Помилка тесту {a}->{b}: {e}")
